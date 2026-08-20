import json
import pandas as pd
from moth import MOTHExperiment

df=pd.read_csv("example_data.csv")

exp=MOTHExperiment(
    time_column="time",
    target_column="future_event",
    feature_columns=["signal_a","signal_b","signal_c"],
    lags=(3,7,12,23),
    windows=(12,24,48),
    random_state=23,
)

result=exp.run(df)
print(json.dumps(result,indent=2))
