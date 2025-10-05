# IMO Reasoning Pipeline

Implementation of the IMO-level reasoning system from the paper.

## Components (To Be Built)

- `solver.py` - Rigor-first solver with structured output
- `verifier.py` - Strict verification with bug reports  
- `corrector.py` - Correction loop
- `pipeline.py` - Full solve → verify → correct → iterate

## Target

Improve from 33% (baseline SWE-agent) to 50-70%+ with:
- Multi-turn verification
- Self-improvement passes
- Structured feedback loops
- Multi-verification gates
