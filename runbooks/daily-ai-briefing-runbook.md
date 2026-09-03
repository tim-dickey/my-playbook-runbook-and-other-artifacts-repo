# Daily AI Briefing Runbook

## Metadata

| Field | Value |
|---|---|
| **Author** | Tim Dickey |
| **Last Updated** | 2026-09-03 |
| **Status** | Active |
| **Audience** | Self (or any agent/assistant producing the morning AI news briefing) |
| **Estimated Duration** | 15–25 minutes |

---

## Overview

This runbook produces a recurring, structured daily briefing on global AI news — business, research/R&D, newly published papers, engineering developments, and materials science relevant to AI hardware — filtered through a local-agent and homelab lens. Each run produces one dated Markdown note using `templates/daily-ai-briefing-template.md`.

## Prerequisites

- [ ] Access to this repository (write access to create a new note file, or a PR workflow)
- [ ] Web/search access (search engine or research assistant with web search)
- [ ] `templates/daily-ai-briefing-template.md` present in this repo
- [ ] A `notes/` directory (or agreed destination) for dated briefing files

## Trigger / When to Use This Runbook

Run each morning (or on demand) when a fresh AI news summary is needed. Default cadence: daily, once per morning, covering the prior 24 hours since the last briefing.

## Procedure

### Step 1 — Create today's note from the template

```bash
cp templates/daily-ai-briefing-template.md notes/ai-briefing-$(date +%F).md
```

**Expected output:** a new dated file, e.g. `notes/ai-briefing-2026-09-04.md`, with all template sections intact and blank.

### Step 2 — Gather business & industry news

Search for AI business news dated to today (funding rounds, earnings, product launches, M&A, policy-adjacent business moves). Populate Section 2 of the note with 3–6 items, each tagged with why it matters for local-agent/homelab decisions.

**Expected output:** a filled Section 2 table with source links.

### Step 3 — Pull latest arXiv cs.AI submissions

```text
Check: https://arxiv.org/list/cs.AI/recent
Check: https://arxiv.org/list/cs.AI/current
```

Filter titles/abstracts for relevance to: agent architectures, orchestration frameworks, evaluation harnesses, memory systems, quantization, on-device/edge inference. Populate Section 3 with 3–8 papers.

**Expected output:** a filled Section 3 table with arXiv links and one-line summaries.

### Step 4 — Check Hugging Face trending

```text
Check: https://huggingface.co/papers/trending
Check: https://huggingface.co/models?sort=trending
```

Note any new or updated models runnable locally (Ollama, llama.cpp, vLLM) with parameter counts and quantization options. Populate Section 4.

**Expected output:** a filled Section 4 table.

### Step 5 — Check hardware and materials science feeds

```text
Check: https://www.datacenterknowledge.com/data-center-hardware
Check: https://www.techpowerup.com/review/future-hardware-releases/
Check: NVIDIA / AMD / Intel newsrooms
Check: NIST AIMS (AI for Materials Science) event page and related coverage
```

Prioritize items relevant to NPU/GPU/CPU/unified-memory inference, cooling, interconnects, and materials breakthroughs that affect future accelerator cost/performance. Populate Section 5.

**Expected output:** a filled Section 5 table.

### Step 6 — Check regulation and governance feeds

```text
Check: EU AI Act implementation tracker
Check: https://www.whitehouse.gov/presidential-actions/
Check: relevant state AI legislation trackers (e.g., Colorado, California, Texas)
```

Populate Section 6 with developments that could affect model deployment, data handling, or agent autonomy in regulated or enterprise contexts.

**Expected output:** a filled Section 6 table.

### Step 7 — Write engineering follow-ups and top takeaways

Synthesize Sections 1 and 7: identify the 3 most consequential items overall, and list concrete, testable follow-ups for this homelab (e.g., "pull model X and benchmark on Pangolin15", "test new quantization format in llama.cpp").

### Step 8 — Log sources and commit

Fill Section 8 with every feed/query checked, even null results. Commit the dated note.

```bash
git add notes/ai-briefing-$(date +%F).md
git commit -m "Add: AI briefing $(date +%F)"
```

**Expected output:** a new commit containing the completed daily briefing note.

## Verification

- [ ] All 8 template sections are filled (no placeholder text remains)
- [ ] Every claim has a source link
- [ ] At least one item in Section 7 is a concrete, actionable homelab task
- [ ] File is committed and named `ai-briefing-YYYY-MM-DD.md`

## Rollback / Recovery

1. If a section cannot be completed (e.g., a feed is down), mark it explicitly as "No update found" rather than leaving it blank — do not fabricate entries.
2. If the note was committed with errors, amend or follow up with a correction commit; do not silently rewrite history on a shared branch.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| arXiv listing page is stale or empty | arXiv publishing delay (common on weekends/holidays) | Note the gap in Section 8 and check `/current` instead of `/recent` |
| Hugging Face trending page shows unrelated content | Trending list reflects general popularity, not agent-specific relevance | Cross-check with targeted search for "agent", "memory", "quantization" model cards |
| Hardware/regulation feed paywalled or blocked | Source-specific access restriction | Substitute an equivalent secondary source and note the substitution |
| Duplicate item across sections | Item spans both business and hardware (e.g., a chip launch announcement) | Keep in the most specific section only; cross-reference by name in the other |

## References

- [Daily AI briefing template](../templates/daily-ai-briefing-template.md)
- [Generic runbook template](../templates/runbook-template.md)
