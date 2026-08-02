## SwarmForge Runbook — System76 Pangolin 15 (Pop!_OS)

Purpose: stand up and operate Uncle Bob's SwarmForge agent-swarm harness on the Pangolin 15, using it primarily as a lightweight/mobile driver node (cloud CLI agents, no local model serving given the integrated Radeon 780M GPU) [web:16][web:70].

### 1. Prerequisites check

- [ ] Confirm Pop!_OS is up to date: `sudo apt update && sudo apt full-upgrade -y`
- [ ] Confirm you're on AC power or above 50% battery (expect ~2.5–3 hr under active load) [web:69]
- [ ] Confirm network: Ethernet preferred over WiFi 6E for long swarm runs
- [ ] Confirm SSH access is set up if you'll trigger runs remotely from another home-lab machine

### 2. Install dependencies

```bash
sudo apt install -y git tmux curl build-essential
```

- [ ] Install your CLI agent backend(s). Since the Radeon 780M is integrated graphics with no meaningful VRAM headroom, route all SwarmForge roles through cloud CLIs rather than local models [web:16][web:70]:
  - Claude CLI: follow Anthropic's install instructions, then run `claude setup-token`
  - Codex CLI: install via npm/official installer, authenticate with your OpenAI account
- [ ] Verify both are callable from a plain shell: `claude --version` / `codex --version`

### 3. Clone and configure SwarmForge

```bash
git clone https://github.com/unclebob/swarm-forge.git ~/swarm-forge
cd ~/swarm-forge
```

- [ ] Create `swarmforge.conf` defining agent roles and backends (Architect, Coder, Reviewer) [web:16]
- [ ] Assign CLI backend per role in the config — e.g. Claude CLI for Architect (design reasoning), Codex CLI for Coder (implementation loop)
- [ ] Write or copy your `constitution.prompt` layers (project rules > engineering rules > workflow rules) that all agents must obey [web:16]
- [ ] Confirm the target project repo is cloned locally and its path is referenced correctly in the config

### 4. Dedicate storage for worktrees (optional but recommended)

- [ ] If using the second NVMe slot, mount it and point SwarmForge's worktree base directory there to keep agent branches off your main Pop!_OS drive [web:70]
- [ ] Example: `mkdir /mnt/swarmforge-worktrees` and reference this path in `swarmforge.conf`

### 5. Launch a run

```bash
cd ~/swarm-forge
./swarmforge.sh
```

- [ ] Confirm tmux sessions spin up correctly — one per agent role [web:16]
- [ ] Attach to verify: `tmux ls` then `tmux attach -t <session-name>`
- [ ] Watch the shared inter-agent message log (optionally run the Logger utility agent) to confirm Architect → Coder → Reviewer handoffs are firing [web:16]

### 6. Running detached / remote-triggered sessions

- [ ] Always launch inside a detached tmux session so runs survive SSH disconnects:
  ```bash
  tmux new -s swarmforge-run -d './swarmforge.sh'
  ```
- [ ] If triggering from another machine (Mac Studio, OlaresOne) over SSH, connect and re-attach as needed:
  ```bash
  ssh <user>@<pangolin-ip>
  tmux attach -t swarmforge-run
  ```
- [ ] For remote monitoring without keeping a shell open, consider RustDesk for occasional visual checks

### 7. Power and battery management

- [ ] Keep the Pangolin plugged into its 100W USB-C charger for any run longer than ~30 minutes [web:69][web:70]
- [ ] For unattended/overnight runs, treat the Pangolin as untrusted for battery — prefer using it only as an SSH client into the Mac Studio or OlaresOne, which should carry the actual compute load

### 8. Validation / gatekeeping

- [ ] Confirm the Reviewer agent's checks are running: coverage, CRAP complexity, mutation testing [web:16]
- [ ] Do not merge any agent branch until Reviewer signs off — SwarmForge's worktree isolation means nothing auto-merges without explicit notification [web:16]
- [ ] Spot-check a completed behavior slice manually before trusting the swarm on the next one, especially early in adoption — undisciplined agent swarms have failed badly without this kind of gatekeeping in other reported cases [web:22]

### 9. Shutdown / cleanup

```bash
tmux kill-session -t swarmforge-run
```

- [ ] Prune stale worktrees periodically: `git worktree list` then `git worktree remove <path>` for finished branches
- [ ] Review the constitution and role prompts after each run — adjust based on what the Reviewer flagged

### 10. Quick troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| tmux sessions don't launch | tmux not installed or PATH issue | `sudo apt install tmux`, restart shell |
| Agent CLI auth fails | Token expired or not set | Re-run `claude setup-token` / re-auth Codex CLI |
| Worktree conflicts | Stale branch from prior run | `git worktree remove` the stale path, re-run |
| Session dies on SSH disconnect | Not launched inside tmux | Always use `tmux new -s <name> -d` pattern |
| Sluggish performance | Running local model attempt on iGPU | Route role back to cloud CLI backend instead [web:70] |

