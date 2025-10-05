#!/bin/bash
# Run SWE-agent (full agentic framework) baseline on all 8 models

cd /Users/noahcasarotto-dinning/All\ of\ Coding/Giga-Think
source swe_venv/bin/activate
cd SWE-agent

# Set SWE-bench API key for auto-evaluation
export SWEBENCH_API_KEY=swb_7qXNMdZptY-e1eK-MlKwKUL8A_r_MSFL84RvJxhB_V4_68e1c2cd

echo "🚀 Running SWE-agent baselines for all 8 models"
echo "This will take many hours (5-10 min per problem)"
echo "Each model: 10 problems (to start small)"
echo ""

# Model list
models=(
  "anthropic/claude-opus-4.1"
  "anthropic/claude-sonnet-4.5"
  "openai/gpt-5"
  "openai/gpt-5-mini"
  "x-ai/grok-4"
  "x-ai/grok-3-mini"
  "google/gemini-2.5-pro"
  "google/gemini-2.5-flash"
)

run_ids=(
  "sweagent_claude_opus41"
  "sweagent_claude_sonnet45"
  "sweagent_gpt5"
  "sweagent_gpt5mini"
  "sweagent_grok4"
  "sweagent_grok3mini"
  "sweagent_gemini25pro"
  "sweagent_gemini25flash"
)

for i in "${!models[@]}"; do
  model="${models[$i]}"
  run_id="${run_ids[$i]}"
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "MODEL $((i+1))/8: $model"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  python -m sweagent run-batch \
    --config config/default.yaml \
    --agent.model.name "$model" \
    --agent.model.per_instance_cost_limit 5.00 \
    --instances.type swe_bench \
    --instances.subset lite \
    --instances.split test \
    --instances.slice :10 \
    --instances.evaluate=True \
    --run_name "$run_id" \
    --num_workers 2
  
  echo "✅ Model $((i+1))/8 complete!"
  echo ""
  sleep 30
done

echo "🎉 All SWE-agent baselines complete!"
