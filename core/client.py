"""
OpenRouter client wrapper for unified model access.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenRouterClient:
    """Unified client for all OpenRouter models."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
    
    def complete(self, model_id, messages, max_tokens=4000, temperature=0.1):
        """Make a completion request."""
        response = self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Giga-Think",
            }
        )
        return response
    
    def get_response_text(self, response):
        """Extract text from response."""
        return response.choices[0].message.content
    
    def get_tokens_used(self, response):
        """Get token usage from response."""
        return response.usage.total_tokens
