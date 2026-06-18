# WeRSS MP Briefing Skill

This repository contains the `werss-mp-briefing` Codex skill for generating D91 `/mp` WeRSS morning and evening article briefings.

## Purpose

- Generate fixed-window WeRSS reports for the D91 `/mp` 新增文章报告 module.
- Keep website JSON and Obsidian Markdown archive output synchronized.
- Preserve original article URLs for every used source.
- Keep summaries objective, evidence-grounded, and free of investment-action wording.
- Provide a small project surface for future prompt, contract, and validator tuning.

## Structure

- `SKILL.md`: Codex skill entrypoint and execution contract.
- `references/output_contract.md`: JSON and Markdown output schema.
- `references/d91_integration.md`: D91 backend/frontend integration notes.
- `scripts/collect_werss_window.py`: collect WeRSS articles by `created_at` window.
- `scripts/validate_report.py`: validate report JSON source coverage, wording, and number grounding.
- `agents/openai.yaml`: skill interface metadata.
- `examples/sample_report.json`: minimal validator fixture.

## Validation

Run the included validator against the sample payload:

```bash
python3 scripts/validate_report.py examples/sample_report.json
```

Check Python syntax without writing cache files into the source tree:

```bash
PYTHONPYCACHEPREFIX=/tmp/werss-mp-briefing-pycache python3 -m py_compile scripts/collect_werss_window.py scripts/validate_report.py
```

## Install Locally

After editing this repository, sync it into the local Codex skill directory:

```bash
rsync -a --delete ./ ~/.codex/skills/werss-mp-briefing/
```

Review `SKILL.md` and the two files under `references/` before changing report fields, generation prompts, validator rules, or D91 integration behavior.
