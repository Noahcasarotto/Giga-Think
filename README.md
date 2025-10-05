# Giga-Think

IMO-level reasoning system with comprehensive SWE-bench evaluation.

## 🎯 Project Status

### ✅ Complete & Working
- **8 Models** configured (Grok, GPT-5, Claude, Gemini via OpenRouter)
- **Baseline Pipeline**: 6% success (Claude Opus 4.1 best)
- **SWE-Agent Pipeline**: 33% success (5.5x improvement!)
- **Modal Cloud Integration**: Full evaluation without local Docker
- **400+ Problems Tested**: Comprehensive benchmarking

### ⏳ In Progress
- **IMO Reasoning Pipeline**: solve → verify → correct → iterate (Next phase)

## 📊 Benchmark Results

```
Baseline (Blind Patching):     6% (3/50)  - $0.03/problem
SWE-Agent (Full Agentic):     33% (3/9)   - $9.64/problem
Improvement:                   5.5x better (+27pp)
```

See [docs/RESULTS.md](docs/RESULTS.md) for full details.

## 🏗️ Project Structure

```
core/               # Reusable modules (models, client)
baselines/          # Baseline testing approaches  
reasoning/          # IMO reasoning pipeline (to build)
evaluation/         # Evaluation utilities
scripts/            # CLI tools
docs/               # Documentation
results/            # Archived benchmark results
SWE-agent/          # Full agentic framework
```

## 🚀 Quick Start

### Test Baseline
```bash
python3 -m baselines.simple_baseline
```

### Run SWE-Agent
```bash
source swe_venv/bin/activate
./scripts/run_swe_agent.sh
```

### View Results
```bash
./scripts/show_results.sh
```

## 📚 Documentation

- [Architecture Overview](docs/PIPELINE_SWE_AGENT.md)
- [Baseline Pipeline](docs/PIPELINE_BASELINE.md)
- [Results & Benchmarks](docs/RESULTS.md)

## 💰 Costs

- **OpenRouter API**: $0.03-10/problem (depending on approach)
- **Modal Cloud**: $0.50-1/problem (evaluation)
- **sb-cli**: FREE (quota-limited)

## 🔑 Setup

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - `OPENROUTER_API_KEY`
   - `SWEBENCH_API_KEY` (optional, for sb-cli)
3. Install: `pip install -r requirements.txt`

## 🎯 Next Phase: IMO Reasoning

Build the verification and correction loops to improve 33% → 50-70%+

---

**Repository**: https://github.com/Noahcasarotto/Giga-Think
