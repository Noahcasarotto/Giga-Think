#!/bin/bash
# Run Docker evaluation on the 9 SWE-agent patches
# Should take ~60-90 minutes

echo "🐳 DOCKER EVALUATION - 9 Patches"
echo "══════════════════════════════════════════════════════════════"
echo "Estimated time: 60-90 minutes"
echo ""

# Clone fresh SWE-bench if needed
if [ ! -d "SWE-bench-eval" ]; then
    git clone https://github.com/princeton-nlp/SWE-bench.git SWE-bench-eval
fi

cd SWE-bench-eval

# Install
pip install -e . --quiet

# Convert preds to SWE-bench format
cd ..
python3 << 'PYTHON'
import json

# Load SWE-agent predictions
with open("SWE-agent/trajectories/noahcasarotto-dinning/default__openrouter--anthropic--claude-opus-4.1__t-0.00__p-1.00__c-10.00___swe_bench_lite_test/preds.json") as f:
    preds = json.load(f)

# Convert to JSONL format (one per line)
with open("swe_agent_preds_for_eval.jsonl", "w") as f:
    for instance_id, data in preds.items():
        entry = {
            "instance_id": instance_id,
            "model_name_or_path": "swe_agent_claude_opus_41",
            "model_patch": data["model_patch"]
        }
        f.write(json.dumps(entry) + "\n")

print(f"✅ Converted {len(preds)} predictions to JSONL")
PYTHON

echo ""
echo "Starting Docker evaluation..."
echo ""

# Run evaluation (local Docker, no modal)
python3 -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --predictions_path swe_agent_preds_for_eval.jsonl \
    --max_workers 2 \
    --run_id swe_agent_claude_opus_eval \
    --timeout 900

echo ""
echo "✅ Evaluation complete!"
echo "Results in: logs/run_evaluation/swe_agent_claude_opus_eval/"
