# Baseline Testing

Different baseline approaches for SWE-bench testing.

## Scripts

- `simple_baseline.py` - Single-pass prompting (6% success)
- `multi_model_baseline.py` - Test all 8 models in parallel

## Results

- Simple baseline: 0-6% across models
- Claude Opus 4.1 best at 6% (3/50)
- Cost: ~$0.03/problem

## Usage

```bash
python3 -m baselines.simple_baseline --model claude_best --problems 10
python3 -m baselines.multi_model_baseline --problems 50
```
