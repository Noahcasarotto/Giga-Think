#!/bin/bash
# Overnight baseline testing launcher

cd /Users/noahcasarotto-dinning/All\ of\ Coding/Giga-Think

echo "🚀 Starting overnight baseline test..."
echo "Started: $(date)"
echo ""

# Set API keys
export OPENROUTER_API_KEY=$(grep OPENROUTER_API_KEY .env | cut -d'=' -f2)
export SWEBENCH_API_KEY=$(grep SWEBENCH_API_KEY .env | cut -d'=' -f2)

# Run the test
python3 testing/baseline_all_models.py 2>&1 | tee testing/overnight_run.log

echo ""
echo "✅ Overnight run complete!"
echo "Finished: $(date)"
echo ""
echo "Check results:"
echo "  cat testing/overnight_run.log"
echo "  sb-cli list-runs swe-bench_lite test"
