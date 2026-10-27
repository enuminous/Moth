# MOTH

<!-- ENUMINOUS-UNIFIED-NAV:START -->
## Repository navigation

**eNuminous network:** [All public repositories](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md) · [EFMW](https://github.com/enuminous/EFMW) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [Frozen Lean](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Zoo](https://github.com/enuminous/Tortoise) · [Papers](https://github.com/enuminous/papers) · [Quantum geometry](https://github.com/enuminous/Base888-Quantum-Geometry)

**This project:** [Repository home](https://github.com/enuminous/Moth) · [Subject index](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md#zoo-index-and-agents)

<details open>
<summary><strong>On this page</strong></summary>

- [Intended uses](#intended-uses)
- [Core signal path](#core-signal-path)
- [Flat-stack repository](#flat-stack-repository)
- [Scientific hypothesis](#scientific-hypothesis)
- [Important interpretation rule](#important-interpretation-rule)
- [Example features](#example-features)
- [Baselines](#baselines)
- [Primary endpoint](#primary-endpoint)
- [Installation](#installation)
- [Run](#run)
- [Tests](#tests)
- [Minimal use](#minimal-use)
- [Freeze discipline](#freeze-discipline)
- [Negative results](#negative-results)
- [Status](#status)


</details>

**Related repositories:** [Tortoise](https://github.com/enuminous/Tortoise) · [Monolithic-Zoo-Lean4](https://github.com/enuminous/Monolithic-Zoo-Lean4) · [Monolithic-102-Zoo-Lean4](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Shark](https://github.com/enuminous/Shark) · [Ant](https://github.com/enuminous/Ant) · [Penguin](https://github.com/enuminous/Penguin) · [Dolphin](https://github.com/enuminous/Dolphin)

> **Evidence boundary:** A link between projects is navigation, not an assertion of proven equivalence, experimental validation, or shared authorship. See each repository’s own status and review notes.
<!-- ENUMINOUS-UNIFIED-NAV:END -->


**Multiscale Oscillation and Temporal Harmonics**

MOTH is an EFMW-derived framework for discovering which timescales actually carry useful structure in a sequential system.

Its narrow question is:

> Do multiscale recurrence and oscillation features add out-of-sample predictive information beyond standard autocorrelation and spectral baselines?

## Intended uses

- operations telemetry
- machinery
- demand forecasting
- network traffic
- logistics
- biological rhythms
- queueing systems
- market microstructure
- repeated human workflows
- any time series with suspected multi-timescale structure

## Core signal path

```text
time series
→ detrending
→ local oscillation
→ autocorrelation by lag
→ rolling frequency power
→ multiscale recurrence
→ cross-scale agreement / disagreement
→ MOTH temporal score
```

## Flat-stack repository

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
moth.py
features.py
baselines.py
metrics.py
freeze.py
temporal_schema.json
example_config.yaml
example_data.csv
example_run.py
test_moth.py
MANIFEST.sha256
```

## Scientific hypothesis

> Some systems contain useful predictive information distributed across multiple timescales, and cross-scale recurrence may matter beyond a single dominant period.

MOTH does not assume that this is true.

## Important interpretation rule

MOTH uses ordinary time-series mathematics.

Terms such as "harmonic" are operational here and refer to measurable periodic or quasi-periodic structure.

A result is not evidence for any special EFMW harmonic constant unless separately demonstrated.

## Example features

- lag autocorrelation
- rolling variance
- rolling zero-crossing rate
- spectral power in frozen bands
- recurrence similarity
- cross-scale agreement
- phase-change proxy
- oscillation growth
- scale concentration

## Baselines

Included:

- raw-state logistic model
- autocorrelation-only model
- Fourier-band-power model
- rolling-variance model
- base-rate predictor

## Primary endpoint

> Does MOTH improve out-of-sample prediction over a matched raw-state model and conventional temporal baselines?

Primary metric:

- Brier score

Secondary metrics:

- log loss
- ROC-AUC
- average precision
- performance by dominant-timescale regime

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python example_run.py
```

## Tests

```bash
pytest -q
```

## Minimal use

```python
import pandas as pd
from moth import MOTHExperiment

df = pd.read_csv("example_data.csv")

exp = MOTHExperiment(
    time_column="time",
    target_column="future_event",
    feature_columns=["signal_a","signal_b","signal_c"],
    lags=(3,7,12,23),
    windows=(12,24,48),
)

print(exp.run(df))
```

## Freeze discipline

Freeze before prospective testing:

- detrending rule
- lag set
- spectral windows
- frequency bands
- recurrence definition
- target
- data split
- baselines
- metrics
- exclusions
- seeds

Then run:

```bash
python freeze.py
```

## Negative results

If ordinary autocorrelation or spectral features match MOTH, then the multiscale EFMW-derived representation has not demonstrated incremental value.

## Status

Research software. Experimental.
