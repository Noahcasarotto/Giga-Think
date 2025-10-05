#!/bin/bash
# Overnight SWE-agent run with Modal (NO Docker needed!)
# Tests 10 problems per model with FULL agentic workflow

cd /Users/noahcasarotto-dinning/All\ of\ Coding/Giga-Think
source swe_venv/bin/activate
cd SWE-agent

echo "🚀 SWE-AGENT OVERNIGHT RUN - MODAL CLOUD EXECUTION"
echo "=================================================="
echo "Started: $(date)"
echo ""
echo "Configuration:"
echo "  • Models: 8"
echo "  • Problems per model: 10"
echo "  • Total: 80 problems"
echo "  • Platform: Modal (cloud containers)"
echo "  • Estimated time: 6-12 hours"
echo "  • Estimated cost: $40-80 ($5/problem avg)"
echo ""

# Models with openrouter/ prefix (works with litellm!)
models=(
  "openrouter/anthropic/claude-opus-4.1"
  "openrouter/anthropic/claude-sonnet-4.5"
  "openrouter/openai/gpt-5"
  "openrouter/openai/gpt-5-mini"
  "openrouter/x-ai/grok-4"
  "openrouter/x-ai/grok-3-mini"
  "openrouter/google/gemini-2.5-pro"
  "openrouter/google/gemini-2.5-flash"
)

names=(
  "claude_opus_41"
  "claude_sonnet_45"
  "gpt5"
  "gpt5_mini"
  "grok4"
  "grok3_mini"
  "gemini_25_pro"
  "gemini_25_flash"
)

# Test on problems 50-59 (fresh, avoid quota issues)
for i in "${!models[@]}"; do
  model="${models[$i]}"
  name="${names[$i]}"
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "MODEL $((i+1))/8: $model"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Started: $(date)"
  
  python -m sweagent run-batch \
    --config config/default.yaml \
    --agent.model.name "$model" \
    --agent.model.per_instance_cost_limit 10.00 \
    --instances.type swe_bench \
    --instances.subset lite \
    --instances.split test \
    --instances.slice 50:60 \
    --instances.evaluate=False \
    --instances.deployment.type=modal \
    --instances.deployment.image=python:3.12 \
    --num_workers 2 \
    2>&1 | tee "../testing/swe_agent_${name}_overnight.log"
  
  echo "✅ Model $((i+1))/8 complete! ($(date))"
  echo ""
  sleep 60
done

echo "🎉 ALL SWE-AGENT RUNS COMPLETE!"
echo "Finished: $(date)"
echo ""
echo "Results in: SWE-agent/trajectories/"
echo "Logs in: testing/swe_agent_*_overnight.log"
