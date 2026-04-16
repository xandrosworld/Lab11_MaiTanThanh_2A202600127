# Day 11 - Guardrails, HITL, and Responsible AI

This repository contains:

- the completed Day 11 lab in `src/`
- a production-style Assignment 11 defense-in-depth pipeline in `src/production/pipeline.py`
- grading artifacts in `artifacts/assignment/`
- the final individual report in `reports/Mai_Tan_Thanh_Assignment11_Report.md`

## What Was Implemented

### Lab tasks

The Day 11 lab TODOs were completed across:

- `src/attacks/attacks.py`
- `src/guardrails/input_guardrails.py`
- `src/guardrails/output_guardrails.py`
- `src/guardrails/nemo_guardrails.py`
- `src/testing/testing.py`
- `src/hitl/hitl.py`

These modules cover:

- adversarial prompt design
- AI-generated red teaming
- regex-based prompt injection detection
- topic filtering
- input and output guardrail plugins
- output redaction
- LLM-as-Judge
- before/after security testing
- HITL confidence routing

### Assignment 11 production pipeline

The final assignment solution is implemented in:

- `src/production/pipeline.py`

It includes:

1. `Rate Limiter`
2. `Input Guardrails`
3. `Session Anomaly Detector` as a bonus sixth safety layer
4. `Output Guardrails`
5. `LLM-as-Judge`
6. `Audit Log`
7. `Monitoring & Alerts`

## Final Results

Running the assignment pipeline with:

```bash
python src/main.py --part 5
```

produced these results:

- Safe queries: `5/5` passed
- Attack queries: `7/7` blocked
- Rate limiting: `10` allowed, `5` blocked
- Edge cases: `5/5` blocked
- Bonus anomaly demo: `4/4` blocked
- Audit log: `36` entries

## Repository Structure

```text
Day-11-Guardrails-HITL-Responsible-AI-main/
├── artifacts/
│   └── assignment/
│       ├── audit_log.json
│       ├── output_redaction_demo.json
│       └── results_summary.json
├── notebooks/
├── reports/Mai_Tan_Thanh_Assignment11_Report.md
├── src/
│   ├── agents/
│   ├── attacks/
│   ├── core/
│   ├── guardrails/
│   ├── hitl/
│   ├── production/
│   ├── testing/
│   └── main.py
├── assignment11_defense_pipeline.md
├── requirements.txt
├── requirements-nemo.txt
└── README.md
```

## Setup

### Core requirements

```bash
pip install -r requirements.txt
```

### Optional NeMo Guardrails support

NeMo is optional in this repo. If you want to try Part 2C locally:

```bash
pip install -r requirements-nemo.txt
```

The NeMo config in `src/guardrails/nemo_guardrails.py` was updated to use the
`google_genai` backend and was verified locally with:

```bash
python src/guardrails/nemo_guardrails.py
```

On Windows, installing `nemoguardrails` may require Microsoft Visual C++ Build Tools
because one of its dependencies (`annoy`) compiles a native extension.

### API key

Set a Gemini API key before running any model-backed part:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

On Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```

## How To Run

From the project root:

```bash
cd src
python main.py --part 1    # Attacks
python main.py --part 2    # Guardrails
python main.py --part 3    # Testing pipeline
python main.py --part 4    # HITL design
python main.py --part 5    # Assignment 11 production pipeline
```

You can also run the assignment pipeline directly:

```bash
python src/production/pipeline.py
```

## Important Output Files

The main grading artifacts are:

- `artifacts/assignment/audit_log.json`
- `artifacts/assignment/results_summary.json`
- `artifacts/assignment/output_redaction_demo.json`
- `reports/Mai_Tan_Thanh_Assignment11_Report.md`

## Notes

- The default `python src/main.py` flow keeps the original lab behavior and runs Parts `1-4`.
- The assignment submission flow is `python src/main.py --part 5`.
- NeMo support is optional because the assignment allows a pure Python solution.
- `TODO 9` now runs locally via `python src/guardrails/nemo_guardrails.py` after installing `requirements-nemo.txt`.

## References

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [AI Safety Fundamentals](https://aisafetyfundamentals.com/)
