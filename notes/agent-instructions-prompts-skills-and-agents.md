# Agent Instructions, Prompts, Skills, and Agents

## Who This Is For

This guide is for a **mixed audience**: business professionals who want to use AI responsibly in their daily work, and technical professionals who configure AI-enabled tools and workflows.

The terms *prompt*, *skill*, *agent*, *rule*, and *instruction file* are often used interchangeably. They can all be Markdown files, but they have different jobs. Understanding the distinction helps teams use AI consistently, explain it clearly, and establish sensible controls.

---

## The Short Version

- An **instruction file** establishes default operating expectations for a workspace or repository.
- A **prompt** tells AI what to do for a particular request.
- A **skill** is a reusable procedure for a recurring type of work.
- An **agent** is the worker: an AI model operating with instructions, tools, files, and an execution loop.
- A **specification** defines the result wanted; an **evaluation** verifies whether the result meets the standard.

> **Instructions set the operating context. Prompts make requests. Skills provide repeatable methods. Agents perform the work.**

---

## The Relationship at a Glance

| Artifact | Plain-language purpose | Typical scope | Business analogy | Technical analogy |
|---|---|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, or equivalent | Set the normal rules for work | Workspace, repository, or directory | Operating policies | Repository-level instructions |
| Prompt | Request a particular output | One task or interaction | Work request or meeting brief | A task message/template |
| Skill | Standardize a recurring method | Repeatable capability | Standard operating procedure | A named workflow package |
| Agent | Perform work using approved access and guidance | Goal or workstream | Digital worker | Model plus harness, tools, and loop |
| Specification or brief | State desired outcome and constraints | Project or deliverable | Statement of work | Requirements / acceptance criteria |
| Evaluation or test | Check quality and compliance | Deliverable or workflow | QA checklist / control | Tests, fixtures, rubric, or eval |

---

## 1. Persistent Instruction Files

Files such as `AGENTS.md` and `CLAUDE.md` contain durable guidance that should apply to most work in a repository or workspace. They are the **local operating manual** for an AI-enabled work environment.

They commonly define:

- Required validation, review, or approval steps.
- Naming, documentation, privacy, security, and quality conventions.
- Business boundaries, such as when human approval is required.
- Important source systems, directories, or data-handling restrictions.
- The definition of “done” before work can be represented as complete.

```md
# Workspace Working Rules

- Confirm facts from source material before making customer-facing claims.
- Do not change production configuration without human approval.
- Run documented validation checks before reporting work as complete.
- Record material assumptions, risks, and unresolved questions.
```

### What business colleagues should know

This is where a team records enduring controls: approval requirements, language standards, privacy limits, evidence expectations, and escalation paths.

### What technical colleagues should know

The name alone does not make a file active. Each agent harness decides which instruction files it discovers, their precedence, and whether nested directories can override broader guidance.

---

## 2. Prompts: Focused Requests

A prompt gives an AI instructions for a specific task. It may be typed into a chat, stored as a reusable Markdown template, or generated programmatically.

A useful prompt specifies:

- The desired output.
- The audience.
- The allowed source material.
- Important constraints and exclusions.
- The output format.

```md
# Campaign Review Prompt

Review the attached campaign brief for an executive audience.

Identify:
- The intended customer segment.
- Claims that need evidence or approval.
- Risks to brand, privacy, or regulatory compliance.
- The three decisions required from leadership.

Do not invent performance data, customer approvals, or legal conclusions.
```

A prompt may be saved and reused, but it is primarily an **instruction payload**. It does not necessarily include discovery metadata, procedural assets, tools, or a complete repeatable process.

---

## 3. Skills: Repeatable Capability Packages

A skill is a reusable method for a recurring kind of work. It normally has a name, a description of when to use it, step-by-step instructions, an expected output, and optional support materials such as templates, examples, references, or scripts.

Think of a skill as a **standard operating procedure that an agent can select when the work matches the procedure**.

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

```md
---
name: customer-claim-review
description: Review customer-facing claims for evidence, risk, and approval needs.
---

# Customer Claim Review

Use this skill when reviewing marketing, sales, product, or support content that makes factual claims.

1. Extract each distinct claim.
2. Identify the evidence supporting it.
3. Mark unsupported, ambiguous, or regulated claims.
4. Recommend an owner and approval path for material issues.
5. Return results using the claim-evidence template.
```

A skill is **not an autonomous agent**. It explains *how* to carry out a capability; an agent still selects or receives the skill, invokes tools, and carries out the work.

---

## 4. Agents: The Workers That Act

An agent is an AI model operating inside a **harness**: the surrounding system that supplies instructions, context, tools, permissions, feedback loops, and potentially memory or state.

