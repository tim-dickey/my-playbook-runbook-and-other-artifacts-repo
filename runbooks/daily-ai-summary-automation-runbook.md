# Runbook: Daily AI Summary — GitHub Actions Automation

## Overview

This runbook documents the setup and operation of the automated daily AI summary pipeline. Every morning at **8:05 AM CDT**, a GitHub Actions workflow calls the Perplexity API to generate a structured AI news briefing and commits it to `daily-ai-summary/YYYY/MM/YYYY-MM-DD.md`.

---

## Architecture

```
GitHub Actions (cron: 8:05 AM CDT)
    └── generate_daily_ai_summary.py
            └── Perplexity API (sonar-pro, search_recency_filter: day)
                    └── daily-ai-summary/YYYY/MM/YYYY-MM-DD.md
                            └── git commit + push (github-actions[bot])
```

---

## One-Time Setup

### Step 1 — Get a Perplexity API Key

1. Go to [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Generate a new API key.
3. Copy the key — you will not see it again.

### Step 2 — Add the Secret to GitHub

1. Go to your repository: `Settings → Secrets and variables → Actions`
2. Click **New repository secret**
3. Name: `PERPLEXITY_API_KEY`
4. Value: paste your API key
5. Click **Add secret**

> ⚠️ The workflow will silently fail if this secret is missing or expired.

---

## Files

| File | Purpose |
|---|---|
| `.github/workflows/daily-ai-summary.yml` | GitHub Actions workflow — schedule + steps |
| `scripts/generate_daily_ai_summary.py` | Python script — calls Perplexity API, writes markdown |
| `runbooks/daily-ai-summary-automation-runbook.md` | This runbook |

---

## Schedule

- **Cron**: `5 13 * * *` (UTC) = **8:05 AM CDT** daily
- CDT is UTC−5. Adjust the cron UTC hour if your timezone offset changes (e.g. CST = UTC−6 → use `5 14 * * *`).

---

## Manual Trigger

To run on demand without waiting for the schedule:

1. Go to **Actions** tab in the repository
2. Select **Daily AI Summary** workflow
3. Click **Run workflow → Run workflow**

---

## Monitoring & Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Workflow not running | Cron hasn't fired yet | Trigger manually to test |
| `401 Unauthorized` from API | Expired or missing API key | Rotate key in repo Secrets |
| `No summary file found` | Script crashed before writing | Check Actions logs for Python traceback |
| Empty or garbled markdown | API returned partial response | Check `max_tokens` limit; rerun manually |
| File already exists | Same date rerun | Git diff check skips duplicate commits — safe |

---

## Cost Estimate

- Perplexity `sonar-pro` API: ~$0.005–$0.02 per request depending on token usage
- 365 runs/year ≈ **$2–$7/year** estimated
- GitHub Actions: free for public repos; 2,000 min/month free for private repos

---

## Updating the Prompt

To change what the summary covers, edit the `SYSTEM_PROMPT` or `USER_PROMPT` strings in `scripts/generate_daily_ai_summary.py` and commit the change. The next scheduled run will use the updated prompts.

---

*Last updated: 2026-09-21*
