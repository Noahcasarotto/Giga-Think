#!/usr/bin/env python3
"""Test if strict diff formatting fixes the patch errors."""

import os, sys, json, re
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset
from models_config import MODELS

load_dotenv()

STRUCTURED_PROMPT = """You are a software engineer. Provide a COMPLETE, VALID git diff patch.

Repository: {repo}
Problem: {problem_statement}

CRITICAL - Output Format:
1. Brief explanation (1-2 sentences)
2. Complete git diff patch in this EXACT format:

```diff
diff --git a/filename.py b/filename.py
--- a/filename.py
+++ b/filename.py
@@ -10,7 +10,7 @@
 context line
-old line
+new line
 context line
```

Make the patch COMPLETE - do not truncate. End with newline."""

def main():
    # Test on 2 problems
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
    model = MODELS["google_budget"]
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    
    print("="*70)
    print("STRUCTURED OUTPUT TEST - Gemini 2.5 Flash")
    print("="*70)
    print("Testing 2 problems with STRICT diff formatting\n")
    
    results = []
    for i, inst in enumerate(list(dataset)[:2]):
        print(f"\n{'='*70}")
        print(f"Problem {i+1}/2: {inst['instance_id']}")
        print(f"{'='*70}")
        
        response = client.chat.completions.create(
            model=model["id"],
            messages=[{"role": "user", "content": STRUCTURED_PROMPT.format(
                repo=inst['repo'], problem_statement=inst['problem_statement']
            )}],
            max_tokens=4000,
            temperature=0.1,
            extra_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "Giga-Think"}
        )
        
        solution = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"✅ Response received ({tokens} tokens)")
        
        # Extract diff
        diff_match = re.search(r'```diff\n(.*?)```', solution, re.DOTALL)
        if diff_match:
            patch = diff_match.group(1).strip()
            print(f"✅ Found diff block ({len(patch)} chars)")
            print(f"   Starts: {patch[:60]}...")
            print(f"   Ends: ...{patch[-60:]}")
        else:
            patch = solution
            print(f"⚠️  No diff block found")
        
        results.append({
            "instance_id": inst['instance_id'],
            "model_name_or_path": model["name"],
            "model_patch": patch
        })
    
    # Save
    output_file = "testing/predictions_structured_2.jsonl"
    with open(output_file, 'w') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
    
    print(f"\n{'='*70}")
    print(f"💾 Saved {len(results)} predictions to: {output_file}")
    print(f"{'='*70}")
    print("\nNext: Run evaluation to see if structured output fixes errors!")
    print("\nCommand:")
    print(f"python3 -m swebench.harness.run_evaluation \\")
    print(f"  --dataset_name princeton-nlp/SWE-bench_Lite \\")
    print(f"  --predictions_path {output_file} \\")
    print(f"  --max_workers 2 \\")
    print(f"  --run_id structured_test \\")
    print(f"  --modal false")

if __name__ == "__main__":
    main()
