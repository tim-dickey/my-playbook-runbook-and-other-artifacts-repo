## The short answer

Michael's reference checks out: the "open source agent swarm harness" is **SwarmForge**, a tool built by Robert C. Martin ("Uncle Bob") that he discussed with Kent C. Dodds in the July 2026 episode of *Become an Epic Product Engineer* titled "Architecture, AI agents, and product empathy with Robert C. Martin". At the end of that episode, listeners are given an explicit call to action: "Try Robert C. Martin's SwarmForge project locally and follow the setup instructions far enough to run it". This is the tool Michael flagged as one to experiment with in upcoming free time.[^1]

## Who's involved and why it matters

Robert C. Martin is the author of *Clean Code*, *Clean Architecture*, and *The Clean Coder*, a co-author of the Agile Manifesto, and the person who coined the SOLID principles. Kent C. Dodds hosts *Become an Epic Product Engineer* (formerly part of his "Chats with Kent" universe), a podcast focused on skills that stay valuable as AI takes over more implementation work — problem clarity, product judgment, and customer empathy. Their 45-minute conversation, which Dodds publicly called "thrilled" to have recorded, covered software architecture, AI coding agents, and product empathy.[^2][^3][^4]

The core theme of the episode: even as AI agents take over more implementation, the "high-level rules of design and architecture stay remarkably stable" — Martin argues engineers will eventually need to "walk away from the code" and instead review module structure, dependencies, and data flow if they want the real benefit of agents.[^1]

## What is SwarmForge, technically

SwarmForge is deliberately low-tech as far as agent orchestration tools go — no cloud services, no container platforms, just shell scripts, tmux sessions, and git worktrees. Its design philosophy embeds Martin's Clean Code discipline directly into how agents behave, via a layered "constitution" system that every agent must obey.[^2]

| Component | Role |
|---|---|
| swarmforge.sh | Orchestrator script; validates config, launches tmux sessions and agent backends [^2] |
| Architect agent | Owns design, writes Gherkin behavior specs, notifies Coder [^2] |
| Coder agent | Implements one behavior slice at a time using TDD, notifies Reviewer [^2] |
| Reviewer agent | Runs coverage, CRAP complexity, and mutation testing; gatekeeps quality [^2] |
| Logger (optional) | Passive utility that tails the shared inter-agent message log [^2] |
| constitution.prompt | Layered rule file (project > engineering > workflow) all agents must follow [^2] |

Each agent runs in its own git worktree on its own branch, so multiple AI coding agents (Claude CLI or Codex CLI, selectable per role) can work in parallel without stepping on each other's changes; work merges through explicit, notification-driven handoffs rather than silent auto-merges. The repo is hosted at github.com/unclebob/swarm-forge and had passed 283+ stars at last check.[^2]

## The candor behind the pitch: it's not magic

Notably, Martin and other engineers publicly acknowledge that naive, fully autonomous agent swarms often fail badly. In a separate but related discussion, engineers who tried farming out well-scoped tickets to fully autonomous agents called the result a "disaster," with merge conflicts and broken patterns across the board — the fix wasn't more automation, but tighter, hand-guided foundational patterns before letting agents run wide. This context matters: SwarmForge's whole design point (Architect → Coder → Reviewer discipline, worktree isolation, mandatory notification, strict validation) exists specifically to prevent that kind of undisciplined chaos.[^5][^2]

## Where SwarmForge sits in the broader landscape

SwarmForge is one of several open-source "agent harnesses" and "agent swarm" tools that emerged through 2025–2026 as multi-agent coding became mainstream. Others in the same space include:

- **agent-swarm** (desplega-ai) — a lead/worker Docker-based orchestrator for Claude Code instances, with 549+ GitHub stars, MIT-style open source[^6][^7]
- **OpenHarness** (HKUDS) — an open-source Python implementation of a generic "agent harness" covering tool-use, memory, and multi-agent coordination[^8]
- **swarm-orchestrator** — an ISC-licensed tool that verifies agent claims against actual build/test outcomes rather than trusting self-reported agent status, compatible with GitHub Copilot CLI, Claude Code, and Codex[^9]
- **Cursor's research on agent swarm economics** — a July 2026 piece comparing coordination strategies for multi-agent builds, finding that better coordination among cheaper worker models can match higher-cost approaches[^10]

SwarmForge's distinguishing feature versus these peers is its philosophical anchor: rather than adding more orchestration machinery, it intentionally minimizes tooling (tmux + shell + git) while maximizing behavioral discipline through the constitution system — a direct extension of Clean Code principles into the multi-agent era.[^2]

## What Michael (and you) would actually be trying

If you follow the podcast's explicit call to action, trying SwarmForge means: cloning github.com/unclebob/swarm-forge, setting up a `swarmforge.conf` defining agent roles and backends (Claude CLI or Codex CLI), writing role-specific prompt files plus a constitution, and running `swarmforge.sh` to spin up isolated tmux sessions and git worktrees per agent. Given your home-lab and Kubernetes-heavy workflow, it's worth noting SwarmForge assumes local shell/tmux (macOS or Linux) rather than container orchestration — so it would run as a lightweight complement to, not a replacement for, container-based agent stacks you're already exploring.[^2]

---

## References

1. [Architecture, AI agents, and product empathy with Robert C. Martin](https://www.youtube.com/watch?v=RxxxGkFIUJ0) - Kent talks with Robert C. Martin - Uncle Bob - about what AI agents change, what they do not change,...

2. [Swarm Forge: Uncle Bob's AI Agent Coordinator](https://pyshine.com/Swarm-Forge-Uncle-Bobs-AI-Agent-Coordinator/) - Swarm Forge by Uncle Bob Martin is a lightweight tmux-based orchestration platform that coordinates ...

3. [Become an Epic Product Engineer - Video Podcast](https://podcasts.apple.com/am/podcast/become-an-epic-product-engineer/id1896782497) - Architecture, AI agents, and product empathy with Robert C. Martin. Kent talks with Robert C. Martin...

4. [I never really got into Uncle Bob's books before, not sure ...](https://x.com/flaviocopes/status/2081819813194707197) - kentcdodds. Jul 22. Thrilled to have been able to spend 45 minutes talking with @unclebobmartin abou...

5. [Why has nothing ever replaced programmers? - We ...](https://www.youtube.com/watch?v=EHB2X5Qx_EE) - Uncle Bob" Martin! Kent C. Dodds (plus) Architecture, AI agents, and product empathy with Robert C. ...

6. [agent-swarm - AI Agents on GitHub](https://skillsllm.com/skill/agent-swarm) - agent-swarm is an open-source ai agents skill for AI coding assistants such as Claude Code, Codex CL...

7. [desplega-ai/agent-swarm: Your Company ...](https://github.com/desplega-ai/agent-swarm) - Agent Swarm is your Company's Compounding Intelligence Layer. A system of AI agents that remember, r...

8. ["OpenHarness: Open Agent Harness with a Built- ...](https://github.com/HKUDS/OpenHarness) - OpenHarness is an open-source Python implementation designed for researchers, builders, and the comm...

9. [Swarm orchestrator for ai coding agents released](https://www.facebook.com/groups/githubcopilot/posts/1540329548097879/) - Open-source fix for ai coding agent workflow issues. El Mehdį ßel ... Moonshot AI Releases Kimi K2.6...

10. [Agent swarms and the new model economics](https://cursor.com/blog/agent-swarm-model-economics) - We compared old and new agent swarms building SQLite from scratch and found that better coordination...

