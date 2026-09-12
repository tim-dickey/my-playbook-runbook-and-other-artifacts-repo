# Hermes Agent Model & Provider Runbook

**System:** System76 Pangolin 15 laptop running Pop!_OS/Linux  
**Local hardware:** 96 GB RAM; CPU-based local inference observed  
**Primary use:** Hermes research, planning, code assistance, and agent workflows  
**Current recommended primary provider:** GitHub Copilot Pro  
**Current recommended default model:** `gpt-5-mini` with **medium** reasoning effort

---

## 1. Purpose and current state

This runbook documents the work performed to evaluate local LLMs for Hermes Agent, configure Ollama model variants with a larger context window, troubleshoot Hermes/Ollama performance, evaluate Abacus.ai and OpenRouter as cloud providers, and configure GitHub Copilot Pro as the practical primary provider.

### Current working setup

- Hermes is installed as a global CLI and can be invoked from any directory with `hermes`.
- Hermes configuration and state are stored under:

  ```bash
  ~/.hermes/
  ```

- GitHub Copilot Pro is configured in Hermes and was verified to respond successfully.
- The active/default model selected through Copilot is:

  ```text
  gpt-5-mini
  ```

- Reasoning effort is set to:

  ```text
  medium
  ```

- A successful Hermes status bar showed:

  ```text
  ⚕ gpt-5-mini │ 10.8K/264K │ [░░░░░░░░░░] 4% │ 1m
  ```

This confirms that Hermes is operating through Copilot, has a 264K-token available context budget in that session, and is successfully generating responses.

---

## 2. Hermes CLI basics

### Start a normal Hermes chat

```bash
hermes
```

### Display CLI help

```bash
hermes --help
```

### Locate the Hermes executable

Hermes is globally installed; do not `cd` into its installation directory to use it.

```bash
which hermes
```

or:

```bash
command -v hermes
```

### Important directories

The Hermes home directory was observed to contain:

```text
audio_cache
hooks
sandboxes
auth.json
image_cache
sessions
auth.lock
images
skills
bin
logs
SOUL.md
config.yaml
memories
state.db
context_length_cache.yaml
migration
state.db-shm
cron
models_dev_cache.json
state.db-wal
gateway_state.json
ollama_cloud_models_cache.json
whatsapp
hermes-agent
pairing
```

Treat `~/.hermes/config.yaml` as the main configuration file. Avoid manually deleting files in this directory unless you understand their purpose and have a backup.

### Configure providers or defaults

Run this **outside** an active Hermes chat:

```bash
hermes model
```

Use `hermes model` to:

- Add a new provider.
- Authenticate to a provider.
- Run an OAuth/device-code flow.
- Configure a custom endpoint.
- Choose or change a provider/model default.

### Switch model or provider inside a chat

Inside an active Hermes session, use `/model`.

Examples:

```text
/model copilot:gpt-5-mini
```

```text
/model copilot:claude-sonnet-4.6
```

```text
/model openrouter:google/gemini-3-flash-preview
```

Use `/model` only after the provider has already been configured through `hermes model`.

### Show the session status bar

Inside Hermes:

```text
/statusbar
```

This toggles a persistent display of the active model, session/context use, context-fill percentage, cost, and duration.

---

## 3. Local Ollama work

### Local model inventory at the time of evaluation

The following models were installed in Ollama:

```text
qwen3:latest            5.2 GB
qwen3-coder:latest      18 GB
qwen2.5-coder:latest    4.7 GB
llama3.2:latest         2.0 GB
llama3.2:3b             2.0 GB
gemma3n:latest          7.5 GB
gemma3:latest           3.3 GB
devstral:latest         14 GB
cogito:latest           4.9 GB
codellama:latest        3.8 GB
glm-4.7-flash:latest    19 GB
mistral-nemo:latest     7.1 GB
```

### Local model recommendation

For a fully local, CPU-oriented setup on the Pangolin 15, the recommended main candidate was:

```text
qwen3-coder:latest
```

The reason was practical rather than theoretical:

- It is oriented toward coding and tool-like tasks.
- It was faster than GLM-4.7-Flash when tested directly outside Hermes.
- It fits comfortably in 96 GB system RAM.
- It is a more realistic CPU-side model than much larger variants.

### Why 64K context was attempted

Hermes uses a large agent system prompt, tool definitions, history, memories, and related scaffolding. The initial plan was to create 64K-context Ollama variants for use in Hermes.

