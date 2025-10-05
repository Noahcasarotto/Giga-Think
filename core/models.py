"""
Model configurations for IMO-level reasoning system.
Includes best and budget models from each major provider.

Note: Some models may require specific OpenRouter subscription tiers.
Check https://openrouter.ai/models for current availability.
"""

# Model configurations: 8 total (2 per provider)
# Models marked with 'available': True are confirmed working
MODELS = {
    # Grok (xAI) - 1M free BYOK requests per month
    "grok_best": {
        "id": "x-ai/grok-4",
        "name": "Grok 4",
        "provider": "xAI",
        "tier": "best",
        "context_window": "256K tokens",
        "notes": "Latest reasoning model, supports tool calling & structured outputs",
        "available": True,
    },
    "grok_budget": {
        "id": "x-ai/grok-3-mini", 
        "name": "Grok 3 Mini",
        "provider": "xAI",
        "tier": "budget",
        "context_window": "128K tokens",
        "notes": "Lightweight thinking model, fast and smart for logic tasks",
        "available": True,
    },
    
    # OpenAI - 1M free BYOK requests per month
    "openai_best": {
        "id": "openai/gpt-5",
        "name": "GPT-5",
        "provider": "OpenAI",
        "tier": "best",
        "context_window": "400K tokens",
        "notes": "OpenAI's most advanced model, major improvements in reasoning & code quality",
        "available": True,
    },
    "openai_budget": {
        "id": "openai/gpt-5-mini",
        "name": "GPT-5 Mini",
        "provider": "OpenAI",
        "tier": "budget",
        "context_window": "400K tokens",
        "notes": "Compact GPT-5 for lighter reasoning, reduced latency & cost, 1M free BYOK/month",
        "available": True,
    },
    
    # Claude (Anthropic) - 1M free BYOK requests per month
    "claude_best": {
        "id": "anthropic/claude-sonnet-4.5",
        "name": "Claude Sonnet 4.5",
        "provider": "Anthropic",
        "tier": "best",
        "context_window": "1M tokens",
        "notes": "Most advanced Sonnet, SOTA on coding & agentic workflows (SWE-bench leader)",
        "available": True,
    },
    "claude_budget": {
        "id": "anthropic/claude-opus-4.1",
        "name": "Claude Opus 4.1",
        "provider": "Anthropic",
        "tier": "budget",
        "context_window": "200K tokens",
        "notes": "Flagship model, 74.5% on SWE-bench, extended thinking (64K), 1M free BYOK/month",
        "available": True,
    },
    
    # Google (Gemini) - 1M free BYOK requests per month
    "google_best": {
        "id": "google/gemini-2.5-pro",
        "name": "Gemini 2.5 Pro",
        "provider": "Google",
        "tier": "best",
        "context_window": "1M tokens",
        "notes": "SOTA reasoning model with thinking capability, #1 on LMArena leaderboard",
        "available": True,
    },
    "google_budget": {
        "id": "google/gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "provider": "Google",
        "tier": "budget",
        "context_window": "1M tokens",
        "notes": "Workhorse model with thinking capability, optimized for speed & cost",
        "available": True,
    },
}


def get_model_by_key(key: str):
    """Get model config by key"""
    return MODELS.get(key)


def get_model_id(key: str):
    """Get just the model ID string"""
    model = MODELS.get(key)
    return model["id"] if model else None


def get_available_models():
    """Get only models marked as available"""
    return {k: v for k, v in MODELS.items() if v.get("available", True)}


def get_best_models():
    """Get all 'best' tier models"""
    return {k: v for k, v in MODELS.items() if v["tier"] == "best"}


def get_budget_models():
    """Get all 'budget' tier models"""
    return {k: v for k, v in MODELS.items() if v["tier"] == "budget"}


def get_models_by_provider(provider: str):
    """Get models from a specific provider"""
    return {k: v for k, v in MODELS.items() if v["provider"].lower() == provider.lower()}


def list_all_models():
    """Print formatted list of all models"""
    print("\n" + "="*70)
    print("Configured Models (8 total)")
    print("="*70)
    
    providers = {}
    for key, model in MODELS.items():
        provider = model["provider"]
        if provider not in providers:
            providers[provider] = []
        providers[provider].append((key, model))
    
    for provider, models in sorted(providers.items()):
        print(f"\n🏢 {provider}")
        print("-" * 70)
        for key, model in models:
            tier_emoji = "🔥" if model["tier"] == "best" else "💰"
            print(f"\n  {tier_emoji} {model['name']} ({model['tier']})")
            print(f"     Key: {key}")
            print(f"     ID: {model['id']}")
            print(f"     Context: {model['context_window']}")
            print(f"     Notes: {model['notes']}")


if __name__ == "__main__":
    list_all_models()

