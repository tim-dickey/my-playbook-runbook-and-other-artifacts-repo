# Cline + Ollama Runbook: A Local Coding-Agent Alternative to Hosted Services

This runbook explains how to assemble a local coding-agent workflow with **Cline**, **Ollama**, and a VS Code-compatible IDE. It is designed for developers who want a capable local alternative for repository analysis, small coding tasks, and controlled automation—reducing routine cloud-agent usage and subscription spend without pretending that every task should be handed to a small local model.

The basic idea is simple:

```text
VS Code-compatible IDE
        │
        ├── Cline: agent loop, tools, plan/act workflow
        ├── Omni Chat Provider: optional local chat lane
        └── Ollama: local model server at http://localhost:11434
                    │
                    └── Local coding/planning models
```

A local agent works best when it is treated as a capable junior developer with a very fast terminal, not as an unattended production deployment system.

## What this setup can replace

A local Cline + Ollama stack can handle many subscription-consuming tasks:

- Repository orientation and architecture summaries
- Explaining files, errors, tests, and configuration
- Small, bounded refactors
- Generating tests, documentation, and commit-message drafts
- Searching a repository and proposing low-risk improvements
- Running approved read-only commands and tests
- Preparing a plan before a hosted agent tackles a harder task

Keep a hosted model or premium coding agent for high-consequence changes, difficult multi-file implementation, ambiguous requirements, security-sensitive work, and tasks where speed matters more than local cost control.

## Required components

| Component | Purpose | Minimum recommendation |
|---|---|---|
| VS Code-compatible IDE | Editor and extension host | VS Code, VSCodium, Windsurf/Cognition-compatible build, or another compatible editor |
| Cline extension | Agent interface, tools, Plan/Act workflow | Install the official Cline extension from the editor marketplace |
| Ollama | Local model runtime and HTTP server | Current Ollama release for Windows, Linux, or macOS |
| Git | Repository discovery, checkpoints, history | Git installed and available in the IDE's terminal environment |
| Local model | Planning, coding, or review | Start with a 7B–14B model; use larger models only after basic stability is proven |
| Optional: Omni Chat Provider | Non-agent local chat in the IDE | Useful for code discussion while Cline remains the tool-using agent |

Ollama runs as a native Windows application and supports local GPU acceleration on supported NVIDIA and AMD Radeon configurations.[cite:121]

## Hardware sizing

Start with the hardware you already own. The most important resource is usually usable GPU memory or unified memory—not just CPU core count.

| Hardware profile | Practical local-agent model range | Suggested use |
|---|---|---|
| 16 GB system RAM, no useful GPU | 3B–7B | Chat, narrow file explanation, tiny read-only tasks |
| 32–64 GB system RAM or 8–12 GB VRAM | 7B–14B | Planning, repository search, small edits, tests |
| 64–96 GB RAM with a capable iGPU/eGPU/dGPU | 9B–35B depending on quantization and context | Strong local coding, architecture review, moderate agent tasks |
| 96 GB+ unified memory or 24 GB+ VRAM | 30B–70B class models, selectively | Deep analysis, reviews, higher-quality local generation |

Do not start by maximizing context. Context length increases KV-cache memory demand and can make a previously usable model slow or unstable. A practical rule: make a small model reliable at 16k context before increasing context or moving to a larger model.[cite:133]

### AMD Ryzen AI systems

AMD Ryzen AI chips may contain CPU, integrated GPU, and NPU resources. For the standard Cline → Ollama workflow, target the **GPU/eGPU** first. The NPU may be visible in Task Manager but does not automatically mean Ollama is using it. The Ryzen AI 9 HX 370, for example, advertises up to 50 NPU TOPS and up to 80 platform TOPS, but NPU integration depends on the inference runtime rather than on Cline itself.[cite:118]

## Install and verify Ollama

### Install

Install Ollama for the operating system, launch it once, and ensure its local service is running.

On Windows, open PowerShell and verify the service endpoint:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