However, local testing revealed that a 64K context combined with Hermes’ large prompt and CPU inference caused unacceptable latency. Both Qwen3-Coder and GLM could take more than five minutes before responding to even `hi` inside Hermes.

**Lesson:** 96 GB RAM makes large contexts possible to load, but it does not make CPU prompt prefill fast. RAM was not the limiting resource; token-processing speed and large-context prefill were.

### Modelfile storage location

Modelfiles can be saved anywhere. Ollama reads the Modelfile from the path supplied to `ollama create`; it does not require Modelfiles to live in Ollama’s model store.

A valid working directory used during this work was:

```bash
/home/tim_dickey/Local models stuff/
```

Keep custom Modelfiles there if that organization works for you.

### Create a Qwen3-Coder 64K variant

Create a Modelfile:

```bash
cd "/home/tim_dickey/Local models stuff/"
nano Modelfile.qwen3-coder-64k
```

Contents:

```text
FROM qwen3-coder:latest
PARAMETER num_ctx 65536
```

Create the model:

```bash
ollama create qwen3-coder-64k -f Modelfile.qwen3-coder-64k
```

Verify it:

```bash
ollama show qwen3-coder-64k
ollama list
```

Ollama typically exposes the created model with a tag, so Hermes may see:

```text
qwen3-coder-64k:latest
```

rather than merely `qwen3-coder-64k`.

### Create a GLM-4.7-Flash 64K variant

Create a Modelfile:

```bash
cd "/home/tim_dickey/Local models stuff/"
nano Modelfile.glm-4.7-flash-64k
```

Contents:

```text
FROM glm-4.7-flash:latest
PARAMETER num_ctx 65536
```

Build it:

```bash
ollama create glm-4.7-flash-64k -f Modelfile.glm-4.7-flash-64k
```

Verify it:

```bash
ollama show glm-4.7-flash-64k
ollama list
```

### Start and check Ollama

Start the server if it is not already running:

```bash
ollama serve
```

List models:

```bash
ollama list
```

Inspect one model:

```bash
ollama show qwen3-coder-64k:latest
```

Test a model without Hermes:

```bash
ollama run qwen3-coder-64k:latest
```

Then enter:

```text
hi
```

This direct test is important: it separates raw model performance from Hermes agent-prompt and tool overhead.

---

## 4. Ollama and Hermes troubleshooting

### Exact model-name rule

Hermes checks Ollama’s OpenAI-compatible model listing at:

```text
http://127.0.0.1:11434/v1/models
```

The model name Hermes uses must exactly match the `id` returned by Ollama—often including `:latest`.

Inspect the listing:

```bash
curl http://127.0.0.1:11434/v1/models
```

If Hermes reports:

```text
Similar models: glm-4.7-flash-64k:latest
```

then use the complete listed name in Hermes, such as:

```text
/model custom:local-ollama:glm-4.7-flash-64k:latest
```

Likewise, to select Qwen:

```text
/model custom:local-ollama:qwen3-coder-64k:latest
```

### Custom Ollama endpoint

When configuring Ollama as a custom OpenAI-compatible provider in Hermes, use:

```text
http://127.0.0.1:11434/v1
```

Do not append `/chat/completions`; Hermes handles that route itself.

### View Ollama service logs

On Pop!_OS/systemd:

```bash
sudo journalctl -u ollama -f
```

or:

```bash
sudo journalctl -u ollama.service -f
```

This streams logs as Hermes or Ollama sends requests.

### Interpretation of the GLM loading log

Observed log lines included:

```text
offloaded 0/48 layers to GPU
model weights device=CPU size="17.7 GiB"
kv cache device=CPU size="6.2 GiB"
total memory size="24.1 GiB"
llama runner started in 7.05 seconds
```

Interpretation:

- The GLM model loaded successfully.
- It used CPU only: no layers were offloaded to GPU.
- The 64K KV cache accounted for a substantial part of memory use.
- Model loading was not the issue; inference/prompt prefill was the usability bottleneck.

### Why local Hermes was slow

A direct Ollama prompt is small. Hermes adds substantially more content:

- System and agent instructions.
- Tool schemas.
- Session history.
- Memory/context scaffolding.
- Potential planning and tool-call loops.

On CPU, processing this large initial prompt can delay the first generated token for minutes. This is why `ollama run qwen3-coder-64k:latest` could respond more quickly than Hermes with the same model.

