#!/bin/bash
# Fetch all results from sb-cli after overnight run completes

export SWEBENCH_API_KEY=$(grep SWEBENCH_API_KEY .env | cut -d'=' -f2)

echo "📊 FETCHING ALL BASELINE RESULTS"
echo "================================="
echo ""

# List all runs
echo "Your runs:"
sb-cli list-runs swe-bench_lite test
echo ""

# Fetch each model's results
for model in grok_best grok_budget openai_best openai_budget claude_best claude_budget google_best google_budget; do
    run_id="baseline_${model}_50problems"
    echo ""
    echo "Fetching: $model"
    echo "---"
    sb-cli get-report swe-bench_lite test $run_id 2>&1 | grep -E "Resolved|Submitted|Errors|Pending|runs"
done

echo ""
echo "================================="
echo "✅ All results fetched!"
echo ""
echo "Detailed reports saved in: sb-cli-reports/"
