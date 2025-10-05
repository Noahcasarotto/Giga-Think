#!/bin/bash
# Run SWE-bench evaluation on Modal (cloud containers, no local Docker!)

echo "☁️ MODAL EVALUATION - 9 Patches"
echo "══════════════════════════════════════════════════════════════"
echo "Using Modal cloud containers (no Docker needed!)"
echo "Estimated time: 30-60 minutes"
echo "Estimated cost: $5-10 (Modal compute)"
echo ""

cd SWE-bench

# Convert preds to JSONL
python3 << 'PYTHON'
import json

with open("../SWE-agent/trajectories/noahcasarotto-dinning/default__openrouter--anthropic--claude-opus-4.1__t-0.00__p-1.00__c-10.00___swe_bench_lite_test/preds.json") as f:
    preds = json.load(f)

with open("../swe_agent_eval.jsonl", "w") as f:
    for instance_id, data in preds.items():
        entry = {
            "instance_id": instance_id,
            "model_name_or_path": "swe_agent_claude_opus_41",
            "model_patch": data["model_patch"]
        }
        f.write(json.dumps(entry) + "\n")

print(f"✅ Converted {len(preds)} predictions")
PYTHON

echo ""
echo "Running Modal evaluation..."
echo ""

# Run on Modal (bypasses local Docker completely!)
python3 -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --predictions_path ../swe_agent_eval.jsonl \
    --run_id swe_agent_modal_eval \
    --max_workers 3 \
    --modal \
    2>&1 | tee ../testing/modal_eval_output.log

echo ""
echo "✅ Evaluation complete!"
echo "Check results in logs/"
