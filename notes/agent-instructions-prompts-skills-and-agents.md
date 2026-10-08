# Agent Instructions, Prompts, Skills, and Agents

## Why This Matters

Modern AI tools are often described with overlapping terms: *prompt*, *skill*, *agent*, *rule*, and *instruction file*. They can all be stored as Markdown, but they perform different jobs.

For technical and business teams alike, the practical question is simple: **where should a piece of guidance live so the AI uses it consistently, appropriately, and safely?**

This guide explains the relationship among these artifacts in plain business language. It applies whether someone is writing code, preparing a marketing plan, analyzing sales data, drafting a policy, or working in an IDE with an AI assistant.

---

## The Short Version

- A **prompt** tells an AI what to do for a particular request.
- A **skill** is a reusable procedure that teaches an AI how to complete a recurring kind of work.
- An **agent** is the worker: an AI model operating with instructions, tools, files, and an execution loop.
- An **instruction file** such as `AGENTS.md` or `CLAUDE.md` establishes default operating expectations for work in a repository or workspace.

A useful shorthand is:

> **Instructions set the operating context. Prompts make requests. Skills provide repeatable methods. Agents perform the work.**

---

## The Relationship at a Glance

| Artifact | Primary purpose | Typical scope | Business analogy |
|---|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, or equivalent | Establish default operating expectations | A repository, workspace, or directory | Employee handbook and operating policies |
| Prompt | Request a specific result | One interaction or task | A work request or meeting brief |
| Skill | Package a repeatable method | A recurring capability | A documented standard operating procedure |
| Agent | Execute work using context, tools, and procedures | A goal or workstream | A team member with authorized tools and responsibilities |
| Specification or brief | Define desired outcome and success criteria | A project or deliverable | Statement of work or campaign brief |
| Evaluation or test | Check whether the work met expectations | A deliverable or workflow | Quality assurance checklist or acceptance test |

---

## 1. Persistent Instruction Files: The Default Operating Context

Files such as `AGENTS.md` and `CLAUDE.md` contain durable guidance that should apply to most work in a repository or workspace. They commonly define:

- How to build, test, validate, or publish work.
- Naming, documentation, security, privacy, and quality conventions.
- Which directories or systems require extra care.
- What must happen before an agent claims a task is complete.
- Limits on tool use, approvals, or changes to production systems.

Think of these files as the **local operating manual**. They tell an AI how to behave before it receives a specific task.

Example:

```md
# Repository Working Rules

- Confirm facts from source material before writing customer-facing claims.
- Do not change production configuration without human approval.
- Run the documented validation checks before marking work complete.
- Record material assumptions and unresolved questions.
```

### Important caveat

These names are conventions, not universal laws. A file applies only if the AI tool or agent harness recognizes and loads it. The harness also determines instruction precedence and directory scope.

---

## 2. Prompts: A Focused Request

A prompt is a set of instructions supplied for a particular interaction. It can be a sentence typed into chat, a reusable Markdown template, or a programmatic message sent to a model.

A prompt should make the immediate outcome clear:

- What needs to be produced?
- Who is the audience?
- What source material or constraints apply?
- What format is required?
- What must not be assumed or invented?

Example: a one-time prompt for a marketing review.

```md
# Campaign Review Prompt

Review the attached campaign brief for an executive audience.

Identify:
- The intended customer segment.
- Claims that need evidence or approval.
- Risks to brand, privacy, or regulatory compliance.
- The three most important decisions required from leadership.

Do not invent performance data or customer approvals.
```

A prompt can be reused, but it is still primarily an **instruction payload**. It does not necessarily include automatic discovery, support files, tools, or a complete repeatable process.

---

## 3. Skills: Repeatable Capability Packages

A skill packages a reusable method for a repeatable type of work. It typically has a name, a description of when to use it, procedural guidance, output expectations, and optional supporting materials such as templates, reference documents, or scripts.

Think of a skill as a **standard operating procedure that an agent can select when the work matches the procedure**.

Example structure:

```text
skills/
└── customer-claim-review/
    ├── SKILL.md
    ├── claim-evidence-template.md
    ├── examples/
    │   └── reviewed-claim.md
    └── scripts/
        └── extract-claims.py
```

Example `SKILL.md`:

```md
---
name: customer-claim-review
description: Review proposed customer-facing claims for evidence, risk, and approval needs.
---

# Customer Claim Review

Use this skill when reviewing marketing, sales, product, or support content that makes factual claims.

1. Extract each distinct claim.
2. Identify the available evidence for that claim.
3. Mark unsupported, ambiguous, or regulated claims.
4. Recommend an owner and approval path for each material issue.
5. Return results using the claim-evidence template.
```

A skill is **not automatically an agent**. The skill tells an agent *how* to perform a capability; the agent is still the system that chooses or receives the skill, calls tools, and carries out the work.

---

## 4. Agents: The Workers That Act

An agent is an AI model operating within a harness: the surrounding environment that gives it instructions, context, tools, permissions, feedback loops, and often memory or state.

An agent may:

- Read files and repository instructions.
- Select or load a relevant skill.
- Use approved tools such as search, spreadsheets, source control, or test runners.
- Ask for missing information or human approval.
- Validate results and revise its work.
- Hand work to a specialized subagent for independent review.

A business-friendly analogy is a **digital worker**. Like a human worker, it needs a clear mandate, appropriate access, defined boundaries, and a way to verify that it completed the assignment correctly.

