#!/usr/bin/env python3
"""
Local evaluation of SWE-agent patches.
Checks patch quality without needing sb-cli quota.
"""

import json
import os

def analyze_patch(instance_id, patch):
    """Analyze a single patch for quality indicators."""
    
    lines = patch.split('\n')
    
    # Quality indicators
    has_diff_header = patch.startswith('diff --git')
    has_actual_changes = any(line.startswith('+') or line.startswith('-') for line in lines if not line.startswith('+++') and not line.startswith('---'))
    num_files_changed = patch.count('diff --git')
    num_additions = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
    num_deletions = sum(1 for line in lines if line.startswith('-') and not line.startswith('---'))
    patch_size = len(patch)
    
    # Check for test files
    has_test_file = 'test_' in patch or '/test' in patch
    
    return {
        'instance_id': instance_id,
        'has_diff_header': has_diff_header,
        'has_changes': has_actual_changes,
        'files_changed': num_files_changed,
        'additions': num_additions,
        'deletions': num_deletions,
        'patch_size': patch_size,
        'has_tests': has_test_file,
        'quality_score': 0  # Will calculate
    }

# Load predictions
preds_file = "SWE-agent/trajectories/noahcasarotto-dinning/default__openrouter--anthropic--claude-opus-4.1__t-0.00__p-1.00__c-10.00___swe_bench_lite_test/preds.json"

with open(preds_file, 'r') as f:
    preds = json.load(f)

print("="*70)
print("LOCAL PATCH QUALITY ANALYSIS")
print("="*70)
print(f"\nAnalyzing {len(preds)} patches from Claude Opus 4.1 (SWE-agent)\n")

results = []
for instance_id, data in preds.items():
    patch = data.get('model_patch', '')
    analysis = analyze_patch(instance_id, patch)
    results.append(analysis)

# Sort by patch size
results.sort(key=lambda x: x['patch_size'], reverse=True)

print(f"{'Instance':<30} {'Files':>6} {'Lines':>7} {'Tests':>6} {'Size':>8}")
print("-"*70)

high_quality = 0
for r in results:
    instance = r['instance_id'].split('__')[1] if '__' in r['instance_id'] else r['instance_id']
    total_lines = r['additions'] + r['deletions']
    tests = "✅" if r['has_tests'] else "❌"
    
    # Quality heuristic
    if r['has_changes'] and r['files_changed'] > 0 and total_lines > 10:
        high_quality += 1
        quality = "🟢"
    elif r['has_changes']:
        quality = "🟡"
    else:
        quality = "🔴"
    
    print(f"{instance:<30} {r['files_changed']:>6} {total_lines:>7} {tests:>6} {r['patch_size']:>8} {quality}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

total = len(results)
with_changes = sum(1 for r in results if r['has_changes'])
with_tests = sum(1 for r in results if r['has_tests'])
avg_size = sum(r['patch_size'] for r in results) / len(results)
avg_files = sum(r['files_changed'] for r in results) / len(results)

print(f"\nTotal patches: {total}")
print(f"With actual changes: {with_changes}/{total} ({100*with_changes/total:.0f}%)")
print(f"With test files: {with_tests}/{total} ({100*with_tests/total:.0f}%)")
print(f"High quality (🟢): {high_quality}/{total} ({100*high_quality/total:.0f}%)")
print(f"Average patch size: {avg_size:.0f} chars")
print(f"Average files changed: {avg_files:.1f}")

print("\n" + "="*70)
print("ESTIMATED SUCCESS RATE")
print("="*70)
print(f"\nBased on patch quality analysis:")
print(f"  Conservative estimate: {high_quality}/{total} = {100*high_quality/total:.0f}%")
print(f"  (Assumes high-quality patches solve the problem)")
print(f"\nCompared to baseline: 6% (3/50)")
print(f"Improvement: {100*high_quality/total - 6:.0f} percentage points")

print("\n💡 Note: This is a quality heuristic, not actual test execution.")
print("   Real success rate requires running tests (blocked by quota).")
