import numpy as np
import pandas as pd

EPS = 1e-8

def detrend_rolling(s, window=23):
    s = s.astype(float)
    trend = s.rolling(window, min_periods=1).mean()
    return (s - trend).fillna(0.0)

def rolling_zero_crossing(s, window):
    sign = np.sign(s.fillna(0.0))
    cross = (sign != sign.shift(1)).astype(float)
    return cross.rolling(window, min_periods=1).mean().fillna(0.0)

def rolling_band_power(s, window):
    vals = np.zeros(len(s), dtype=float)
    arr = s.to_numpy(dtype=float)
    for i in range(len(arr)):
        start = max(0, i-window+1)
        seg = arr[start:i+1]
        if len(seg) < 4:
            vals[i] = 0.0
            continue
        seg = seg - np.mean(seg)
        spec = np.abs(np.fft.rfft(seg))**2
        if len(spec) <= 1:
            vals[i] = 0.0
        else:
            vals[i] = float(spec[1:].sum() / (len(seg) + EPS))
    return pd.Series(vals, index=s.index)

def build_moth_features(df, feature_columns, lags=(3,7,12,23), windows=(12,24,48)):
    x = df[feature_columns].astype(float).ffill().fillna(0.0)
    out = pd.DataFrame(index=df.index)

    detrended = {}
    for c in feature_columns:
        d = detrend_rolling(x[c], max(lags))
        detrended[c] = d
        out[f"{c}__detrended"] = d
        out[f"{c}__dx"] = d.diff().fillna(0.0)
        out[f"{c}__zero_cross"] = rolling_zero_crossing(d, max(lags))

        for lag in lags:
            out[f"{c}__autocorr_{lag}"] = (
                d.rolling(max(2*lag, 8), min_periods=5)
                 .corr(d.shift(lag))
                 .fillna(0.0)
            )

        for w in windows:
            out[f"{c}__bandpower_{w}"] = rolling_band_power(d, w)
            out[f"{c}__var_{w}"] = d.rolling(w, min_periods=2).var().fillna(0.0)

    # Multiscale recurrence: current state vs lagged state across frozen scales.
    recurrence_cols = []
    for lag in lags:
        parts = []
        for c in feature_columns:
            scale = detrended[c].rolling(max(lag,3), min_periods=1).std().fillna(0.0) + EPS
            similarity = np.exp(-((detrended[c] - detrended[c].shift(lag)).abs() / scale))
            parts.append(similarity.fillna(0.0))
        name = f"recurrence_{lag}"
        out[name] = pd.concat(parts, axis=1).mean(axis=1)
        recurrence_cols.append(name)

    # Agreement between scales.
    if recurrence_cols:
        out["cross_scale_agreement"] = 1.0 - out[recurrence_cols].std(axis=1).fillna(0.0)
        out["recurrence_mean"] = out[recurrence_cols].mean(axis=1)
        out["recurrence_peak"] = out[recurrence_cols].max(axis=1)
    else:
        out["cross_scale_agreement"] = 0.0
        out["recurrence_mean"] = 0.0
        out["recurrence_peak"] = 0.0

    band_cols = [c for c in out.columns if "__bandpower_" in c]
    if band_cols:
        bp = out[band_cols].clip(lower=0)
        total = bp.sum(axis=1).replace(0,np.nan)
        shares = bp.div(total, axis=0).fillna(0.0)
        out["scale_concentration"] = (shares**2).sum(axis=1)
        out["oscillation_power_mean"] = bp.mean(axis=1)
    else:
        out["scale_concentration"] = 0.0
        out["oscillation_power_mean"] = 0.0

    out["oscillation_growth"] = out["oscillation_power_mean"].diff().clip(lower=0).fillna(0.0)
    out["recurrence_change"] = out["recurrence_mean"].diff().abs().fillna(0.0)

    components = [
        out["cross_scale_agreement"].abs(),
        out["recurrence_mean"],
        out["recurrence_peak"],
        out["scale_concentration"],
        out["oscillation_power_mean"],
        out["oscillation_growth"],
        out["recurrence_change"],
    ]

    ranked = pd.concat(components, axis=1).rank(pct=True)
    out["moth_temporal_score"] = ranked.mean(axis=1).fillna(0.0)

    return out.replace([np.inf,-np.inf], np.nan).fillna(0.0)
