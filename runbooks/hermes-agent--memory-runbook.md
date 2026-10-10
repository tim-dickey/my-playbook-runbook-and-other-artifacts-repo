# Hermes + Hindsight Runbook

## Purpose

This runbook documents how to connect Hermes Agent to Hindsight for persistent memory through a Router-compatible model gateway, verify that the integration works, and recover from the failure modes encountered during setup.

## Architecture

```text
Hermes Agent
  ├─ primary chat requests → Router → local chat model
  └─ Hindsight plugin → Hindsight API
                         ├─ retain: extract durable memories
                         ├─ recall: retrieve relevant memories
                         └─ embeddings: Router → embedding model
```

Hindsight is the long-term memory service. Hermes is the conversational agent that uses it. Router is the OpenAI-compatible gateway that routes chat and embedding requests to configured local models.

## Confirmed Configuration

| Component | Purpose | Verified state |
|---|---|---|
| Hermes Agent | Conversational agent | Running with Hindsight provider enabled |
| Hindsight plugin | Hermes memory integration | Installed, available, and active |
| Hindsight | Long-term memory store | API reachable and bank operational |
| Active bank | Hermes automatic memory bank | `hermes` |
| Memory template | Initial bank behavior | Conversation |
| Connection mode | Hermes-to-Hindsight connection | `local_external` |
| Router | Model gateway | Provides chat and embedding endpoints |
| Chat model | Hermes answers and memory extraction | Local Qwen model |
| Embedding model | Memory indexing and retrieval | Router `default-embedding` model |

## Validate the Setup

### Check the Hermes provider

Run:

```bash
hermes memory status
```

Expected indicators:

```text
Provider:  hindsight
Plugin:    installed
Status:    available
```

### Check Hindsight health

From an environment that can reach the Hindsight API:

```bash
curl -i <HINDSIGHT_API_URL>/health/ready
```

Expected result: an HTTP 200 response reporting a healthy service and connected database.

### Test retain and recall

1. Start a new Hermes session after changing memory settings.
2. Send a harmless, durable fact:

   ```text
   Please remember that my homelab project uses Hermes, Router, and Hindsight.
   ```

3. Wait until the memory-save message finishes.
4. Ask:

   ```text
   What do you remember about my homelab project?
   ```

Success looks like a `hindsight_recall` preparation message followed by a correct response that uses the stored fact.

Never test memory with passwords, API keys, tokens, private keys, recovery codes, or other secrets.

## Initial Hindsight Bank Setup

1. Create or select a Hindsight bank.
2. Apply the **Conversation** starter template.
3. Configure Hermes to use Hindsight in `local_external` mode.
4. Start a new Hermes session so the new provider configuration is loaded.
5. Confirm `hermes memory status` reports Hindsight as active.

The active automatic-memory bank is `hermes`. Other banks are separate stores and are not automatically used by Hermes unless explicitly configured.

## Troubleshooting

### Hindsight crashes at startup

**Symptom**

The Hindsight API pod or container repeatedly restarts, or enters `CrashLoopBackOff`.

**Known cause**

The configured embedding alias points to an unavailable model. A chat model alone is not enough: Hindsight needs embeddings to index and retrieve memory.

**Inspect previous container logs**

```bash
kubectl -n <NAMESPACE> logs <POD_NAME> \
  -c hindsight-api --previous --tail=200
```

**Typical evidence**

```text
no model is installed that can serve default-embedding
```

**Recovery**

1. Open Router's model or tools interface.
2. Install an embedding-capable model.
3. Set that model as Router's `default-embedding` target.
4. Confirm the model endpoint is callable.
5. Restart or wait for Hindsight to restart.
6. Recheck the readiness endpoint and Hermes memory status.

### HTTP 503: model already serving a request

**Symptom**

Hermes or Hindsight returns an error resembling:

```text
HTTP 503: model ... is already serving the 1 requests it was configured for
```

**Cause**

The local chat model allows only one simultaneous request. A Hermes reply can collide with Hindsight retain work, observation consolidation, or auxiliary title generation.

**Immediate recovery**

1. Let the current model request finish.
2. Use `/retry` once.
3. Do not queue repeated prompts while the model is busy.

**Persistent mitigation**

In **Hindsight → Bank Configuration → Configuration → Observations**:

1. Change **Enable Observations** from `Server Default (Enabled)` to **Disabled**.
2. Select **Save changes**.

This disables automatic background observation consolidation for that bank, reducing competition for a single-concurrency model.

### Auxiliary title-generation HTTP 400

**Symptom**

```text
Auxiliary title generation failed: HTTP 400:
reasoning_effort="none" is not one of the values this model accepts
```

**Meaning**

Memory retain and recall can still function. The failure comes from optional automatic session-title generation, not the memory pipeline.

**Fix**

Disable automatic title generation:

```bash
hermes config set auxiliary.title_generation.enabled false
```

Then restart Hermes:

```bash
exit
hermes
```

Manual titles can still be created with `/title` if needed.

### Provider temporarily unavailable

**Symptom**

Hermes retries a provider and eventually reports it is temporarily unavailable.

**Recovery order**

1. Check whether the chat model is already busy.
2. Wait for the running request to finish.
3. Retry once.
4. Check Router model status and Hindsight health if retries fail.
5. Verify that background observations are disabled for the active bank.

## Operational Rules

- Keep Hindsight's API and dashboard access intentionally limited.
- Store secrets in an appropriate secrets manager or password manager, not in agent memory.
- Prefer one deliberate change at a time; verify retain and recall after each change.
- Treat a successful recall in a new Hermes session as the acceptance test.
- Document model aliases, API URLs, and bank names in deployment-specific private configuration, not in a broadly shared runbook.

## Recovery Checklist

- [ ] Hermes reports Hindsight as installed, available, and active.
- [ ] Hindsight health endpoint returns HTTP 200.
- [ ] Router has a functioning chat model and embedding model.
- [ ] The active bank is `hermes`.
- [ ] Observations are disabled for the active bank if the chat model has single-request concurrency.
- [ ] Automatic title generation is disabled if the local model rejects `reasoning_effort="none"`.
- [ ] A harmless fact can be retained and recalled from a new Hermes session.
