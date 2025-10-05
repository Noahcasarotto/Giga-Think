#!/bin/bash
# Show all SWE-bench benchmark results

export SWEBENCH_API_KEY=swb_7qXNMdZptY-e1eK-MlKwKUL8A_r_MSFL84RvJxhB_V4_68e1c2cd

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          SWE-BENCH LITE BENCHMARK RESULTS                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo "BASELINE SCORES (Blind Patching - 50 problems each):"
echo "────────────────────────────────────────────────────────────────"

for model in grok_best grok_budget openai_best openai_budget claude_best claude_budget google_best google_budget; do
    echo ""
    sb-cli get-report swe-bench_lite test baseline_${model}_50problems 2>/dev/null | grep "Resolved (submitted)" | sed "s/Resolved (submitted):/  $model:/"
done

echo ""
echo ""
echo "SWE-AGENT SCORE (Full Agentic - 1 problem):"
echo "────────────────────────────────────────────────────────────────"
sb-cli get-report swe-bench_lite test default__anthropic--claude-opus-4.1__t-0.00__p-1.00__c-5.00___swe_bench_lite_test_20251005112500953768 2>/dev/null | grep "Resolved (submitted)"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "LOCAL RESULTS (Not submitted - from trajectories):"
echo "  Claude Opus 4.1 SWE-agent: 9/10 patches generated ($96.43)"
echo "  (Quota exceeded - cannot get official evaluation)"
echo ""