### Local conclusion

Local Qwen3-Coder is workable for direct Ollama usage and experimentation. It was not a satisfying Hermes primary model at a 64K context setting on this laptop due to the large agent-prompt prefill cost.

GLM-4.7-Flash was slower and/or prone to stalling in this setup, so it was demoted from consideration as a primary Hermes model.

---

## 5. Local-model cleanup suggestions

These were the proposed housekeeping decisions—not mandatory removals.

### Keep

```text
qwen3-coder:latest
qwen3:latest
glm-4.7-flash:latest          # Optional; retain only if you wish to experiment
llama3.2:3b                   # Small/fast quick-chat option
gemma3:latest or gemma3n:latest
```

### Consider removing if not specifically used

```text
codellama:latest
mistral-nemo:latest
devstral:latest
cogito:latest
```

Optionally, remove the older coding model if Qwen3-Coder is sufficient:

```text
qwen2.5-coder:latest
```

### Remove an Ollama model

```bash
ollama rm codellama:latest
```

Example cleanup:

```bash
ollama rm codellama:latest
ollama rm mistral-nemo:latest
ollama rm devstral:latest
ollama rm cogito:latest
```

Do not remove a model merely because it is old if you know you use it for a particular workflow. Removed models can be pulled again later.

---

## 6. Abacus.ai evaluation and outcome

### Abacus RouteLLM endpoint

The Python example provided by Abacus used:

```python
url = "https://routellm.abacus.ai/v1/chat/completions"
```

For a custom OpenAI-compatible provider in Hermes, the configured **base URL** must omit `/chat/completions`:

```text
https://routellm.abacus.ai/v1
```

Hermes appends `/chat/completions` automatically.

### Avoid duplicate endpoint suffixes

Incorrect Hermes base URL:

```text
https://routellm.abacus.ai/v1/chat/completions
```

This led Hermes to call:

```text
https://routellm.abacus.ai/v1/chat/completions/chat/completions
```

and caused:

```text
HTTP 404: Method chat/completions/chat/completions not found
```

### Tool-calling limitation discovered

Attempting to use:

```text
meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8
```

produced an Abacus response that the model did not support tool calling.

Hermes is agent-first and normally sends tool definitions. Therefore, an Abacus model that cannot accept OpenAI-style tools is not suitable as a primary Hermes model.

### Message-role incompatibility discovered

Trying Abacus model `gpt-5.1` got past the tool-support issue but failed with:

```text
Invalid role "developer" in messages. Must be one of user, assistant, system or tool.
```

Hermes sends the newer OpenAI `developer` role in its request flow. The Abacus RouteLLM implementation rejected that role, even though it advertised OpenAI compatibility.

### Abacus conclusion

Abacus RouteLLM was not used as the Hermes primary provider because of two compatibility blockers:

1. Some candidate models did not support tools.
2. The endpoint rejected Hermes’ `developer` message role.

Abacus may still be useful for direct scripted API calls or non-agent chat, but it is not the current recommended Hermes path unless either Hermes adds a compatible role-mapping option or Abacus accepts the `developer` role.

---

## 7. OpenRouter setup and caveat

### Add OpenRouter as a secondary provider

From the terminal:

```bash
hermes model
```

Choose **OpenRouter**, authenticate with an OpenRouter API key, and select a default OpenRouter model.

This does not need to replace GitHub Copilot. Hermes can retain both providers.

### Use OpenRouter after setup

Inside Hermes:

```text
/model openrouter
```

Then select a specific model, for example:

```text
/model openrouter:google/gemini-3-flash-preview
```

Switch back to Copilot:

```text
/model copilot:gpt-5-mini
```

### OpenRouter 402 behavior discovered

Using:

```text
google/gemini-3-flash-preview
```

returned:

```text
HTTP 402: This request requires more credits, or fewer max_tokens.
You requested up to 65536 tokens, but can only afford 13316.
```

Hermes was requesting up to 65,536 output tokens per call. OpenRouter performed a preflight affordability check based on that maximum, even if the actual intended response would be small.

### Attempted configuration override

The following was added to `~/.hermes/config.yaml`:

```yaml
model:
  default: google/gemini-3-flash-preview
  max_tokens: 15000
  provider: openrouter
  base_url: https://openrouter.ai/api/v1
```

Despite this setting, OpenRouter still reported a 65,536-token request.

