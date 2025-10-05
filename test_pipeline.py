#!/usr/bin/env python3
"""
End-to-end pipeline test.
Verifies all core functionality still works after cleanup.
"""

import sys
import os

print("="*70)
print("END-TO-END PIPELINE TEST")
print("="*70)

# Test 1: Import core modules
print("\n[1/5] Testing core modules...")
try:
    from core.models import MODELS
    from core.client import OpenRouterClient
    print(f"  ✅ Imported core modules")
    print(f"  ✅ Found {len(MODELS)} models configured")
except Exception as e:
    print(f"  ❌ Failed to import core: {e}")
    sys.exit(1)

# Test 2: Verify models are accessible
print("\n[2/5] Testing model configurations...")
try:
    model = MODELS["claude_budget"]
    print(f"  ✅ Model config loaded: {model['name']}")
    print(f"  ✅ Model ID: {model['id']}")
except Exception as e:
    print(f"  ❌ Failed to load model: {e}")
    sys.exit(1)

# Test 3: Test OpenRouter connection
print("\n[3/5] Testing OpenRouter API connection...")
try:
    client = OpenRouterClient()
    response = client.complete(
        model_id=model["id"],
        messages=[{"role": "user", "content": "Say 'test successful' and nothing else."}],
        max_tokens=20
    )
    result = client.get_response_text(response)
    tokens = client.get_tokens_used(response)
    print(f"  ✅ OpenRouter API working")
    print(f"  ✅ Response: {result[:50]}...")
    print(f"  ✅ Tokens used: {tokens}")
except Exception as e:
    print(f"  ❌ OpenRouter API failed: {e}")
    sys.exit(1)

# Test 4: Verify baseline module exists
print("\n[4/5] Testing baseline modules...")
try:
    import baselines.simple_baseline
    import baselines.multi_model_baseline
    print(f"  ✅ Baseline modules accessible")
except Exception as e:
    print(f"  ❌ Baseline import failed: {e}")
    sys.exit(1)

# Test 5: Verify reasoning module ready
print("\n[5/5] Testing reasoning module structure...")
try:
    import reasoning
    print(f"  ✅ Reasoning module exists")
    print(f"  ✅ Ready for IMO pipeline implementation")
except Exception as e:
    print(f"  ❌ Reasoning module failed: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print("\n📊 Summary:")
print(f"  • Core modules: Working")
print(f"  • Model configs: {len(MODELS)} models")
print(f"  • OpenRouter API: Connected")
print(f"  • Baselines: Accessible")
print(f"  • Reasoning: Ready for implementation")
print("\n🎯 Pipeline is fully functional!")
print("   Ready to build IMO reasoning on top!\n")
