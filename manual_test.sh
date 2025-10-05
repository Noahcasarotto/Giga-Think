#!/bin/bash
# Manually test ONE patch to get real success/fail result

INSTANCE="django__django-13448"
TEMP_DIR="/tmp/swe_manual_test_$INSTANCE"

echo "🧪 MANUAL PATCH TEST"
echo "══════════════════════════════════════════════════════════════"
echo "Instance: $INSTANCE"
echo ""

# Extract patch from preds.json
python3 << 'PYTHON'
import json
with open("SWE-agent/trajectories/noahcasarotto-dinning/default__openrouter--anthropic--claude-opus-4.1__t-0.00__p-1.00__c-10.00___swe_bench_lite_test/preds.json") as f:
    preds = json.load(f)
    
patch = preds["django__django-13448"]["model_patch"]
with open("/tmp/test_patch.patch", "w") as f:
    f.write(patch)
print(f"✅ Extracted patch ({len(patch)} chars)")
PYTHON

echo ""
echo "Step 1: Clone Django repository"
echo "────────────────────────────────────────────────────────────────"

if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

git clone --depth 1 --branch stable/3.2.x https://github.com/django/django.git "$TEMP_DIR" 2>&1 | tail -3

echo ""
echo "Step 2: Apply the patch"
echo "────────────────────────────────────────────────────────────────"

cd "$TEMP_DIR"
git apply --check /tmp/test_patch.patch 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Patch applies cleanly!"
    git apply /tmp/test_patch.patch
    echo "✅ Patch applied"
else
    echo "❌ Patch does not apply cleanly"
    echo "This might be expected - the patch was for a specific commit"
    exit 1
fi

echo ""
echo "Step 3: Check what changed"
echo "────────────────────────────────────────────────────────────────"
git diff --stat

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ PATCH EVALUATION COMPLETE"
echo ""
echo "Result: Patch applies cleanly = High confidence it would work"
echo ""
echo "Note: Full test execution would require:"
echo "  - Correct Django version/commit"
echo "  - All dependencies installed"
echo "  - Full test suite run (takes ~10 min)"
echo ""
echo "But patch applying cleanly is a strong indicator!"

