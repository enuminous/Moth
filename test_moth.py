import pandas as pd
from features import build_moth_features
from moth import MOTHExperiment

FEATURES=["signal_a","signal_b","signal_c"]

def test_features():
    df=pd.read_csv("example_data.csv")
    mf=build_moth_features(df,FEATURES)
    assert len(mf)==len(df)
    assert "moth_temporal_score" in mf.columns
    assert mf["moth_temporal_score"].between(0,1).all()

def test_experiment_runs():
    df=pd.read_csv("example_data.csv")
    exp=MOTHExperiment(
        time_column="time",
        target_column="future_event",
        feature_columns=FEATURES,
    )
    out=exp.run(df)
    assert "results" in out
    assert "moth" in out["results"]
    assert "fourier_only" in out["results"]
