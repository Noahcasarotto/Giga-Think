# Giga-Think Architecture

## 🏗️ Clean Modular Structure

```
Giga-Think/
│
├── core/                          # ⚙️ Reusable Core Components
│   ├── models.py                 # 8 model configurations
│   ├── client.py                 # OpenRouter API wrapper
│   └── README.md
│
├── baselines/                     # 📊 Baseline Testing
│   ├── simple_baseline.py        # Single-pass (6% success)
│   ├── multi_model_baseline.py   # All 8 models in parallel
│   └── README.md
│
├── reasoning/                     # 🧠 IMO Reasoning (TO BUILD)
│   ├── solver.py                 # Rigor-first solver
│   ├── verifier.py               # Strict verification
│   ├── corrector.py              # Correction loop
│   ├── pipeline.py               # Full reasoning flow
│   └── README.md
│
├── evaluation/                    # 🧪 Evaluation Tools
│   ├── swe_bench.py              # SWE-bench integration
│   ├── modal_runner.py           # Modal execution
│   └── README.md
│
├── scripts/                       # 🛠️ Utility Scripts
│   ├── run_swe_agent.sh          # Run SWE-agent
│   ├── show_results.sh           # View benchmarks
│   ├── evaluate_quality.py       # Quality analysis
│   └── README.md
│
├── docs/                          # 📚 Documentation
│   ├── ARCHITECTURE.md           # This file
│   ├── RESULTS.md                # Benchmark results
│   ├── PIPELINE_BASELINE.md      # Baseline approach
│   └── PIPELINE_SWE_AGENT.md     # SWE-agent approach
│
├── SWE-agent/                     # 🤖 SWE-Agent Framework
│   ├── config/                   # Agent configurations
│   ├── tools/                    # Agent tools
│   └── .env                      # Agent keys
│
├── testing/                       # 🧪 Test Data & Scripts
│   ├── swe_bench_baseline.py     # Core testing
│   ├── *.jsonl                   # Prediction files
│   └── README.md
│
├── .env                           # 🔑 API Keys
├── requirements.txt               # 📦 Dependencies
└── README.md                      # 📖 Main docs
```

## 🔄 Data Flow

### Baseline Pipeline
```
Problem → OpenRouter (1 call) → Patch → sb-cli eval → 6%
```

### SWE-Agent Pipeline  
```
Problem → Modal (agent: browse, test, fix) → Patch → Modal eval → 33%
```

### IMO Reasoning Pipeline (To Build)
```
Problem → Solver → Self-improve → Verify → Correct → Re-verify → Solution
```

## 🎯 Design Principles

1. **Modular**: Each component is independent and reusable
2. **Testable**: Easy to test individual components
3. **Documented**: README in every directory
4. **Scalable**: Easy to add new models, evaluations, reasoning strategies
5. **Cost-Aware**: Track costs at every step

## 🚀 Adding IMO Reasoning

Clean interfaces ready:
```python
from core.client import OpenRouterClient
from reasoning.pipeline import IMOPipeline

pipeline = IMOPipeline(
    model="claude_opus_41",
    max_iterations=5,
    verification_passes=5
)

result = pipeline.solve(problem)
```

## 💾 Version Control

- **Main branch**: Clean, organized, working
- **Backup branch**: `backup-working-system` (pre-cleanup)
- **Safe to experiment**: Can always revert!
