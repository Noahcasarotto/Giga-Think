#!/usr/bin/env python3
"""
Comprehensive baseline test for all 8 models.
Runs overnight on 50 SWE-bench problems per model.
Generates predictions locally, submits to sb-cli cloud for evaluation.
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset
from models_config import MODELS

load_dotenv()

STRUCTURED_PROMPT = """You are a software engineer fixing a bug. Provide a COMPLETE, VALID git diff patch.

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


def generate_predictions_for_model(model_key, instances, num_problems=50):
    """Generate predictions for a single model."""
    
    model_config = MODELS[model_key]
    
    print(f"\n{'='*70}")
    print(f"GENERATING PREDICTIONS: {model_config['name']}")
    print(f"{'='*70}")
    print(f"Model: {model_config['id']}")
    print(f"Problems: {num_problems}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    predictions = []
    errors = []
    
    for i, instance in enumerate(instances[:num_problems], 1):
        instance_id = instance['instance_id']
        
        print(f"\n[{i}/{num_problems}] {instance_id}")
        
        try:
            prompt = STRUCTURED_PROMPT.format(
                repo=instance['repo'],
                problem_statement=instance['problem_statement']
            )
            
            response = client.chat.completions.create(
                model=model_config["id"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.1,
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Giga-Think-Baseline",
                }
            )
            
            solution = response.choices[0].message.content
            tokens = response.usage.total_tokens
            
            # Extract diff
            diff_match = re.search(r'```diff\n(.*?)```', solution, re.DOTALL)
            if diff_match:
                patch = diff_match.group(1).strip()
            else:
                patch = solution
            
            # Ensure patch ends with newline
            if not patch.endswith('\n'):
                patch += '\n'
            
            predictions.append({
                "instance_id": instance_id,
                "model_name_or_path": model_config["name"],
                "model_patch": patch
            })
            
            print(f"  ✅ {tokens} tokens, patch: {len(patch)} chars")
            
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ Error: {error_msg[:100]}")
            errors.append({
                "instance_id": instance_id,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            time.sleep(2)  # Longer delay after error
    
    # Save predictions
    output_file = f"testing/baseline_{model_key}_{num_problems}problems.jsonl"
    with open(output_file, 'w') as f:
        for pred in predictions:
            f.write(json.dumps(pred) + '\n')
    
    # Save errors log
    if errors:
        error_file = f"testing/errors_{model_key}_{num_problems}problems.json"
        with open(error_file, 'w') as f:
            json.dump(errors, f, indent=2)
        print(f"\n  ⚠️  {len(errors)} errors logged to {error_file}")
    
    print(f"\n{'='*70}")
    print(f"COMPLETED: {model_config['name']}")
    print(f"{'='*70}")
    print(f"✅ Predictions: {len(predictions)}/{num_problems}")
    print(f"❌ Errors: {len(errors)}")
    print(f"💾 Saved to: {output_file}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return output_file, len(predictions), len(errors)


def submit_to_cloud(predictions_file, model_key, run_id):
    """Submit predictions to sb-cli cloud evaluation."""
    
    print(f"\n{'='*70}")
    print(f"SUBMITTING TO CLOUD: {run_id}")
    print(f"{'='*70}")
    
    # Submit command
    cmd = f"sb-cli submit swe-bench_lite test --predictions_path {predictions_file} --run_id {run_id}"
    
    print(f"Command: {cmd}")
    print(f"Submitting...")
    
    result = os.system(f"export SWEBENCH_API_KEY={os.getenv('SWEBENCH_API_KEY')} && {cmd}")
    
    if result == 0:
        print(f"✅ Submitted successfully!")
        return True
    else:
        print(f"❌ Submission failed (exit code: {result})")
        return False


def main():
    """Run baseline tests for all 8 models overnight."""
    
    print("="*70)
    print("OVERNIGHT BASELINE TEST - ALL 8 MODELS")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Problems per model: 50")
    print(f"Total predictions: 400 (8 models × 50 problems)")
    print("="*70)
    
    # Load dataset once
    print("\nLoading SWE-bench Lite dataset...")
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    instances = list(dataset)[:50]  # First 50 problems
    print(f"✅ Loaded {len(instances)} problems\n")
    
    # Track results
    all_results = []
    
    # Test each model
    for i, (model_key, model_config) in enumerate(MODELS.items(), 1):
        print(f"\n\n{'#'*70}")
        print(f"MODEL {i}/8: {model_config['name']}")
        print(f"{'#'*70}")
        
        try:
            # Generate predictions
            predictions_file, num_preds, num_errors = generate_predictions_for_model(
                model_key, instances, num_problems=50
            )
            
            # Submit to cloud
            run_id = f"baseline_{model_key}_50problems"
            submitted = submit_to_cloud(predictions_file, model_key, run_id)
            
            all_results.append({
                "model_key": model_key,
                "model_name": model_config["name"],
                "predictions_file": predictions_file,
                "num_predictions": num_preds,
                "num_errors": num_errors,
                "submitted": submitted,
                "run_id": run_id if submitted else None,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"\n✅ Model {i}/8 complete!")
            print(f"   Wait time before next model: 30 seconds...")
            time.sleep(30)  # Rate limiting between models
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR for {model_key}: {e}")
            all_results.append({
                "model_key": model_key,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            time.sleep(60)  # Longer wait after critical error
    
    # Save master results
    master_file = f"testing/overnight_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(master_file, 'w') as f:
        json.dump({
            "start_time": datetime.now().isoformat(),
            "total_models": 8,
            "problems_per_model": 50,
            "results": all_results
        }, f, indent=2)
    
    # Print summary
    print(f"\n\n{'='*70}")
    print("OVERNIGHT RUN COMPLETE!")
    print(f"{'='*70}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults:")
    
    successful = sum(1 for r in all_results if r.get("submitted"))
    print(f"  ✅ Successfully submitted: {successful}/8 models")
    print(f"  ❌ Failed: {8 - successful}/8 models")
    
    print(f"\n💾 Master log saved to: {master_file}")
    
    print(f"\n{'='*70}")
    print("TO GET RESULTS:")
    print(f"{'='*70}")
    print("Run this to see all your submissions:")
    print("  export SWEBENCH_API_KEY=swb_7qXNMdZptY-e1eK-MlKwKUL8A_r_MSFL84RvJxhB_V4_68e1c2cd")
    print("  sb-cli list-runs swe-bench_lite test")
    print("\nThen get each report:")
    print("  sb-cli get-report swe-bench_lite test baseline_MODEL_KEY_50problems")
    
    print(f"\n🎉 All baselines established! Ready to build reasoning pipeline!")


if __name__ == "__main__":
    print("\n⚠️  This will run for several hours!")
    print("Estimated time: 4-6 hours (depending on rate limits)")
    print("Cost estimate: ~$5-15 (400 predictions × avg $0.01-0.04 per prediction)")
    print("\nPress Ctrl+C within 5 seconds to cancel...")
    
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(0)
    
    print("\n🚀 Starting overnight baseline run...\n")
    main()
