import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

class LogisticModel:
    def __init__(self, random_state=23):
        self.scaler = RobustScaler()
        self.model = LogisticRegression(max_iter=4000, random_state=random_state)
        self.constant_ = None

    def fit(self, X, y):
        y = np.asarray(y, dtype=int)
        if len(np.unique(y)) < 2:
            self.constant_ = float(y.mean()) if len(y) else 0.0
            return self
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X), y)
        return self

    def predict_proba(self, X):
        if self.constant_ is not None:
            return np.full(len(X), self.constant_)
        return self.model.predict_proba(self.scaler.transform(X))[:,1]

class BaseRateModel:
    def fit(self, X, y):
        self.p_ = float(np.mean(y))
        return self
    def predict_proba(self, X):
        return np.full(len(X), self.p_, dtype=float)

def autocorr_only(df, feature_columns, lag=7, window=23):
    x = df[feature_columns].astype(float).ffill().fillna(0.0)
    vals = []
    for c in feature_columns:
        vals.append(x[c].rolling(window, min_periods=5).corr(x[c].shift(lag)).fillna(0.0))
    return pd.DataFrame({"autocorr": pd.concat(vals,axis=1).mean(axis=1)})

def variance_only(df, feature_columns, window=23):
    x = df[feature_columns].astype(float).ffill().fillna(0.0)
    return pd.DataFrame({"rolling_variance": x.rolling(window,min_periods=2).var().mean(axis=1).fillna(0.0)})

def fourier_power_only(df, feature_columns, window=24):
    x = df[feature_columns].astype(float).ffill().fillna(0.0)
    vals = []
    for c in feature_columns:
        arr = x[c].to_numpy(dtype=float)
        power = np.zeros(len(arr))
        for i in range(len(arr)):
            start=max(0,i-window+1)
            seg=arr[start:i+1]
            if len(seg)<4:
                continue
            seg=seg-np.mean(seg)
            spec=np.abs(np.fft.rfft(seg))**2
            power[i]=float(spec[1:].sum()/(len(seg)+1e-8)) if len(spec)>1 else 0.0
        vals.append(pd.Series(power,index=df.index))
    return pd.DataFrame({"fourier_power":pd.concat(vals,axis=1).mean(axis=1)})
