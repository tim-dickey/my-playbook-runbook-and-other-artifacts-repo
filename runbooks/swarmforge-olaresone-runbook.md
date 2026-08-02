## SwarmForge Runbook — OlaresOne (host shell alongside Olares K3s)

Purpose: stand up and operate Uncle Bob's SwarmForge agent-swarm harness on the OlaresOne, running natively on the host Linux shell alongside (not inside) Olares's Kubernetes/containerd stack, leveraging the RTX 5090 Mobile GPU for optional local model backends [web:16][web:39][web:41].

### 1. Prerequisites check

- [ ] Confirm Olares is updated: check Settings > System Update in the Olares desktop
- [ ] Enable host shell access: Settings > VPN > toggle on **Allow SSH via VPN** [web:40]
- [ ] Connect via LarePass desktop client to retrieve VPN/SSH credentials [web:40]
- [ ] Confirm current GPU/CPU load from Olares's own services before planning swarm runs (check for contention)

### 2. Access the host shell

```bash
ssh olares@<intranet-or-tailscale-ip>
```

- [ ] Confirm you land on a real host shell, not a container — verify with `hostname` and `uname -a`
- [ ] Confirm this is separate from `olares-cli`, which manages the Kubernetes cluster itself, not general-purpose shell tasks [web:41][web:47]

### 3. Install dependencies

```bash
sudo apt update
sudo apt install -y git tmux curl build-essential
```

- [ ] Install CLI agent backend(s):
  - Claude CLI: install per Anthropic instructions, then `claude setup-token`
  - Codex CLI: install via npm/official installer, authenticate with OpenAI account
- [ ] Verify: `claude --version` / `codex --version`
- [ ] Optional — local model runtime to use the RTX 5090's 24GB VRAM:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### 4. Clone and configure SwarmForge

```bash
git clone https://github.com/unclebob/swarm-forge.git ~/swarm-forge
cd ~/swarm-forge
```

- [ ] Create `swarmforge.conf` defining Architect, Coder, Reviewer roles and backends [web:16]
- [ ] Decide backend mix per role — cloud CLI vs. local model served from the RTX 5090 [web:16][web:42]
- [ ] Write `constitution.prompt` layers (project > engineering > workflow rules) [web:16]
- [ ] Confirm target project repo path is correctly referenced in the config

### 5. Manage GPU contention with Olares's own workloads

- [ ] Check whether Olares has GPU slicing enabled (time-slicing or memory-slicing) under system GPU settings [web:50]
- [ ] If running a local model for a SwarmForge role, carve out a dedicated slice or schedule swarm runs when Olares's own AI services are idle [web:50]
- [ ] Confirm available VRAM before loading a local model: `nvidia-smi`

### 6. Dedicate storage for worktrees

- [ ] Use the 2TB NVMe generously — git worktrees per agent role cost little relative to available storage [web:39]
- [ ] Optionally create a dedicated directory: `mkdir ~/swarmforge-worktrees` and reference it in `swarmforge.conf`

### 7. Launch a run

```bash
cd ~/swarm-forge
./swarmforge.sh
```

- [ ] Confirm tmux sessions spin up per agent role [web:16]
- [ ] Attach to verify: `tmux ls` then `tmux attach -t <session-name>`
- [ ] Confirm git worktrees created correctly: `git worktree list`
- [ ] Watch the shared inter-agent message log (optionally enable the Logger utility agent) to confirm Architect → Coder → Reviewer handoffs [web:16]

### 8. Running detached / remote-triggered sessions

- [ ] Always launch inside detached tmux so runs survive SSH disconnects:
  ```bash
  tmux new -s swarmforge-run -d './swarmforge.sh'
  ```
- [ ] From another machine (Mac Studio, Pangolin) over the Olares VPN tunnel:
  ```bash
  ssh olares@<tailscale-ip>
  tmux attach -t swarmforge-run
  ```
- [ ] Keep all SwarmForge traffic bound to the Olares LAN/VPN tunnel — the tool has no built-in auth layer, so avoid exposing it publicly [web:16][web:40]

### 9. Validation / gatekeeping

- [ ] Confirm Reviewer agent checks run: coverage, CRAP complexity, mutation testing [web:16]
- [ ] Do not merge any agent branch until Reviewer signs off — no auto-merge across worktrees [web:16]
- [ ] Manually spot-check early completed behavior slices before trusting the swarm on subsequent ones — undisciplined agent swarms have failed badly without this gatekeeping in other reported cases [web:22]

### 10. Shutdown / cleanup

```bash
tmux kill-session -t swarmforge-run
```

- [ ] Prune stale worktrees: `git worktree list` then `git worktree remove <path>`
- [ ] Unload local models if not in continuous use to free VRAM back to Olares's services: `ollama stop <model-name>`
- [ ] Review constitution and role prompts post-run, adjusting based on Reviewer feedback

### 11. Quick troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Can't SSH into host | SSH via VPN not enabled | Settings > VPN > Allow SSH via VPN, reconnect via LarePass [web:40] |
| tmux sessions don't launch | tmux not installed | `sudo apt install tmux`, restart shell |
| Agent CLI auth fails | Token expired | Re-run `claude setup-token` / re-auth Codex CLI |
| Local model slow or OOM | GPU contention with Olares's own workloads | Enable GPU slicing or schedule swarm runs during idle periods [web:50] |
| Worktree conflicts | Stale branch from prior run | `git worktree remove` the stale path, re-run |
| Session dies on SSH disconnect | Not launched inside tmux | Always use `tmux new -s <name> -d` pattern |
| Confusing SwarmForge with Kubernetes workloads | Tried to deploy into K3s cluster | Run SwarmForge on the host shell directly, not as a K8s pod — it's not designed for that layer [web:16][web:41] |

