from dataclasses import dataclass
import pandas as pd

from features import build_moth_features
from baselines import LogisticModel, BaseRateModel, autocorr_only, variance_only, fourier_power_only
from metrics import binary_metrics, stratify

@dataclass
class MOTHExperiment:
    time_column: str
    target_column: str
    feature_columns: list
    lags: tuple = (3,7,12,23)
    windows: tuple = (12,24,48)
    train_fraction: float = 0.65
    random_state: int = 23

    def run(self, df):
        df=df.sort_values(self.time_column).reset_index(drop=True).copy()
        cut=max(20,int(len(df)*self.train_fraction))
        y=df[self.target_column].astype(int).to_numpy()

        mf=build_moth_features(df,self.feature_columns,self.lags,self.windows)
        raw=df[self.feature_columns].astype(float).ffill().fillna(0.0)
        full=pd.concat([raw,mf],axis=1).fillna(0.0)

        autocorr=autocorr_only(df,self.feature_columns,lag=7,window=max(self.lags))
        variance=variance_only(df,self.feature_columns,window=max(self.lags))
        fourier=fourier_power_only(df,self.feature_columns,window=self.windows[1] if len(self.windows)>1 else self.windows[0])

        models={
            "moth":(LogisticModel(self.random_state),full),
            "raw_state":(LogisticModel(self.random_state),raw),
            "autocorr_only":(LogisticModel(self.random_state),autocorr),
            "variance_only":(LogisticModel(self.random_state),variance),
            "fourier_only":(LogisticModel(self.random_state),fourier),
            "base_rate":(BaseRateModel(),raw),
        }

        results={}
        for name,(model,X) in models.items():
            model.fit(X.iloc[:cut],y[:cut])
            p=model.predict_proba(X.iloc[cut:])
            results[name]={
                "overall":binary_metrics(y[cut:],p),
                "by_multiscale_activity":stratify(
                    y[cut:],p,mf["oscillation_power_mean"].to_numpy()[cut:]
                )
            }

        return {
            "n_total":len(df),
            "train_n":cut,
            "test_n":len(df)-cut,
            "results":results,
            "primary_delta_brier_raw_minus_moth":(
                results["raw_state"]["overall"]["brier"]
                - results["moth"]["overall"]["brier"]
            ),
            "interpretation":(
                "Positive delta favors MOTH over the matched raw-state model. "
                "Compare separately against ordinary autocorrelation and Fourier-power baselines."
            )
        }