### OpenRouter conclusion

In the Hermes version used during this work, `model.max_tokens` in `config.yaml` was not honored in the relevant CLI flow. Therefore:

- Add adequate OpenRouter credits if you want to use 64K-style Hermes requests.
- Keep a strict spend limit in the OpenRouter dashboard.
- Treat OpenRouter as an optional/secondary provider until the `max_tokens` override behavior is confirmed fixed in a future Hermes release.

Do not assume that setting `max_tokens` in `config.yaml` is currently effective; confirm by inspecting the next provider error or request behavior.

---

## 8. GitHub Copilot Pro: primary provider

### Why Copilot became the recommended primary path

GitHub Copilot Pro was already available and Hermes supports it as a first-class provider. It avoided:

- CPU-only local inference delays.
- Abacus tool-calling and message-role incompatibilities.
- OpenRouter’s low-credit/max-token preflight failure.

### Configure Copilot in Hermes

Run:

```bash
hermes model
```

Select **GitHub Copilot** and complete the authentication flow. Hermes may use an existing GitHub CLI login/token or present a device-code login flow.

### Copilot model list observed

The provider offered models including:

```text
gemini-3-flash-preview
claude-opus-4.7
claude-sonnet-4.6
gemini-3.1-pro-preview
gpt-5.2-codex
gpt-5.3-codex
gpt-5.4-mini
gpt-5.4
gpt-5-mini
grok-code-fast-1
claude-sonnet-4
claude-sonnet-4.5
claude-opus-4.5
claude-haiku-4.5
gemini-2.5-pro
gpt-5.2
gpt-4.1
gpt-4o
```

### Selected default model

For general research, planning, and everyday agent use, select:

```text
gpt-5-mini
```

Reasoning:

- It provides a good tradeoff between quality, speed, and premium-request usage.
- It is less extravagant than full GPT-5.4 or Claude Opus tiers.
- It remains capable enough for planning, research synthesis, and normal agent work.

### Reasoning effort setting

When Hermes asks for GPT-5-mini reasoning effort, use:

```text
medium
```

Guidance:

- `low`: use for simple, latency-sensitive tasks.
- `medium`: recommended daily default for research/planning.
- `high`: reserve for difficult, high-value analysis or complex technical work; it can be slower and use more model effort.
- `Disable reasoning`: use only if you specifically prefer a more direct, non-reasoning style.

### Switch to more capable Copilot models selectively

For an unusually hard task, switch inside Hermes for the current session:

```text
/model copilot:gpt-5.4
```

or:

```text
/model copilot:claude-sonnet-4.6
```

Return to the economical daily default:

```text
/model copilot:gpt-5-mini
```

Use the exact names Hermes lists if syntax differs in a future update.

---

## 9. Hermes dashboard

### Launch the official dashboard

The installed Hermes CLI did not support `hermes web` or `hermes ui`.

Use:

```bash
hermes dashboard
```

Run it from any directory, including your home directory:

```bash
cd ~
hermes dashboard
```

Open the localhost URL printed by the command.

### What the official dashboard is for

The official dashboard is primarily a control/observability interface. Use it to inspect and manage items such as:

- Sessions and transcripts.
- Token/context consumption.
- Logs and runtime state.
- Models/providers and settings.
- Tools, skills, and agent operations.

### Important limitation

Treat the official dashboard as **mission control**, not necessarily as the primary web chat client. The terminal TUI remains the reliable chat interface.

If a browser chat interface becomes important later, investigate a separate community web UI or an Open WebUI integration. Verify compatibility and security before exposing any local endpoint beyond localhost.

---

## 10. Recommended operating model

### Daily default

Use Copilot with GPT-5-mini at medium reasoning:

```bash
hermes
```

Inside Hermes, confirm or switch:

```text
/model copilot:gpt-5-mini
```

### Research/planning work

- Start with `gpt-5-mini` at medium reasoning.
- Use `/statusbar` to watch context and duration.
- Move to `gpt-5.4` or `claude-sonnet-4.6` only when the task is unusually complex or high stakes.

### Coding or code-review work

- Start with `gpt-5-mini` for routine analysis.
- Consider a Codex model from Copilot for coding-intensive work:

```text
/model copilot:gpt-5.2-codex
```

or:

```text
/model copilot:gpt-5.3-codex
```

Use the Copilot model picker as the source of truth for currently available IDs.

### Local/private experimentation

