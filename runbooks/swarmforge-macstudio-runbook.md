## SwarmForge Runbook — Mac Studio M3 Ultra (macOS)

Purpose: stand up and operate Uncle Bob's SwarmForge agent-swarm harness on the Mac Studio M3 Ultra as the primary high-compute host, optionally running local model backends alongside cloud CLI agents given its large unified memory pool [web:16][web:62].

### 1. Prerequisites check

- [ ] Confirm macOS is up to date: Apple menu > System Settings > General > Software Update
- [ ] Confirm unified memory config (96GB / 192GB / 256GB+) to plan local model ceiling [web:62]
- [ ] Confirm machine is on stable power (desktop, not battery-dependent)
- [ ] Confirm SSH is enabled if triggering runs remotely: System Settings > General > Sharing > Remote Login

### 2. Install dependencies

```bash
xcode-select --install
brew install git tmux
```

- [ ] Install CLI agent backend(s):
  - Claude CLI: install per Anthropic instructions, then `claude setup-token`
  - Codex CLI: install via npm/official installer, authenticate with OpenAI account
- [ ] Verify: `claude --version` / `codex --version`
- [ ] Optional — local model runtime for on-device agent roles:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
  or install MLX for Apple Silicon-optimized inference [web:62]

### 3. Clone and configure SwarmForge

```bash
git clone https://github.com/unclebob/swarm-forge.git ~/swarm-forge
cd ~/swarm-forge
```

- [ ] Create `swarmforge.conf` defining Architect, Coder, Reviewer roles and backends [web:16]
- [ ] Decide backend mix per role — e.g. cloud CLI for Architect's design reasoning, local model (Ollama/MLX) for Coder's repetitive TDD loop to control API costs [web:16][web:62]
- [ ] Write `constitution.prompt` layers (project > engineering > workflow rules) [web:16]
- [ ] Confirm target project repo path is correctly referenced in the config

### 4. Local model setup (optional, if using on-device backend)

- [ ] Pull a model sized to your unified memory:
  - 96GB config: 30B–65B Q4 models comfortably [web:62]
  - 192GB+ config: 70B+ models at Q5/Q6 quantization [web:62]
  ```bash
  ollama pull <model-name>
  ```
- [ ] Reserve ~20% memory headroom for macOS and agent processes — don't load a model that consumes the full unified memory pool [web:62]
- [ ] Point the relevant SwarmForge role config at the local model's endpoint (e.g. `http://localhost:11434`)

### 5. Launch a run

```bash
cd ~/swarm-forge
./swarmforge.sh
```

- [ ] Confirm tmux sessions spin up per agent role [web:16]
- [ ] Attach to verify: `tmux ls` then `tmux attach -t <session-name>`
- [ ] Confirm git worktrees created correctly: `git worktree list`
- [ ] Watch the shared inter-agent message log (optionally enable the Logger utility agent) to confirm Architect → Coder → Reviewer handoffs [web:16]

### 6. Running detached / remote-triggered sessions

- [ ] Always launch inside detached tmux so runs survive SSH disconnects:
  ```bash
  tmux new -s swarmforge-run -d './swarmforge.sh'
  ```
- [ ] From another machine (Pangolin, OlaresOne) over SSH:
  ```bash
  ssh <user>@<mac-studio-ip>
  tmux attach -t swarmforge-run
  ```

### 7. Thermal and power monitoring (for long/local-inference runs)

- [ ] For sustained local model inference alongside multi-agent orchestration, monitor power draw — comparable Apple Silicon workloads have shown 160–180W sustained under heavy local LLM load [web:54]
- [ ] Ensure adequate desk ventilation for extended sessions
- [ ] Use Activity Monitor or `sudo powermetrics` to watch GPU/Neural Engine utilization if diagnosing slowdowns

### 8. Validation / gatekeeping

- [ ] Confirm Reviewer agent checks run: coverage, CRAP complexity, mutation testing [web:16]
- [ ] Do not merge any agent branch until Reviewer signs off — no auto-merge across worktrees [web:16]
- [ ] Manually spot-check early completed behavior slices before trusting the swarm on subsequent ones — undisciplined agent swarms have failed badly without this gatekeeping in other reported cases [web:22]

### 9. Shutdown / cleanup

```bash
tmux kill-session -t swarmforge-run
```

- [ ] Prune stale worktrees: `git worktree list` then `git worktree remove <path>`
- [ ] Unload local models if not in continuous use: `ollama stop <model-name>` to free unified memory
- [ ] Review constitution and role prompts post-run, adjusting based on Reviewer feedback

### 10. Quick troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| tmux sessions don't launch | tmux not installed or Homebrew PATH issue | `brew install tmux`, restart shell, check `brew doctor` |
| Agent CLI auth fails | Token expired | Re-run `claude setup-token` / re-auth Codex CLI |
| Local model runs out of memory | Model too large for remaining unified memory | Use smaller quantization or reserve less for other apps [web:62] |
| Worktree conflicts | Stale branch from prior run | `git worktree remove` the stale path, re-run |
| Session dies on SSH disconnect | Not launched inside tmux | Always use `tmux new -s <name> -d` pattern |
| Fans ramping / thermal throttling | Sustained local inference + orchestration load | Reduce concurrent local model roles, monitor via `powermetrics` [web:54] |

