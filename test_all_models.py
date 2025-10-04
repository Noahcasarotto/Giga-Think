#!/usr/bin/env python3
"""
Test all 8 configured models to ensure they're accessible via OpenRouter.
This validates that each model ID is correct and returns reasonable responses.
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from models_config import MODELS, list_all_models

load_dotenv()


def test_single_model(client: OpenAI, key: str, model_config: dict, problem: str):
    """Test a single model with a simple problem"""
    
    model_id = model_config["id"]
    model_name = model_config["name"]
    
    print(f"\n{'='*70}")
    print(f"Testing: {model_name}")
    print(f"ID: {model_id}")
    print(f"{'='*70}")
    
    try:
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": problem}
            ],
            max_tokens=300,
            temperature=0.1,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Giga-Think",
            }
        )
        
        elapsed = time.time() - start_time
        result = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"✅ SUCCESS ({elapsed:.2f}s, {tokens} tokens)")
        print(f"\nResponse preview (first 200 chars):")
        print(f"{result[:200]}...")
        
        return {
            "success": True,
            "key": key,
            "model": model_name,
            "tokens": tokens,
            "time": elapsed,
            "response": result
        }
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return {
            "success": False,
            "key": key,
            "model": model_name,
            "error": str(e)
        }


def test_all_models():
    """Test all 8 models"""
    
    print("\n" + "="*70)
    print("Testing All 8 Models")
    print("="*70)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found in .env")
        return
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # Simple test problem
    problem = """Solve: If 2x + 3 = 11, what is x?
    
Show your work briefly."""
    
    print(f"\n📝 Test problem: {problem}")
    print("\n" + "="*70)
    
    results = []
    
    # Test each model
    for key, model_config in MODELS.items():
        result = test_single_model(client, key, model_config, problem)
        results.append(result)
        
        # Small delay to avoid rate limits
        time.sleep(0.5)
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print("\n🎉 Working models:")
        for r in successful:
            print(f"   ✓ {r['model']} ({r['key']}) - {r['tokens']} tokens, {r['time']:.2f}s")
    
    if failed:
        print("\n⚠️  Failed models:")
        for r in failed:
            print(f"   ✗ {r['model']} ({r['key']})")
            print(f"      Error: {r['error']}")
    
    # Cost estimate
    total_tokens = sum(r.get("tokens", 0) for r in successful)
    estimated_cost = total_tokens * 0.000001 * 10  # Very rough estimate
    print(f"\n💰 Estimated cost for testing: ~${estimated_cost:.4f}")
    
    if len(successful) == len(results):
        print("\n🎉 All models working! Ready to build the reasoning pipeline.")
    elif len(successful) > 0:
        print(f"\n✅ {len(successful)} models working. You can proceed with those.")
        print("   (Some model IDs may need adjustment)")
    else:
        print("\n⚠️  No models working. Check your API key and model IDs.")
    
    return results


def test_quick():
    """Quick test with just one model from each provider"""
    
    print("\n" + "="*70)
    print("Quick Test (1 model per provider)")
    print("="*70)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found in .env")
        return
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    problem = "What is 5 + 3? Just say the number."
    
    # Test one from each provider
    quick_models = {
        "openai_budget": MODELS["openai_budget"],
        "claude_budget": MODELS["claude_budget"],
        "google_budget": MODELS["google_budget"],
        "grok_budget": MODELS["grok_budget"],
    }
    
    results = []
    for key, model_config in quick_models.items():
        result = test_single_model(client, key, model_config, problem)
        results.append(result)
        time.sleep(0.5)
    
    successful = [r for r in results if r["success"]]
    print(f"\n✅ Quick test: {len(successful)}/4 providers working")


if __name__ == "__main__":
    import sys
    
    # Show model list
    list_all_models()
    
    # Determine which test to run
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        test_quick()
    else:
        print("\n" + "="*70)
        print("Ready to test all 8 models")
        print("="*70)
        print("\nThis will:")
        print("  • Test each model with a simple math problem")
        print("  • Show which models are accessible")
        print("  • Estimate total cost (should be <$0.01)")
        print("\nOptions:")
        print("  python3 test_all_models.py         - Test all 8 models")
        print("  python3 test_all_models.py --quick - Test 1 per provider (faster)")
        
        input("\nPress Enter to test all 8 models (or Ctrl+C to cancel)...")
        test_all_models()

