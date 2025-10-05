#!/bin/bash
# Manually test one SWE-agent patch

echo "Manual Patch Evaluation"
echo "======================="
echo ""

# Pick the simplest patch (django-13448 - smallest)
INSTANCE="django__django-13448"
PATCH_FILE="SWE-agent/trajectories/noahcasarotto-dinning/default__openrouter--anthropic--claude-opus-4.1__t-0.00__p-1.00__c-10.00___swe_bench_lite_test/$INSTANCE/$INSTANCE.patch"

if [ -f "$PATCH_FILE" ]; then
    echo "✅ Found patch file"
    echo ""
    echo "Patch summary:"
    echo "──────────────"
    head -30 "$PATCH_FILE"
    echo ""
    echo "Patch size: $(wc -c < "$PATCH_FILE") bytes"
    echo "Files changed: $(grep -c 'diff --git' "$PATCH_FILE")"
    echo ""
    
    # Show what it's trying to fix
    echo "What this patch does:"
    echo "────────────────────"
    grep -A5 "^---\|^+++" "$PATCH_FILE" | head -20
else
    echo "❌ Patch file not found at: $PATCH_FILE"
    echo ""
    echo "Available instances:"
    ls -1 SWE-agent/trajectories/noahcasarotto-dinning/default__openrouter--anthropic--claude-opus-4.1__t-0.00__p-1.00__c-10.00___swe_bench_lite_test/ | grep django
fi
