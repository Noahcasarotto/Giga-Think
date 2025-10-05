# Overnight Baseline Testing

Complete baseline evaluation of all 8 models on SWE-bench Lite.

## 🚀 Quick Start

### 1. Run the overnight test:
```bash
./run_overnight.sh
```

This will:
- Test all 8 models on 50 problems each (400 total predictions)
- Generate predictions locally via OpenRouter
- Submit each batch to SWE-bench cloud for evaluation
- Run for ~4-6 hours

### 2. Monitor progress (while running):
```bash
./check_progress.sh
```

Or watch live:
```bash
tail -f testing/overnight_run.log
```

### 3. Get results (after completion):
```bash
./get_all_results.sh
```

## 📊 What You'll Get

Baseline scores for all 8 models:
- Grok 4
- Grok 3 Mini
- GPT-5
- GPT-5 Mini
- Claude Sonnet 4.5
- Claude Opus 4.1
- Gemini 2.5 Pro
- Gemini 2.5 Flash

## 💰 Cost Estimate

- ~400 predictions × $0.01-0.04 per prediction
- **Total: $5-15**
- Cloud evaluation is FREE (included in sb-cli)

## ⏱️ Timeline

- **Generation**: 4-6 hours (local OpenRouter calls)
- **Cloud Evaluation**: Happens automatically after submission
- **Results**: Available immediately after evaluation completes

## 📁 Output Files

- `testing/baseline_MODEL_KEY_50problems.jsonl` - Predictions for each model
- `testing/overnight_run.log` - Complete run log
- `testing/overnight_run_TIMESTAMP.json` - Master results file
- `sb-cli-reports/` - Detailed evaluation reports

## 🎯 Next Steps

After baselines are established:
1. Build IMO reasoning pipeline
2. Re-run same 50 problems with reasoning
3. Compare: Baseline vs Reasoning scores
4. Prove the pipeline works!
