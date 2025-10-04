# Giga-Think

An implementation of IMO-level reasoning system based on iterative verification and refinement.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your OpenRouter API key:
```bash
cp .env.example .env
```

3. Get your OpenRouter API key:
   - Visit https://openrouter.ai/keys
   - Sign up or log in
   - Create a new API key
   - Add it to `.env` as `OPENROUTER_API_KEY`

## Testing OpenRouter Connection

Test the API and see available models:

```bash
python test_openrouter.py
```

This will:
- Verify your API key works
- Show recommended models for math reasoning
- Optionally test a model with a simple problem

## Architecture

Based on the solve → self-improve → verify → correct → re-verify loop:
1. **Solver** - Rigor-first prompting with structured output
2. **Self-improvement** - Inject additional reasoning budget
3. **Verifier** - Strict grader producing bug reports
4. **Correction loop** - Address feedback iteratively
5. **Multi-verification acceptance** - 5x independent verification before accepting

## Project Status

- [ ] API connections and basic testing
- [ ] Solver prompt implementation
- [ ] Verifier prompt implementation
- [ ] Self-improvement pass
- [ ] Correction loop
- [ ] Multi-verification gate
- [ ] Parallel attempt orchestration

