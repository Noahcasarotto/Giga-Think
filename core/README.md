# Core Modules

Reusable components for the Giga-Think system.

## Modules

- `models.py` - Configuration for 8 models across 4 providers
- `client.py` - OpenRouter API client wrapper
- `prompts.py` - Prompt templates (to be added)

## Usage

```python
from core.models import MODELS
from core.client import OpenRouterClient

# Get a model config
model = MODELS["claude_best"]

# Make API calls
client = OpenRouterClient()
response = client.complete(
    model_id=model["id"],
    messages=[{"role": "user", "content": "Hello"}]
)
```
