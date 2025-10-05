#!/usr/bin/env python3
"""
SWE-bench Lite Baseline Test
Loads the dataset and tests models WITHOUT any reasoning pipeline.
Just establishes baseline performance.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path to import models_config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset
from models_config import MODELS

load_dotenv()


def load_swe_bench_lite(num_samples=5):
    """Load first N samples from SWE-bench Lite for quick testing."""
    print("Loading SWE-bench Lite dataset...")
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    print(f"✅ Loaded {len(dataset)} total problems")
    print(f"   Testing on first {num_samples} samples\n")
    # Convert to list for easier slicing
    return list(dataset)[:num_samples]


def format_problem_for_model(instance):
    """Format a SWE-bench problem for the model."""
    prompt = f"""You are a software engineer tasked with fixing a bug.

**Repository**: {instance['repo']}
**Problem Statement**:
{instance['problem_statement']}

**Instructions**:
1. Analyze the problem carefully
2. Provide a fix in the form of a git diff patch
3. Explain your reasoning

Provide your solution as a complete patch."""
    
    return prompt


def test_model_baseline(model_key, instances, max_problems=3):
    """Test a model on SWE-bench problems without any reasoning pipeline."""
    
    model_config = MODELS[model_key]
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    print("="*70)
    print(f"BASELINE TEST: {model_config['name']}")
    print("="*70)
    print(f"Testing on {min(max_problems, len(instances))} problems")
    print("NO reasoning pipeline - just direct solving\n")
    
    results = []
    
    for i, instance in enumerate(instances[:max_problems]):
        print(f"\n{'='*70}")
        print(f"Problem {i+1}/{max_problems}: {instance['instance_id']}")
        print(f"{'='*70}")
        print(f"Repo: {instance['repo']}")
        print(f"Problem: {instance['problem_statement'][:100]}...")
        
        prompt = format_problem_for_model(instance)
        
        try:
            print(f"\n🔄 Querying {model_config['name']}...")
            
            response = client.chat.completions.create(
                model=model_config["id"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.1,
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Giga-Think-SWE-Baseline",
                }
            )
            
            solution = response.choices[0].message.content
            tokens = response.usage.total_tokens
            
            print(f"✅ Response received ({tokens} tokens)")
            print(f"\nSolution preview (first 200 chars):")
            print(solution[:200] + "...")
            
            result = {
                "instance_id": instance["instance_id"],
                "repo": instance["repo"],
                "model": model_config["name"],
                "model_id": model_config["id"],
                "tokens": tokens,
                "solution": solution,
                "timestamp": datetime.now().isoformat(),
                "problem_statement": instance["problem_statement"]
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "instance_id": instance["instance_id"],
                "error": str(e)
            })
    
    # Save results
    output_file = f"testing/baseline_results_{model_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print("BASELINE TEST COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Tested {len(results)} problems")
    print(f"💾 Results saved to: {output_file}")
    print(f"\nNext steps:")
    print(f"1. Review the solutions manually")
    print(f"2. Later: Build reasoning pipeline")
    print(f"3. Later: Re-run and compare improvement")
    
    return results


def quick_peek_at_dataset():
    """Just look at what a SWE-bench problem looks like."""
    print("\n" + "="*70)
    print("PEEKING AT SWE-BENCH LITE DATASET")
    print("="*70)
    
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    
    print(f"\nDataset size: {len(dataset)} problems")
    print(f"\nFields in each problem:")
    print(list(dataset[0].keys()))
    
    print(f"\n{'='*70}")
    print("FIRST PROBLEM EXAMPLE:")
    print(f"{'='*70}")
    
    example = dataset[0]
    print(f"\nInstance ID: {example['instance_id']}")
    print(f"Repo: {example['repo']}")
    print(f"\nProblem Statement:")
    print(example['problem_statement'][:500] + "...")
    
    return dataset


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--peek":
            # Just look at the dataset
            quick_peek_at_dataset()
            
        elif sys.argv[1] == "--test":
            # Run baseline test
            model_key = sys.argv[2] if len(sys.argv) > 2 else "claude_budget"
            num_problems = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            
            instances = load_swe_bench_lite(num_samples=num_problems)
            test_model_baseline(model_key, instances, max_problems=num_problems)
    else:
        print("\nUsage:")
        print("  python testing/swe_bench_baseline.py --peek")
        print("    └─ Just look at the dataset structure")
        print()
        print("  python testing/swe_bench_baseline.py --test [model_key] [num_problems]")
        print("    └─ Test a model on N problems")
        print()
        print("Examples:")
        print("  python testing/swe_bench_baseline.py --peek")
        print("  python testing/swe_bench_baseline.py --test google_budget 2")
        print("  python testing/swe_bench_baseline.py --test grok_best 5")
        print()
        print("Available models:", ", ".join(MODELS.keys()))
