#!/usr/bin/env python3
"""
Convert our baseline results to SWE-bench evaluation format.
SWE-bench expects JSONL with: instance_id, model_name_or_path, model_patch
"""

import json
import sys
import re

def extract_patch_from_solution(solution):
    """Extract the diff patch from the model's solution."""
    # Look for code blocks with diff
    diff_pattern = r'```(?:diff)?\n(.*?)```'
    matches = re.findall(diff_pattern, solution, re.DOTALL)
    
    if matches:
        # Return the first diff block
        patch = matches[0].strip()
        # Ensure it starts with diff or ---
        if not patch.startswith('diff') and not patch.startswith('---'):
            # Add diff header if missing
            patch = f"diff --git a/file.py b/file.py\n{patch}"
        return patch
    
    # If no code block, try to find diff-like content
    lines = solution.split('\n')
    patch_lines = []
    in_patch = False
    
    for line in lines:
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            in_patch = True
        if in_patch:
            patch_lines.append(line)
    
    if patch_lines:
        return '\n'.join(patch_lines)
    
    # Last resort: return the whole solution
    return solution

def convert_results(input_file, output_file):
    """Convert our format to SWE-bench format."""
    
    with open(input_file, 'r') as f:
        results = json.load(f)
    
    swebench_results = []
    
    for result in results:
        if 'error' in result:
            print(f"⚠️  Skipping {result.get('instance_id', 'unknown')} - had error")
            continue
        
        patch = extract_patch_from_solution(result['solution'])
        
        swebench_entry = {
            "instance_id": result['instance_id'],
            "model_name_or_path": result['model'],
            "model_patch": patch
        }
        
        swebench_results.append(swebench_entry)
        print(f"✅ Converted {result['instance_id']}")
    
    # Write as JSONL (one JSON object per line)
    with open(output_file, 'w') as f:
        for entry in swebench_results:
            f.write(json.dumps(entry) + '\n')
    
    print(f"\n💾 Saved {len(swebench_results)} predictions to {output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_swebench_format.py input.json output.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_results(input_file, output_file)