Use direct Ollama rather than Hermes for quick local prompts when speed matters:

```bash
ollama run qwen3-coder:latest
```

Use `qwen3-coder-64k:latest` only when a large context is genuinely required and you can accept slow CPU inference.

### OpenRouter as a secondary option

- Configure it through `hermes model`.
- Use it only after adding enough credits to satisfy Hermes’ 64K maximum-request behavior.
- Set a provider/key spending cap in OpenRouter before extended agent sessions.
- Do not assume `model.max_tokens` is presently honored by Hermes.

---

## 11. Troubleshooting reference

| Symptom | Likely cause | Action |
|---|---|---|
| Hermes cannot see an Ollama custom model | Model name differs from Ollama’s `/v1/models` listing, often missing `:latest` | Run `curl http://127.0.0.1:11434/v1/models`; use exact returned model ID |
| Hermes reports `custom` is not found | Provider label/type was interpreted as a model | Select a fully qualified model ID such as `custom:local-ollama:qwen3-coder-64k:latest` |
| Ollama model loads but Hermes takes minutes before first token | Hermes system prompt/tools/history create a very large CPU prefill | Use Copilot/cloud provider for Hermes; use direct Ollama for local quick tasks |
| GLM-4.7-Flash seems stuck | Large CPU model/context and possible model/tool-flow instability | Test directly with `ollama run`; prefer Qwen3-Coder or use cloud provider |
| Abacus returns `chat/completions/chat/completions not found` | Base URL contains endpoint path Hermes appends itself | Set base URL to `https://routellm.abacus.ai/v1` |
| Abacus returns model does not support tool calling | Selected model cannot accept tools | Select a tool-enabled model, but note the later `developer` role incompatibility |
| Abacus rejects `developer` role | RouteLLM compatibility gap | Do not use Abacus RouteLLM as current primary Hermes provider |
| OpenRouter returns 402 and says 65,536 tokens requested | Hermes is sending a 64K maximum request and credit balance is too low | Add credits, impose an OpenRouter spend cap, or use Copilot instead |
| `max_tokens` in config does nothing | Hermes version may ignore it in CLI/web flow | Confirm by observing provider request errors; do not rely on it until verified fixed |
| `hermes web` or `hermes ui` fails | Those commands do not exist in installed CLI version | Use `hermes dashboard` |

---

## 12. Security and maintenance checklist

- Never paste API tokens into chats, screenshots, committed files, or shared runbooks.
- Keep API keys in Hermes’ authentication/config flow or supported environment variables, not in shell history where possible.
- Maintain separate spending limits for OpenRouter/API providers.
- Keep the Hermes dashboard bound to localhost unless you intentionally configure remote access and secure it.
- Before updating Hermes, back up `~/.hermes/config.yaml`, `SOUL.md`, skills, memories, and any custom configuration.
- After Hermes updates, re-test:
  - Copilot authentication.
  - Active default model.
  - `/model` switching.
  - OpenRouter `max_tokens` behavior if you intend to use it.
  - Dashboard startup via `hermes dashboard`.

---

## 13. Quick-command cheat sheet

```bash
# Start Hermes chat
hermes

# Configure providers/models
hermes model

# Show command help
hermes --help

# Launch official dashboard
hermes dashboard

# Find Hermes executable
which hermes

# Start Ollama (if not running as a service)
ollama serve

# View Ollama models
ollama list

# View exact OpenAI-compatible Ollama model IDs
curl http://127.0.0.1:11434/v1/models

# Run local Qwen directly
ollama run qwen3-coder:latest

# Follow Ollama service logs
sudo journalctl -u ollama -f

# Inspect a local model
ollama show qwen3-coder-64k:latest
```

Inside Hermes:

```text
/statusbar
/model copilot:gpt-5-mini
/model copilot:gpt-5.4
/model copilot:claude-sonnet-4.6
/model openrouter:google/gemini-3-flash-preview
```

---

## 14. Final recommendation

Use **GitHub Copilot Pro + `gpt-5-mini` + medium reasoning** as the normal Hermes setup. It is the best practical balance of capability, compatibility, and incremental cost among the evaluated paths.

Keep Ollama/Qwen3-Coder for private direct local experiments. Keep OpenRouter configured as a secondary option only after setting credits and a spending cap. Do not make Abacus RouteLLM the primary Hermes provider unless its tool-calling and `developer`-role compatibility changes.
