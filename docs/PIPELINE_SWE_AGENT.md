# SWE-AGENT PIPELINE (Full Agentic)

## Step 1: Run SWE-Agent (YOUR MACHINE + MODAL CLOUD)
```bash
source swe_venv/bin/activate
cd SWE-agent

python -m sweagent run-batch \
  --config config/default.yaml \
  --agent.model.name "openrouter/anthropic/claude-opus-4.1" \
  --agent.model.per_instance_cost_limit 10.00 \
  --instances.type swe_bench \
  --instances.subset lite \
  --instances.split test \
  --instances.slice 50:60 \
  --instances.deployment.type=modal \
  --num_workers 2
```

**What happens:**

### 1A. Your Machine (Orchestrator)
- Loads SWE-bench problems
- Manages workflow
- Calls OpenRouter for LLM responses
- **CPU**: ~1% (just orchestration)

### 1B. Modal Cloud (Agent Runtime)
For EACH problem, Modal containers:

**Container Setup** (~2 min first time):
1. Pull SWE-bench Docker image for that repo
2. Clone repo at exact commit
3. Install dependencies

**Agent Loop** (~3-10 min per problem):
1. **Read files** - Agent browses repository
   ```
   🤖 → "Let me find the relevant code..."
   📂 → ls, cat, grep commands
   ```

2. **Create test script** - Agent writes reproduction
   ```
   🤖 → "I'll create a test to verify the bug..."
   📝 → Creates test_issue.py (200+ lines)
   🏃 → Runs: python test_issue.py
   ```

3. **Write fix** - Agent edits source files
   ```
   🤖 → "Now I'll fix the issue..."
   ✏️ → Edits django/contrib/syndication/views.py
   ```

4. **Verify** - Agent re-runs tests
   ```
   🏃 → python test_issue.py
   ✅ → "Tests pass! Submitting..."
   ```

5. **Submit** - Agent calls submit command
   ```
   git diff > patch
   ```

**Multiple API calls per problem**: 20-100 calls
**Cost per problem**: $9.64 average
**Location**: Modal cloud containers (Linux x86_64)

## Step 2: Extract Predictions (YOUR MACHINE)
```bash
# SWE-agent auto-saves to:
SWE-agent/trajectories/.../preds.json
```

**Files created**:
- Individual .traj files (agent's full conversation, 2-3MB each!)
- .patch files (the actual code changes)
- preds.json (consolidated predictions)

## Step 3: Evaluate (MODAL CLOUD - Different Containers)
```bash
python3 -m swebench.harness.run_evaluation \
  --dataset_name princeton-nlp/SWE-bench_Lite \
  --predictions_path preds.json \
  --run_id eval_name \
  --modal true \
  --max_workers 3
```

**What happens:**

### On Modal (NEW containers):
For each prediction:
1. **Build container** (~2 min)
   - Pull base image
   - Install dependencies
2. **Apply patch** (~10 sec)
   - git apply the patch
3. **Run tests** (~1-3 min)
   - Run FAIL_TO_PASS tests (should now pass)
   - Run PASS_TO_PASS tests (should still pass)
4. **Report results**
   - resolved: True/False

**Location**: Modal cloud
**Your CPU**: <1% (just monitoring)
**Time**: ~5-7 min per problem
**Cost**: ~$5-10 Modal credits (separate from OpenRouter)

## Step 4: Get Results (YOUR MACHINE)
```bash
# Results saved in:
logs/run_evaluation/eval_name/
```

**Output**:
```
Resolved: 33% (3/9)
```

---

## TOTAL PIPELINE:
```
[Your Machine]         [Modal - Agent Runtime]        [Modal - Evaluation]      [Your Machine]
      ↓                         ↓                             ↓                        ↓
  Orchestrate → → SWE-Agent works in cloud → → Modal evaluates → → Download Results
   (~1% CPU)      (browse, test, fix, iterate)    (apply, test)         (instant)
   (instant)         (3-10 min/problem)            (5-7 min/problem)     (free)
   (free)            ($9.64/problem)               ($0.50-1/problem)     (free)
```

## KEY DIFFERENCES FROM BASELINE:

| Aspect | Baseline | SWE-Agent |
|--------|----------|-----------|
| **Generation Location** | Your machine | Modal cloud |
| **Can Browse Code** | ❌ No | ✅ Yes |
| **Can Run Tests** | ❌ No | ✅ Yes |
| **Iteration** | ❌ Single-pass | ✅ Multi-turn (20-100 calls) |
| **Test Creation** | ❌ No | ✅ Yes (200+ line scripts) |
| **API Calls** | 1 per problem | 20-100 per problem |
| **Time** | 30 sec/problem | 3-10 min/problem |
| **Your CPU** | <1% | <1% (Modal does work) |
| **Cost** | $0.03/problem | $10-11/problem total |