An agent may read files, select a skill, use approved tools, ask for missing information, validate its results, and hand work to a specialized reviewer. The agent is therefore not just a document or a model; it is the working system that acts toward a goal.

```text
Business goal or technical objective
  ↓
Agent receives task and operating context
  ↓
Agent selects a prompt or skill
  ↓
Agent uses approved tools and source material
  ↓
Agent validates work and reports results
  ↓
Human reviews decisions requiring authority or judgment
```

### Shared operating principle

Treat agents as **assistants with bounded authority**, not independent decision-makers. Agents can prepare, analyze, draft, validate, and flag. Accountable people approve commitments, financial actions, external communications, and consequential business decisions.

---

## Roles: When They Help

Add a role to a prompt or skill when it changes observable behavior: what the AI prioritizes, what evidence it requires, what it may decide, or what it must not do.

```md
Act as an independent compliance reviewer.
Identify evidence gaps and escalation needs.
Do not rewrite the campaign or approve claims.
```

This role is useful because it defines a decision lens and a boundary. In contrast, “You are a helpful, world-class expert” rarely changes a meaningful action.

Common business roles include finance reviewer, security reviewer, sales-enablement reviewer, policy analyst, and adversarial reviewer. Common technical roles include architecture reviewer, test engineer, release manager, and incident analyst.

---

## Where Guidance Belongs

Place a piece of guidance at the **lowest scope that reliably owns it**.

```text
Applies to nearly every task in the workspace?
  → Persistent instruction file

Applies to one request or interaction?
  → Prompt

Defines a recurring, named method that should be reusable?
  → Skill

Defines the desired business result and constraints?
  → Specification, brief, or requirements document

Defines how quality and compliance are checked?
  → Evaluation, checklist, rubric, or test
```

| Example guidance | Best location | Reason |
|---|---|---|
| “Never publish external statements without human approval.” | Persistent instruction file | Broad, durable business control |
| “Turn this meeting transcript into executive decisions and action items.” | Prompt | A specific request against a specific source |
| “Review every public claim against evidence and approval rules.” | Skill | A recurring, repeatable process |
| “Launch a Q3 partner campaign within approved budget and messaging.” | Specification or brief | Defines the intended outcome and constraints |
| “Every public claim needs a source, owner, and approval status.” | Evaluation or checklist | Defines how quality is verified |

---

## Worked Example: Campaign Approval

A campaign approval shows how the artifacts work together without giving the AI unchecked authority.

### Business objective

Launch a partner campaign that uses approved positioning, stays within budget, protects customer and company information, and does not publish unsupported claims.

### Decision ownership

The **executive sponsor** owns the final go/no-go decision. Marketing, product, finance, legal/compliance, and other named reviewers provide approval inputs within their subject-matter authority. The agent prepares evidence and decision materials; it never makes the final approval decision.

| Participant | Accountability in this example |
|---|---|
| Executive sponsor | Makes the final go/no-go decision after required reviews are complete. |
| Marketing owner | Owns campaign strategy, audience fit, creative readiness, and the proposed launch plan. |
| Product owner | Confirms product accuracy, availability, and substantiation for product-related statements. |
| Finance owner | Confirms budget availability and compliance with approved spending authority. |
| Legal/compliance owner | Reviews regulated, contractual, privacy, brand, and policy risks as applicable. |
| Agent | Assembles evidence, checks readiness criteria, flags gaps, and produces a decision packet. |

### Artifact-to-work mapping

| Artifact | Example in the campaign process | Why it belongs there |
|---|---|---|
| Persistent instructions | “Do not publish external copy without the executive sponsor’s recorded approval. Preserve claim sources and approval status.” | These are durable controls for all customer-facing work. |
| Campaign brief / specification | Target audience, offer, campaign channels, budget, timeline, required approvals, prohibited claims, and acceptance criteria | This states the desired business outcome and constraints. |
| Prompt | “Prepare an executive approval summary from the attached brief, draft copy, budget, and evidence register.” | It requests a specific artifact for this campaign. |
| Claim-review skill | Extract claims, link evidence, identify approval gaps, and flag regulated or unsupported language | This is a reusable method for repeated campaign reviews. |
| Agent | Reads approved campaign materials, runs the claim-review skill, prepares a decision packet, and records unresolved risks | The agent performs bounded preparation and validation work. |
| Evaluation / checklist | Each claim has evidence, an owner, approval status, and an approved version; budget and required reviewers are confirmed | This makes campaign readiness observable and auditable. |
| Final approval | Executive sponsor records approve, reject, or request-changes decision after prerequisite reviews | A named accountable person retains final decision authority. |

