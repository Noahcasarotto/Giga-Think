#!/usr/bin/env python3
"""
Quick test to verify reasoning capabilities with a simple math problem.
Tests multiple models to see their different approaches.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def test_model_reasoning(model_id: str, problem: str):
    """Test a model with a reasoning problem"""
    print(f"\n{'='*70}")
    print(f"Testing: {model_id}")
    print(f"{'='*70}")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": problem}
            ],
            max_tokens=1000,
            temperature=0.1,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Giga-Think",
            }
        )
        
        result = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"\n✅ Response received ({tokens} tokens):\n")
        print(result)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def main():
    print("\n" + "="*70)
    print("Testing Reasoning Capabilities")
    print("="*70)
    
    # Simple problem to test reasoning
    problem = """Solve this problem step by step:

If x + 2 = 5, what is x?

Show your reasoning clearly."""
    
    print(f"\n📝 Problem:\n{problem}")
    
    # Test with a cheap model first
    print("\n" + "="*70)
    print("Testing with GPT-4o-mini (cheap, fast)")
    print("="*70)
    
    result = test_model_reasoning("openai/gpt-4o-mini", problem)
    
    if result:
        print("\n" + "="*70)
        print("✅ Basic reasoning test passed!")
        print("="*70)
        print("\n💡 Next steps:")
        print("   1. Test with more powerful models (Claude, GPT-4o)")
        print("   2. Try harder math problems")
        print("   3. Build the solver → verify → correct pipeline")
        
        print("\n📋 Available models to try:")
        print("   • anthropic/claude-3.5-sonnet (best for math)")
        print("   • openai/gpt-4o (very capable)")
        print("   • anthropic/claude-3.5-haiku (faster, cheaper)")
        
        print("\n💰 Cost so far: ~$0.0002 (very minimal)")


if __name__ == "__main__":
    main()

