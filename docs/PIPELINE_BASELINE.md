# BASELINE PIPELINE (Simple Prompting)

## Step 1: Generate Predictions (YOUR MACHINE)
```bash
python3 testing/baseline_all_models.py
```

**What happens:**
1. Loads SWE-bench Lite dataset (300 problems)
2. For each of 8 models:
   - Sends problem to OpenRouter API
   - Gets back a patch (single-pass)
   - Saves to testing/baseline_MODEL_50problems.jsonl
3. Takes 4-6 hours, costs ~$15

**Location**: Your laptop
**CPU**: <1% (just HTTP requests)
**Files created**: 
  - testing/baseline_grok_best_50problems.jsonl
  - testing/baseline_claude_best_50problems.jsonl
  - etc. (8 files)

## Step 2: Submit to Cloud Evaluation (SB-CLI)
```bash
export SWEBENCH_API_KEY=swb_...
sb-cli submit swe-bench_lite test \
  --predictions_path testing/baseline_claude_best_50problems.jsonl \
  --run_id baseline_claude_best
```

**What happens:**
1. Uploads your predictions to SWE-bench servers
2. THEIR servers:
   - Build Docker containers
   - Clone repos at correct commits
   - Apply your patches
   - Run test suites
   - Check FAIL_TO_PASS and PASS_TO_PASS
3. Takes 2-5 minutes per problem
4. FREE (but quota limited)

**Location**: SWE-bench cloud (Princeton servers)
**Your CPU**: 0% (nothing running locally)

## Step 3: Get Results
```bash
sb-cli get-report swe-bench_lite test baseline_claude_best
```

**Output:**
```
Resolved: 6% (3/50)
Cost: $0 (evaluation is free)
```

**Files created**:
  - sb-cli-reports/baseline_claude_best.json

---

## TOTAL PIPELINE:
```
[Your Machine]              [SB-CLI Cloud]          [Your Machine]
     ↓                           ↓                       ↓
Generate → Upload → → → Evaluate → → → Download Results
(4-6hrs)  (instant)      (2-5min)          (instant)
($15)     (free)         (free)            (free)
```