```text
Business goal
  ↓
Agent receives task and operating context
  ↓
Agent selects a prompt or skill
  ↓
Agent uses approved tools and source materials
  ↓
Agent validates work and reports results
  ↓
Human reviews decisions that require judgment or authority
```

---

## Roles: When They Belong in a Prompt or Skill

A role statement is useful only when it changes observable behavior. It should establish a decision lens, authority boundary, evidence standard, or output expectation.

Good role statement:

```md
Act as an independent compliance reviewer.
Your role is to identify evidence gaps and escalation needs.
Do not rewrite the campaign or approve claims.
```

Weak role statement:

```md
You are a helpful, world-class expert.
```

The first version changes what the agent prioritizes and what it is allowed to do. The second mostly adds decoration.

Use a role inside a prompt or skill when a focused perspective is required. For example:

- A finance reviewer prioritizes traceability, variance, and approval authority.
- A security reviewer prioritizes threats, access control, and evidence.
- A sales-enablement reviewer prioritizes customer relevance, proof points, and objection handling.
- An adversarial reviewer looks for weaknesses rather than simply improving a document.

---

## Where Instructions Belong

Place guidance at the **lowest scope that reliably owns it**.

```text
Does it apply to nearly every task in this workspace?
  → Persistent instruction file

Does it apply to one requested output or one interaction?
  → Prompt

Does it define a recurring, named procedure that should be reusable?
  → Skill

Does it define the desired business outcome and acceptance criteria?
  → Specification, brief, or requirements document

Does it define how success is measured?
  → Evaluation, checklist, rubric, or test
```

Examples:

| Guidance | Recommended location | Why |
|---|---|---|
| "Never publish external statements without human approval." | Persistent instruction file | It applies broadly and expresses an enduring control. |
| "Turn this meeting transcript into executive decisions and action items." | Prompt | It is a specific request for a specific source. |
| "Review every proposed public claim against evidence and approval rules." | Skill | It is a recurring, repeatable business process. |
| "Launch a Q3 partner campaign with approved budget and messaging." | Specification or brief | It defines the target business outcome. |
| "Every public claim must have a source, owner, and approval status." | Evaluation or checklist | It defines how quality is verified. |

---

## Common Harness Equivalents

Different AI products use different names and file locations for persistent instructions. The underlying purpose is similar: provide project or workspace context that the agent loads automatically or by convention.

| Agent or harness | Common persistent instruction artifact | Notes |
|---|---|---|
| OpenAI Codex | `AGENTS.md` | Supports repository and nested-directory instruction files. |
| Claude Code | `CLAUDE.md` | Common project-level instruction convention. |
| GitHub Copilot | `.github/copilot-instructions.md` and `AGENTS.md` | Supports repository guidance and more specialized instruction or agent definitions under `.github/`. |
| Hermes Agent | `AGENTS.md` | Uses it as the primary project context file. |
| OpenClaw | `AGENTS.md` | Operational workspace instructions; identity and memory may be held separately. |
| Gemini CLI | `GEMINI.md` | Project or directory context file convention. |
| Cursor | `.cursor/rules/*.mdc`, plus supported instruction files | Rules can be scoped or activated based on context. |

When a team supports several tools, a concise `AGENTS.md` can serve as a portable baseline. Tool-specific files should be thin extensions used only for features unique to that harness.

---

## A Portable Repository Pattern

```text
repo/
├── AGENTS.md                              # Shared, durable operating guidance
├── CLAUDE.md                              # Claude-specific extension, if needed
├── GEMINI.md                              # Gemini-specific extension, if needed
├── .github/
│   ├── copilot-instructions.md            # Copilot-wide guidance
│   ├── instructions/                      # Copilot scoped instructions
│   └── agents/                            # Copilot specialist agents
├── .cursor/
│   └── rules/                             # Cursor activation-aware rules
├── prompts/                               # Focused request templates
├── skills/                                # Repeatable capability packages
├── specs/                                 # Business outcomes and acceptance criteria
├── evals/                                 # Tests, rubrics, and quality checks
└── docs/
    └── runbooks/                          # Human-readable operating procedures
```

This organization separates four questions that otherwise become tangled:

1. **How should the AI normally behave here?**
2. **What do we want it to do right now?**
3. **Which repeatable process should it use?**
4. **How will we know the result is acceptable?**

---

## Governance and Risk Controls

For business-side use, the most important design choice is not the filename. It is the control model around AI work.

- Keep universal guardrails in persistent instructions.
- Use roles to establish decision boundaries, not to create theatrical personas.
- Require sources, assumptions, and uncertainty labels for consequential analysis.
- Separate preparation from approval: an agent may draft, analyze, or flag; accountable people approve decisions, customer commitments, financial actions, and external communications.
- Use skills for recurring work only after the team can describe the process, decision points, and expected output.
- Create evaluations for high-impact work so the team can test behavior rather than relying on a persuasive demo.
- Prefer small, composable skills over a single giant instruction document.

---

## The Decision Test

Before creating a new Markdown artifact, ask:

> If this instruction disappeared, what observable behavior would change?

- If the answer is **everyday conduct across the workspace**, use persistent instructions.
- If the answer is **this particular request**, use a prompt.
- If the answer is **a recurring method that multiple tasks need**, use a skill.
- If the answer is **who can decide, approve, or act**, encode it as a boundary in the agent and process design.
- If the answer is **what a successful result looks like**, use a specification and evaluation criteria.

Clear scope prevents duplicated instructions, contradictory guidance, accidental overreach, and inconsistent results. It also makes the AI system easier to explain, operate, audit, and improve.