### Example workflow

```text
1. Marketing creates the campaign brief and provides draft assets.
2. The agent reads standing instructions and the campaign brief.
3. The agent uses the claim-review skill to produce an evidence and risk register.
4. The agent prepares an approval packet: summary, draft assets, budget status,
   claims requiring approval, open questions, and recommendation.
5. Marketing, product, finance, and legal/compliance provide required review input.
6. The executive sponsor records the final approve, reject, or request-changes decision.
7. The agent records the decision and prepares only approved materials for publication.
8. A final checklist confirms that the released version matches the approved version.
```

### Approval packet example

```md
# Campaign Approval Packet

## Decision requested
Executive sponsor: approve, reject, or request changes to the partner campaign.

## Confirmed facts
- Target audience: [from approved brief]
- Budget status: [within / outside approved limit]
- Approved channels: [list]

## Required-review status
| Review area | Accountable reviewer | Status | Material finding |
|---|---|---|---|
| Marketing | [Name] | Pending | [Finding] |
| Product | [Name] | Pending | [Finding] |
| Finance | [Name] | Pending | [Finding] |
| Legal / compliance | [Name] | Pending | [Finding] |

## Claims requiring review
| Claim | Evidence source | Owner | Approval status | Risk / note |
|---|---|---|---|---|
| [Claim] | [Source] | [Owner] | Pending | Needs product validation |

## Open questions
- [Question requiring human judgment]

## Recommendation
- [Proceed only when stated requirements are satisfied]

## Executive sponsor decision
- Decision: [Approve / Reject / Request changes]
- Decision owner: [Executive sponsor name]
- Date and conditions: [Record any decision conditions]
```

### Control boundary

The agent may summarize, compare, flag, and prepare. It must not silently approve claims, alter budget authority, invent evidence, or publish externally unless the process explicitly grants that permission and the executive sponsor’s final approval plus all required prerequisite approvals are recorded.

---

## Common Harness Equivalents

Different AI products use different names for persistent instruction artifacts. The purpose is similar: provide workspace or project context that an agent loads automatically or by convention.

| Agent or harness | Common persistent instruction artifact | Mixed-audience interpretation |
|---|---|---|
| OpenAI Codex | `AGENTS.md` | Shared project operating guidance |
| Claude Code | `CLAUDE.md` | Project-level working expectations |
| GitHub Copilot | `.github/copilot-instructions.md` and `AGENTS.md` | Repository guidance, with optional specialized instructions and agents |
| Hermes Agent | `AGENTS.md` | Primary project context |
| OpenClaw | `AGENTS.md` | Operational workspace instructions; identity and memory may be separate |
| Gemini CLI | `GEMINI.md` | Project or directory context |
| Cursor | `.cursor/rules/*.mdc`, plus supported instruction files | Persistent instructions that can be scoped or context-activated |

For teams using several products, a concise `AGENTS.md` can be the portable baseline. Keep tool-specific files thin, and reserve them for capabilities unique to that tool.

---

## A Portable Repository Pattern

```text
repo/
├── AGENTS.md                              # Shared operating guidance
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
├── specs/                                 # Outcomes and acceptance criteria
├── evals/                                 # Tests, rubrics, and quality checks
└── docs/
    └── runbooks/                          # Human-readable operating procedures
```

This structure separates four questions that otherwise become tangled:

1. How should the AI normally behave here?
2. What do we want it to do right now?
3. Which repeatable process should it use?
4. How will we know the result is acceptable?

---

## Governance Checklist

Before adopting an AI workflow, business and technical owners should be able to answer these questions together:

- What is the agent allowed to read, write, change, or send?
- What information is sensitive, regulated, proprietary, or customer-controlled?
- Which tasks may be automated, and which require human approval?
- What evidence must the agent cite or preserve?
- How will the team detect incorrect, incomplete, or noncompliant work?
- Who owns the skill, instruction file, and evaluation criteria as the process evolves?

Strong AI workflows combine clear instructions, narrow reusable skills, bounded agent permissions, and observable quality checks.

---

## The Decision Test

Before creating a new Markdown artifact, ask:

> If this instruction disappeared, what observable behavior would change?

- If it affects everyday conduct across the workspace, use persistent instructions.
- If it affects one request, use a prompt.
- If it describes a recurring method, use a skill.
- If it defines decision authority, encode it as an agent and process boundary.
- If it defines success, express it in a specification and evaluation criteria.

Clear scope reduces duplicated instructions, contradictory guidance, accidental overreach, and inconsistent results. It also makes AI-enabled work easier to explain, operate, audit, and improve.
