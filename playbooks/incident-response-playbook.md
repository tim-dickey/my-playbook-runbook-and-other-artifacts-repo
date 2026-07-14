# Incident Response Playbook

## Metadata

| Field | Value |
|---|---|
| **Author** | tim-dickey |
| **Last Updated** | 2026-07-14 |
| **Status** | Active |
| **Audience** | On-call engineers, engineering managers |

---

## Overview

This playbook guides responders through the end-to-end process of declaring, managing, and closing a production incident. It covers communication, escalation, and post-incident review.

## Goals

- Restore service as quickly as possible.
- Keep stakeholders informed throughout the incident.
- Capture learnings to prevent recurrence.

## Scope

**In scope:**

- Production outages and degradations.
- Security incidents affecting production systems.
- Data integrity issues impacting end users.

**Out of scope:**

- Planned maintenance windows.
- Pre-production environment issues.

## Stakeholders & Roles

| Role | Responsibility |
|---|---|
| Incident Commander (IC) | Owns overall coordination; makes final calls on response actions. |
| Technical Lead | Drives technical investigation and mitigation. |
| Communications Lead | Updates status page and notifies stakeholders. |
| Scribe | Maintains the incident timeline and action items. |

## Prerequisites

- [ ] Access to monitoring and alerting dashboards.
- [ ] Access to the incident communication channel (Slack / Teams).
- [ ] Familiarity with relevant runbooks (see References).

## Trigger / When to Use This Playbook

Use this playbook when any of the following are true:

- A customer-facing service is completely unavailable.
- Error rate exceeds 5% for more than 5 minutes.
- A P1 or P2 alert fires in the monitoring system.

## Decision Tree / Process Flow

1. **Detect** — Alert fires or someone reports an issue.
2. **Triage** — Assess severity (P1–P4) and assign an Incident Commander.
3. **Declare** — Open an incident channel; notify stakeholders.
4. **Investigate** — Technical Lead drives root-cause analysis. Reference the relevant runbook.
5. **Mitigate** — Apply a fix or workaround to restore service.
6. **Resolve** — Confirm service is healthy; close the incident.
7. **Review** — Conduct a post-incident review within 48 hours.

## Escalation Path

| Situation | Contact / Team |
|---|---|
| P1 outage lasting > 30 minutes | Engineering Manager + VP Engineering |
| Data loss or breach suspected | Security team immediately |
| Customer SLA at risk | Customer Success team |

## Success Criteria

- [ ] Service is fully restored and error rates are back to baseline.
- [ ] Status page has been updated to reflect resolution.
- [ ] Post-incident review is scheduled.
- [ ] Action items are tracked to completion.

## Post-Incident / Post-Action Review

1. Schedule a blameless retrospective within 48 hours of resolution.
2. Document the timeline, root cause, and contributing factors.
3. Identify and assign action items to prevent recurrence.
4. Update this playbook and any related runbooks with new learnings.

## References

- [Runbooks directory](../runbooks/)
- [Incident severity definitions](../docs/severity-levels.md) *(add when created)*
