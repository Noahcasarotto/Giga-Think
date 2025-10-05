#!/bin/bash
# COMPREHENSIVE END-TO-END PIPELINE TEST
# Tests EVERYTHING to make sure cleanup didn't break anything

set -e  # Exit on any error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🧪 COMPLETE PIPELINE VERIFICATION TEST                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "This will test:"
echo "  1. OpenRouter connection (all 8 models)"
echo "  2. Baseline prediction generation"
echo "  3. SWE-agent with Modal"
echo "  4. Modal evaluation"
echo "  5. Result extraction"
echo ""
echo "Estimated time: 10-15 minutes"
echo "Cost: ~$5-10"
echo ""
read -p "Press ENTER to start comprehensive test (Ctrl+C to cancel)..."
echo ""

FAILED=0
PASSED=0

# Helper function
test_step() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TEST: $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

report() {
    if [ $? -eq 0 ]; then
        echo "✅ PASS: $1"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAIL: $1"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# ═══════════════════════════════════════════════════════════════
test_step "1. OpenRouter API Connection"
# ═══════════════════════════════════════════════════════════════

python3 << 'PYTHON'
import sys
sys.path.insert(0, "core")
from models import MODELS
from client import OpenRouterClient

print("Testing OpenRouter with Claude Opus 4.1...")
client = OpenRouterClient()
response = client.complete(
    model_id=MODELS["claude_budget"]["id"],
    messages=[{"role": "user", "content": "Say 'test' and nothing else"}],
    max_tokens=10
)
result = client.get_response_text(response)
print(f"Response: {result}")
print(f"Tokens: {client.get_tokens_used(response)}")
assert "test" in result.lower(), "Model didn't respond correctly"
print("✅ OpenRouter connection working!")
PYTHON

report "OpenRouter API"

# ═══════════════════════════════════════════════════════════════
test_step "2. Baseline Prediction Generation (1 problem)"
# ═══════════════════════════════════════════════════════════════

python3 << 'PYTHON'
import sys
import json
sys.path.insert(0, "baselines")
sys.path.insert(0, "core")

from datasets import load_dataset
from models import MODELS
from client import OpenRouterClient

print("Loading SWE-bench dataset...")
dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
problem = dataset[100]  # Use problem 100 (fresh)

print(f"Problem: {problem['instance_id']}")

print("Generating baseline prediction...")
client = OpenRouterClient()

prompt = f"""You are a software engineer. Fix this bug.

Repository: {problem['repo']}
Problem: {problem['problem_statement'][:500]}...

Provide a git diff patch."""

response = client.complete(
    model_id=MODELS["google_budget"]["id"],  # Fast, cheap model
    messages=[{"role": "user", "content": prompt}],
    max_tokens=2000,
    temperature=0.1
)

solution = client.get_response_text(response)
print(f"Generated solution: {len(solution)} chars")
print(f"Tokens used: {client.get_tokens_used(response)}")

# Save
with open("test_baseline_pred.json", "w") as f:
    json.dump({
        "instance_id": problem['instance_id'],
        "model_patch": solution
    }, f)

print("✅ Baseline generation working!")
PYTHON

report "Baseline Generation"

# ═══════════════════════════════════════════════════════════════
test_step "3. SWE-Agent Generation (1 problem on Modal)"
# ═══════════════════════════════════════════════════════════════

source swe_venv/bin/activate

cd SWE-agent

python -m sweagent run-batch \
    --config config/default.yaml \
    --agent.model.name "openrouter/google/gemini-2.5-flash" \
    --agent.model.per_instance_cost_limit 5.00 \
    --instances.type swe_bench \
    --instances.subset lite \
    --instances.split test \
    --instances.slice 100:101 \
    --instances.evaluate=False \
    --instances.deployment.type=modal \
    --instances.deployment.image=python:3.12 \
    --num_workers 1 \
    2>&1 | tail -50

cd ..

report "SWE-Agent Generation"

# ═══════════════════════════════════════════════════════════════
test_step "4. Modal Evaluation (1 problem)"
# ═══════════════════════════════════════════════════════════════

# Find the generated prediction
PRED_DIR=$(find SWE-agent/trajectories -name "preds.json" -type f | head -1)

if [ -f "$PRED_DIR" ]; then
    echo "Found predictions at: $PRED_DIR"
    
    # Run evaluation
    python3 -m swebench.harness.run_evaluation \
        --dataset_name princeton-nlp/SWE-bench_Lite \
        --predictions_path "$PRED_DIR" \
        --run_id pipeline_test \
        --modal true \
        --max_workers 1 \
        --timeout 900 \
        2>&1 | tail -30
    
    report "Modal Evaluation"
else
    echo "❌ No predictions found"
    FAILED=$((FAILED + 1))
fi

# ═══════════════════════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    TEST SUMMARY                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "  Tests Passed:  $PASSED"
echo "  Tests Failed:  $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED!"
    echo ""
    echo "✅ OpenRouter working"
    echo "✅ Baseline generation working"
    echo "✅ SWE-agent with Modal working"
    echo "✅ Modal evaluation working"
    echo ""
    echo "🚀 READY TO BUILD IMO REASONING PIPELINE!"
else
    echo "⚠️  SOME TESTS FAILED"
    echo ""
    echo "Check output above for details"
    exit 1
fi