A successful result shows locally installed models.

### Pull a starter model

Choose a model appropriate to available memory. Replace the model name below with one from the Ollama library or an internal standard:

```powershell
ollama pull <model-name>
ollama list
ollama run <model-name> "Reply with exactly: local model is ready."
```

### Verify active allocation

While an IDE task is generating, run:

```powershell
ollama ps
```

Inspect its processor/allocation output to determine whether the model is using GPU, CPU, or a combination. For Windows GPU troubleshooting, consult current Ollama Windows and GPU support documentation rather than assuming a particular AMD or NVIDIA device will be selected automatically.[cite:121]

## Choose model roles

Use different models for different jobs. This is usually more effective than selecting one “smartest” model and letting it play planner, executor, reviewer, and accidental intern simultaneously.

### Recommended role pattern

| Role | Characteristics | Typical model size | Cline mode |
|---|---|---:|---|
| Planner | Concise, reliable at decomposition and constraints | 7B–14B | Plan |
| Executor | Good tool calling, code changes, and test interpretation | 9B–30B | Act |
| Escalation coder | Better multi-file reasoning and implementation | 20B–35B+ | Act when needed |
| Reviewer | Strong architecture and critique, not necessarily tool-heavy | 20B–35B+ | Omni Chat or Plan |
| Fast utility model | Cheap explanation and small transformations | 3B–8B | Omni Chat |

### Example local model mapping

The following is an example, not a universal ranking:

```text
Plan: LFM 2.5 8B
Act: Ornith 1.5 9B
Escalation Act: Qwen3 Coder Agent / Qwen3 Coder 30B
Review: Ornith 1.5 35B
Fast chat: Llama 3.2 3B
```

A useful lesson from practical testing: a planning model can produce excellent short plans yet still be unreliable at repeated terminal/tool loops. If that happens, make it a **no-tools planner** and delegate all repository exploration and edits to the Act model.

## Configure Cline

1. Open Extensions in the IDE.
2. Install **Cline** from the marketplace.
3. Open the Cline panel from the Activity Bar.
4. Select the gear icon to open Cline settings.
5. Set the provider to **Ollama**.
6. Set the base URL to:

```text
http://localhost:11434
```

7. Choose an installed model.
8. Enable **Compact Prompt** if the option is available.
9. Begin with conservative tool approvals.

Cline’s local-runtime workflow is: install a local runtime, start its server, select the corresponding provider in Cline settings, and choose a local model.[cite:135]

### Baseline Cline settings

| Setting | Starting value | Why |
|---|---:|---|
| Provider | Ollama | Native local model connection |
| Base URL | `http://localhost:11434` | Default local Ollama service endpoint |
| Context window | 16,384 | Good initial balance for local agent work |
| Request timeout | 120,000 ms | Allows cold model loads and slower local generation |
| Compact prompt | Enabled | Reduces avoidable token and context pressure |
| Auto-approve | Read and safe commands only | Preserves control while validating behavior |
| Checkpoints | Enabled for edit tasks; optional for read-only tests | Provides rollback when working in Git repositories |

Do not assume a model can support a chosen context window merely because its marketing page advertises one. Match Cline’s request context to the context Ollama is actually configured to serve.

## Plan and Act setup

Cline can use separate models for **Plan** and **Act** modes. This is useful for reducing cost and improving reliability.

### Plan mode

Use Plan for:

- Turning requirements into a short sequence of steps
- Listing assumptions and risks
- Creating acceptance criteria
- Asking for a proposed file/change list before edits

For a smaller local planning model, avoid letting it conduct open-ended repository exploration. Supply known facts and request a plan only.

Example Plan prompt:

```text
Planning only. Do not call tools, run commands, read files, or ask follow-up questions.

Known facts:
- This is a Git repository.
- The task is read-only until explicitly approved.
- The goal is to identify runtime entry points and configuration files.

Create a three-step plan under 150 words. Include one validation command per step.
```

### Act mode

Use Act for:

