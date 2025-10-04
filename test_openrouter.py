#!/usr/bin/env python3
"""
Test script to verify OpenRouter API connection and list available models.
OpenRouter provides unified access to GPT, Claude, Gemini, and many other models.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def test_openrouter_connection():
    """Test basic OpenRouter API connection"""
    print("\n" + "="*60)
    print("Testing OpenRouter API Connection")
    print("="*60)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_key_here":
        print("❌ OpenRouter API key not configured in .env file")
        print("\n📝 To get an API key:")
        print("   1. Visit: https://openrouter.ai/keys")
        print("   2. Sign up or log in")
        print("   3. Create a new API key")
        print("   4. Add it to your .env file as OPENROUTER_API_KEY")
        return False
    
    try:
        # OpenRouter uses OpenAI-compatible API
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Simple test call using a cheap model
        print("\n🔄 Testing with a simple call...")
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Cheap, widely available model
            messages=[
                {"role": "user", "content": "Say 'OpenRouter API test successful' and nothing else."}
            ],
            max_tokens=100,
            temperature=0.1,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",  # Optional
                "X-Title": "Giga-Think",  # Optional
            }
        )
        
        result = response.choices[0].message.content
        print(f"✅ OpenRouter API working!")
        print(f"   Model used: openai/gpt-4o-mini")
        print(f"   Response: {result}")
        print(f"   Tokens used: {response.usage.total_tokens}")
        
        # Check balance
        print(f"\n💰 Credit usage: ~$0.0001 (very cheap for testing)")
        print(f"   Visit https://openrouter.ai/activity to see your usage")
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter API error: {e}")
        return False


def list_recommended_models():
    """Display recommended models for the IMO-level reasoning system"""
    print("\n" + "="*60)
    print("Recommended Models for IMO-Level Reasoning")
    print("="*60)
    
    models = {
        "🧠 High-Performance Models": [
            {
                "id": "anthropic/claude-3.5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "best_for": "Complex reasoning, strong at math proofs",
                "context": "200K tokens"
            },
            {
                "id": "openai/gpt-4o",
                "name": "GPT-4o",
                "best_for": "General reasoning, good at structured thinking",
                "context": "128K tokens"
            },
            {
                "id": "google/gemini-pro-1.5",
                "name": "Gemini 1.5 Pro",
                "best_for": "Long context, detailed analysis",
                "context": "2M tokens"
            },
            {
                "id": "google/gemini-2.0-flash-thinking-exp:free",
                "name": "Gemini 2.0 Flash Thinking (FREE!)",
                "best_for": "Extended reasoning, completely free",
                "context": "32K tokens"
            },
        ],
        "💰 Budget-Friendly Testing Models": [
            {
                "id": "anthropic/claude-3.5-haiku",
                "name": "Claude 3.5 Haiku",
                "best_for": "Fast, cheap, still capable",
                "context": "200K tokens"
            },
            {
                "id": "openai/gpt-4o-mini",
                "name": "GPT-4o Mini",
                "best_for": "Testing pipelines cheaply",
                "context": "128K tokens"
            },
            {
                "id": "meta-llama/llama-3.1-70b-instruct",
                "name": "Llama 3.1 70B",
                "best_for": "Open source, good value",
                "context": "128K tokens"
            },
        ],
        "🆓 Free Models for Development": [
            {
                "id": "meta-llama/llama-3.1-8b-instruct:free",
                "name": "Llama 3.1 8B (Free)",
                "best_for": "Testing API connections",
                "context": "128K tokens"
            },
            {
                "id": "google/gemini-flash-1.5:free",
                "name": "Gemini 1.5 Flash (Free)",
                "best_for": "Quick prototyping",
                "context": "1M tokens"
            },
        ]
    }
    
    for category, model_list in models.items():
        print(f"\n{category}")
        print("-" * 60)
        for model in model_list:
            print(f"\n  📌 {model['name']}")
            print(f"     ID: {model['id']}")
            print(f"     Best for: {model['best_for']}")
            print(f"     Context: {model['context']}")


def test_reasoning_model(model_id: str):
    """Test a specific model with a simple math problem"""
    print("\n" + "="*60)
    print(f"Testing Model: {model_id}")
    print("="*60)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_key_here":
        print("❌ OpenRouter API key not configured")
        return False
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        test_problem = """Solve this simple problem:
If x + 2 = 5, what is x?

Show your reasoning step by step."""
        
        print(f"\n🔄 Testing with simple math problem...")
        print(f"   Problem: If x + 2 = 5, what is x?")
        
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": test_problem}
            ],
            max_tokens=500,
            temperature=0.1,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Giga-Think",
            }
        )
        
        result = response.choices[0].message.content
        print(f"\n✅ Response received!")
        print(f"   Tokens used: {response.usage.total_tokens}")
        print(f"\n📝 Model's solution:\n")
        print(result)
        return True
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("OpenRouter API Test Suite")
    print("="*60)
    print("\nOpenRouter provides unified access to multiple AI models:")
    print("• GPT (OpenAI)")
    print("• Claude (Anthropic)")
    print("• Gemini (Google)")
    print("• Llama (Meta)")
    print("• And many more!")
    
    # Test basic connection
    if not test_openrouter_connection():
        return
    
    # Show recommended models
    list_recommended_models()
    
    # Prompt to test a specific model
    print("\n" + "="*60)
    print("Test a Specific Model")
    print("="*60)
    print("\nWould you like to test a specific model with a simple problem?")
    print("(This will use a small amount of credits)")
    print("\nRecommended for testing:")
    print("  • google/gemini-2.0-flash-thinking-exp:free (FREE, good reasoning)")
    print("  • anthropic/claude-3.5-haiku (cheap, fast)")
    print("  • openai/gpt-4o-mini (cheap, fast)")
    print("\nOr just press Enter to skip.")
    
    model_choice = input("\nEnter model ID (or press Enter to skip): ").strip()
    
    if model_choice:
        test_reasoning_model(model_choice)
    
    print("\n" + "="*60)
    print("🎉 OpenRouter setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Choose your preferred model(s) for the reasoning system")
    print("  2. Start building the solver → verify → correct pipeline")
    print("  3. Test with progressively harder math problems")


if __name__ == "__main__":
    main()

