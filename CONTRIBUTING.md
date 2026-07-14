# Contributing Guidelines

Thank you for contributing to this repository! The goal is to keep every artifact clear, accurate, and genuinely useful.

## Types of Contributions

- **New playbook** – a strategic guide for a scenario you have encountered.
- **New runbook** – a step-by-step procedural document for a specific task or incident response.
- **Edit** – corrections, clarifications, or updates to existing content.
- **Template improvement** – enhancements to the starter templates in `templates/`.

## Naming Conventions

| Directory | File name format | Example |
|---|---|---|
| `playbooks/` | `<topic>-playbook.md` | `incident-response-playbook.md` |
| `runbooks/` | `<topic>-runbook.md` | `database-backup-runbook.md` |
| `templates/` | `<type>-template.md` | `playbook-template.md` |

- Use lowercase kebab-case for all file names.
- Be specific: `kubernetes-node-drain-runbook.md` is better than `k8s-runbook.md`.

## Document Quality Standards

1. **Complete all sections.** Do not leave template placeholders unfilled.
2. **Be concise.** Prefer numbered steps over paragraphs of prose for procedural content.
3. **Include context.** State the audience, prerequisites, and any assumptions at the top.
4. **Verify steps.** Only document procedures you have actually tested or observed.
5. **Keep it current.** If a process changes, update the runbook/playbook promptly.

## Pull Request Process

1. Fork the repository (or create a feature branch if you have write access).
2. Copy the relevant template and fill it out completely.
3. Place the new file in the correct directory.
4. Open a pull request with a short, descriptive title such as:
   - `Add: Kubernetes node drain runbook`
   - `Update: On-call escalation playbook — new PagerDuty steps`
5. Address any review feedback before merging.

## Review Criteria

Reviewers will check that the artifact:

- Follows the naming convention.
- Has all template sections completed.
- Contains accurate, tested information.
- Is written clearly and is free of typos.