- Reading files
- Executing approved terminal commands
- Searching the repository
- Editing files and running tests

For a new local executor model, validate one tool at a time. A narrow prompt is more diagnostic than “understand the repository and fix everything.”

Example Act prompt:

```text
Read-only validation task.

Run exactly one command:

git rev-parse --show-toplevel

Then report only the resulting repository root path.
Do not run any other commands. Do not modify files.
```

After that succeeds, test a bounded Git file-list query:

```text
Read-only validation task.

Run exactly this command:

git ls-files | Select-Object -First 80

Then summarize likely repository categories from that output only.
Do not read files, run additional commands, modify files, or ask follow-up questions.
```

## Configure Omni Chat Provider (optional)

Use Omni Chat Provider for a local chat lane beside Cline. It is useful for discussing code, drafting implementation ideas, and reviewing outputs without granting terminal or file-editing autonomy.

Open the editor’s User `settings.json` through the Command Palette:

```text
Preferences: Open User Settings (JSON)
```

Add one Ollama provider and one model array. Preserve existing settings; do not add a second outer JSON object.

```jsonc
{
  "omnichat.providers": [
    {
      "id": "ollama-local",
      "baseUrl": "http://localhost:11434",
      "apiMode": "ollama"
    }
  ],
  "omnichat.models": [
    {
      "id": "<planner-model-tag>",
      "provider": "ollama-local",
      "displayName": "Local Planner",
      "family": "planner",
      "context_length": 16384,
      "temperature": 0.3
    },
    {
      "id": "<coding-model-tag>",
      "provider": "ollama-local",
      "displayName": "Local Coding Model",
      "family": "code",
      "context_length": 32768,
      "temperature": 0.2
    }
  ]
}
```

Replace placeholders with exact names from `ollama list`, including tags such as `:latest`, `:9b`, or quantization tags. Reload the IDE window after saving.

## Files to maintain

Keep the local-agent plumbing explicit and reproducible.

| File or location | Purpose | Notes |
|---|---|---|
| User `settings.json` | IDE-level Omni Chat configuration and other editor settings | Keep provider IDs and exact model tags here |
| Cline Settings | Provider, model, context, timeout, approval controls | Managed from the Cline panel rather than hand-authored JSON in most installations |
| Ollama Modelfile | Persistent model options such as `num_ctx` and temperature | Useful when a model needs a dedicated agent-oriented tag |
| `.cline/` or project instructions | Repository-specific Cline rules where supported | Store safe-command policy, test commands, and architecture notes |
| `AGENTS.md` | Cross-agent repository instructions | Useful for Cline, Devin, and other agent tooling where supported |
| `.gitignore` | Prevent checkpoints, logs, local secrets, and generated artifacts from being committed | Review before enabling broad write authority |

### Example Ollama Modelfile

```text
FROM <base-coding-model>
PARAMETER num_ctx 32768
PARAMETER temperature 0.2
PARAMETER top_p 0.9
```

Create an agent-specific local tag:

```powershell
ollama create <coding-model>-agent -f Modelfile
ollama list
```

Use a custom tag when you want Cline to consistently receive a particular context limit and sampling profile.

## Git and checkpoint readiness

Cline checkpoints are most useful when the opened folder is an actual Git repository root. Verify it from the IDE terminal:

```powershell
git rev-parse --show-toplevel
```

Expected behavior is a path to the repository root. If it fails:

1. Open the actual repository folder, not its parent directory.
2. Confirm `.git` exists or that the repository is a valid Git worktree.
3. Ensure Git is in the PATH inherited by the IDE.
4. Restart the IDE after installing or updating Git.

Disable checkpoints temporarily for read-only validation or when initialization is repeatedly slow. Re-enable them for edit tasks in a healthy Git repository; checkpoints provide a useful recovery boundary around agent changes. Cline tasks create checkpoints around file-changing work.[cite:92][cite:93]

## Safe operating pattern

### Phase 1: Read-only validation

Validate each component before letting an agent edit:

