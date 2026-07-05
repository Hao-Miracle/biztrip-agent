---
name: "agent-report"
description: "Agent-mode full pipeline: LLM classify + extract + aggregate trips → Excel. Auto-fallback to rule engine without API key. Invoke when user wants smart trip report with AI enhancement."
---

# Agent Report

Full pipeline with LLM enhancement. Automatically detects API key availability and falls back to rule engine.

## Usage

```bash
python3 phase2/agent_report.py
```

## Modes

| Mode | Condition | Behavior |
|------|-----------|----------|
| 🧠 AI Enhanced | `DEEPSEEK_API_KEY` configured | LLM classify + LLM extract + LLM aggregation |
| 📋 Rule Engine | No API key | Domain match + regex (same as Phase 1) |

## Pipeline

```
1. IMAP connect + date filter
2. LLM classify each email → rule fallback if low confidence
3. LLM extract per category → rule fallback if quality < 50%
4. LLM aggregate trips by time + destination
5. Generate Excel (overview + detail + vendor sheets)
```

## Excel Output

- **Sheet 1: 报销总览** — Trip summary + category breakdown + total card
- **Sheet 2: 费用明细** — All records sorted by date, includes extraction method column
- **Sheet 3: 按供应商** — By vendor/platform

## Prerequisites

- `QQ_EMAIL` + `QQ_AUTH_CODE` in `.env` (required)
- `DEEPSEEK_API_KEY` in `.env` (optional, enables AI mode)
- `openai` package installed
