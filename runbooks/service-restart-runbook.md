# Service Restart Runbook

## Metadata

| Field | Value |
|---|---|
| **Author** | tim-dickey |
| **Last Updated** | 2026-07-14 |
| **Status** | Active |
| **Audience** | On-call engineers |
| **Estimated Duration** | 5–15 minutes |

---

## Overview

This runbook describes how to safely restart a systemd-managed service on a Linux host. Use it when a service is unresponsive, consuming excessive resources, or otherwise misbehaving and a restart is the appropriate first response.

## Prerequisites

- [ ] SSH access to the target host.
- [ ] `sudo` privileges on the target host.
- [ ] Confirmation that a restart is safe (no in-flight transactions that cannot be replayed).

## Trigger / When to Use This Runbook

- A monitoring alert fires indicating the service is down or unhealthy.
- The service is responding with errors and a restart has been approved by the Incident Commander.

## Procedure

### Step 1 — Check current service status

```bash
sudo systemctl status <service-name>
```

**Expected output:**

```
● <service-name>.service - ...
   Loaded: loaded (...)
   Active: active (running) since ...
```

If the service shows `failed` or `inactive`, proceed to Step 2.

### Step 2 — Capture logs before restarting

```bash
sudo journalctl -u <service-name> --since "10 minutes ago" > /tmp/<service-name>-pre-restart.log
```

Retain these logs for post-incident review.

### Step 3 — Restart the service

```bash
sudo systemctl restart <service-name>
```

### Step 4 — Verify the service is running

```bash
sudo systemctl status <service-name>
```

**Expected output:**

```
● <service-name>.service - ...
   Active: active (running) since ...
```

### Step 5 — Tail logs to confirm healthy operation

```bash
sudo journalctl -u <service-name> -f
```

Wait 1–2 minutes and confirm no errors are appearing in the log stream. Press `Ctrl+C` to exit.

## Verification

- [ ] `systemctl status` shows `active (running)`.
- [ ] Application-level health check returns HTTP 200 (if applicable).
- [ ] Monitoring alert has cleared.

## Rollback / Recovery

If the service fails to start after a restart:

1. Check logs for the root cause:
   ```bash
   sudo journalctl -u <service-name> -n 100
   ```
2. If a recent configuration change is suspected, restore the previous config and retry:
   ```bash
   sudo systemctl start <service-name>
   ```
3. If the service still fails, escalate to the Incident Commander and follow the [Incident Response Playbook](../playbooks/incident-response-playbook.md).

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Service enters `failed` state immediately after restart | Configuration error or missing dependency | Review logs; fix config; retry |
| Service starts but health check fails | Application-level issue (e.g., database unreachable) | Check dependencies; escalate if needed |
| `sudo systemctl restart` hangs | Service has a long `TimeoutStopSec` | Wait for timeout or use `systemctl kill` |

## References

- [Incident Response Playbook](../playbooks/incident-response-playbook.md)
- [systemd documentation](https://www.freedesktop.org/software/systemd/man/systemctl.html)