1. Confirm Ollama responds directly.
2. Confirm Cline can call Ollama.
3. Confirm Cline can execute one Git command.
4. Confirm Cline can read one file.
5. Confirm the model can summarize the result without extra tool calls.

### Phase 2: Small reversible edits

Use small changes first:

- Correct a documentation typo
- Add a unit test for an existing function
- Add a docstring
- Rename a local helper with test coverage
- Improve an error message

Require the agent to state the files it intends to change before it acts.

### Phase 3: Bounded implementation

For a real task:

1. Ask the Plan model for a short no-tools plan.
2. Review the plan.
3. Switch to Act mode.
4. Require one logical step at a time.
5. Review diffs after every meaningful change.
6. Run only known-safe tests.
7. Commit only after human review.

### Tool approvals

Start with:

```text
Auto-approve: Read, Safe Commands
```

Do not enable unrestricted auto-approval or “YOLO” behavior while models and instructions are still being tested. Cline tools can be configured to require approval; that review boundary is valuable for local agents just as it is for hosted ones.[cite:134]

## Troubleshooting

### Ollama request timed out

**Symptom:** Cline displays an Ollama timeout, often after 30 seconds.

**Likely causes:** Cold model load, a model that is too large, overly large context, CPU fallback, or a timeout too short for local hardware.

**Fix:**

1. Lower Cline context to 16,384.
2. Raise the Cline request timeout to 120,000 ms.
3. Test the model directly:

```powershell
ollama run <model-name> "Reply with exactly: Ollama is responding."
```

4. Use `ollama ps` during generation to inspect allocation.
5. Test a smaller model before diagnosing Cline itself.

### Context window is slow or unstable

**Symptom:** The model loads but becomes very slow, times out, or spills into system memory.

**Fix:**

- Reduce context before replacing hardware.
- Match Cline’s context setting to the model’s Ollama `num_ctx` capability.
- Use 16k as a stable initial baseline.
- Increase to 32k only after confirming responsiveness.
- Use 64k only when the model, GPU/unified memory, and task genuinely require it.

Large contexts materially increase memory allocation and can degrade GPU residency.[cite:133]

### Checkpoint initialization takes too long

**Symptom:** Cline warns that checkpoints are taking too long to initialize.

**Fix:**

- Confirm the open folder is a Git root with `git rev-parse --show-toplevel`.
- Avoid opening a giant parent folder containing many repositories.
- Disable checkpoints for read-only discovery tasks.
- Check for slow Git hooks, antivirus scanning, network drives, or enormous generated directories.
- Re-enable checkpoints before edit-heavy tasks once the repository is healthy.

### Cline repeats commands or ignores a tool budget

**Symptom:** The agent repeatedly runs a successful command, rechecks Git root, or continues searching after being told to stop.

**Cause:** Usually a model tool-use/reasoning limitation, sometimes worsened by noisy terminal wrapper output.

**Fix:**

1. Start a **new Cline task**; do not keep contaminated conversation history.
2. Use a stronger Act model.
3. Give one exact command and an explicit stop condition.
4. State prohibited actions by name.
5. Use read-only, single-command tests before broader tasks.

Example repair prompt:

```text
Run exactly this command once:

git ls-files | Select-Object -First 40

After it completes, stop and provide a five-bullet summary from that output only.
Do not run git rev-parse. Do not read files. Do not call any other tool.
```

If a Plan model loops on tools, keep that model for no-tools planning and move repository exploration into Act mode.

### The model says a successful Git command failed

**Symptom:** `git rev-parse --show-toplevel` returns a valid path, but the model claims the directory is not a Git repository.

**Fix:**

- Trust the command’s exit/output over the model’s narration.
- Start a new task and provide the verified Git root as a known fact.
- Do not ask the model to re-run the same command.
- Switch models if it repeats the contradiction.

### GPU is not being used

**Symptom:** Slow generation; Task Manager shows CPU activity but no meaningful GPU compute activity.

**Fix:**

1. Run `ollama ps` while generating.
2. Update GPU drivers and Ollama.
3. Verify the discrete GPU/eGPU is attached and visible to Windows.
4. Reduce model size and context.
5. Consult Ollama’s current Windows GPU documentation for device selection and AMD/NVIDIA support.

Do not infer active NPU usage merely because Task Manager exposes an NPU graph. Standard Ollama workflows typically depend on supported GPU paths, while NPU use requires runtime-specific support.[cite:121][cite:118]

### Cline’s result is technically correct but incomplete

**Symptom:** A file-list filter finds a root `package.json`, and the agent calls it the application entry point.

**Fix:** Treat it as a candidate, then conduct the next bounded step: read exactly that file and inspect `scripts`, `main`, `module`, `exports`, `bin`, workspace configuration, and framework-specific fields. A manifest is not automatically a runtime entry point.

## Cost-control playbook

Local inference is not “free”—it uses electricity, hardware capacity, and your time—but it can reduce recurring API or subscription usage when routed to the right tasks.

| Task type | Recommended lane | Cost-control reason |
|---|---|---|
| Explain a file or error | Local chat model | Low risk, frequent, often token-heavy |
| Draft a plan | Small local planner | Saves premium model calls before implementation |
| Search a repository | Local Act model, bounded commands | Private and repeatable |
| Small test/doc edit | Local Act model with review | Good learning and validation workload |
| Complex refactor | Larger local model or hosted fallback | Use the most reliable option, not ideology |
| Security review or production incident | Hosted premium model plus human review | Reliability and speed often outweigh token savings |
| Final code review | Larger local reviewer or cloud model | Match review depth to change risk |

A practical routing policy:

```text
Default: local planner or local chat.
Small repository task: local Act model.
Repeated local failure or multi-file complexity: stronger local coding model.
High-stakes, security-sensitive, or deadline-critical work: hosted model + human review.
```

## Security and privacy

Local models reduce external data transfer, but local does not mean risk-free.

- Keep Ollama bound to localhost unless remote access is intentionally required.
- Do not grant broad shell write authority by default.
- Use a separate Git branch or disposable worktree for experimental agent tasks.
- Keep secrets out of prompts, source trees, terminal output, and logs.
- Use `.gitignore` for generated agent artifacts, logs, and local credentials.
- Review proposed diffs before commits and pushes.
- Keep backups of important repositories and configuration files.

A useful operating principle is: **local-first for routine work, human-reviewed for consequential work, and cloud fallback when it genuinely saves time or reduces risk.**

## Final checklist

### Plumbing

- [ ] Ollama is installed and reachable at `http://localhost:11434`
- [ ] `ollama list` shows the chosen local models
- [ ] Direct `ollama run` test succeeds
- [ ] Cline is installed in the IDE
- [ ] Cline uses the Ollama provider and correct base URL
- [ ] Context starts at 16k and timeout is 120 seconds
- [ ] Git works in the IDE terminal
- [ ] The IDE opened the repository root

### Wiring

- [ ] Planner and executor models have distinct roles
- [ ] Plan model is restricted to no-tools planning if it loops on tools
- [ ] Act model passes a one-command read-only test
- [ ] Act model passes a one-file read-only test
- [ ] Checkpoints work in a Git repository or are intentionally disabled
- [ ] Auto-approve is limited to read and safe commands
- [ ] Omni Chat models are optional and separate from Cline’s agent model

### Operating discipline

- [ ] Start with bounded, reversible tasks
- [ ] Require an explicit tool budget for new models
- [ ] Review diffs and test output before committing
- [ ] Escalate to a stronger/local or hosted model when the task outgrows the agent
- [ ] Record known-good model/context/timeout combinations for each machine

When this checklist is complete, Cline becomes a practical local coding-agent lane: not a magical substitute for every premium agent, but a private, controllable, subscription-sparing helper for the steady stream of software-development plumbing that otherwise quietly burns through hosted tokens.