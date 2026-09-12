# Runbook: FastFlowLM + Liquid LFM2.5 NPU Reality Check

**System:** CORSAIR AI WORKSTATION 300  
**Purpose:** Commission and validate AMD Ryzen AI NPU inference with FastFlowLM, run a small Liquid LFM2.5 instruction-following evaluation, and capture direct XRT evidence of NPU offload.  
**Audience use:** Reproducible local-AI experiment and YouTube production runbook.  
**Status:** Baseline run completed successfully through NPU validation, LFM2.5 model load, quality checks, and XRT offload verification.

---

## 1. Experiment question

> Can the CORSAIR AI WORKSTATION 300 run FastFlowLM with a Liquid LFM2.5 model on its AMD NPU in a way that is operationally real, locally private, observable, and useful for narrow technical-research tasks?

This is an **NPU-only** experiment. It is not an iGPU, NVIDIA, Apple Silicon, or cloud-model comparison.

### What the experiment must prove

1. Linux can expose the AMD XDNA NPU to a user-space runtime.
2. XRT can enumerate the NPU and create usable hardware contexts.
3. FastFlowLM can validate the complete NPU stack.
4. FastFlowLM can load a supported NPU-native Liquid LFM2.5 model.
5. The model can perform bounded, source-grounded research tasks.
6. XRT can show active NPU hardware contexts, column allocation, submissions, and completions while inference runs.

### What it must not claim

- That all model computation is exclusively NPU-resident. CPU work such as tokenization and process orchestration may still occur.
- That the NPU is 100% utilized unless a supported metric explicitly reports a utilization percentage.
- That the NPU is faster than an iGPU, RTX GPU, Mac, or cloud service.
- That a successful smoke test proves autonomous research-agent reliability.
- That a generic LFM2.5 GGUF is automatically equivalent to FastFlowLM's NPU-native model package.

---

## 2. Known baseline configuration

| Component | Observed baseline |
|---|---|
| Workstation | CORSAIR AI WORKSTATION 300 |
| Processor | AMD Ryzen AI Max+ 395 with Radeon 8060S |
| NPU runtime identity | RyzenAI-npu5 / `aie2p` |
| NPU PCI address | `0000:c7:00.1` |
| NPU topology | 6x8; FastFlowLM reports 8 columns |
| NPU firmware | 1.1.2.65 |
| Operating system | Ubuntu 26.04.1 LTS |
| Kernel | 7.0.0-31-generic |
| AMD XDNA DRM driver | 0.7 |
| XRT | 2.25.00 |
| FastFlowLM baseline | v1.0.1 |
| Main model | `lfm2.5-it:1.2b` / `LFM2.5-1.2B-NPU2` |
| Main power mode | `performance` |
| Main context limit | 8192 tokens |
| Local FastFlowLM model path | `~/.config/flm/models/` |

### Existing non-test model inventory

An existing model, `LiquidAI/LFM2.5-8B-A1B-GGUF:Q4_K_M`, may already be stored elsewhere on the workstation. Do not treat it as the FastFlowLM NPU test artifact unless FastFlowLM explicitly recognizes and validates it. This runbook tests FastFlowLM's curated NPU-native package and exact model tag.

---

## 3. Safety and test boundaries

- Keep the experiment local. Use `--host 127.0.0.1` if using server mode.
- Do not expose FastFlowLM to the LAN or Internet during commissioning.
- Do not run a competing ROCm/HIP iGPU workload at the same time as FastFlowLM NPU testing. Keep the first experiment NPU-only.
- Capture terminal output to files before changing system configuration.
- Make one bootloader change at a time and preserve a rollback copy.
- Do not update FastFlowLM midway through a baseline measurement. Record the installed version and use any update as a separate experiment.
- Treat model outputs as draft material. Human-review all research claims and structural constraints.

---

## 4. Evidence directory

Create an experiment folder before beginning:

```bash
mkdir -p ~/fastflowlm-reality-check
```

Recommended subdirectories:

```bash
mkdir -p ~/fastflowlm-reality-check/{baseline,npu-ready,lfm2.5-it,offload-proof,quality,sva-diagnosis}
```

Keep all captured command output in this directory. It is the experiment's reproducibility receipt.

---

## 5. Phase A — Preflight and diagnostics

### 5.1 Confirm FastFlowLM is available

```bash
flm help
flm version
```

Expected commands include `run`, `serve`, `pull`, `remove`, `check`, `list`, and `validate`.

Capture baseline output:

```bash
flm version | tee ~/fastflowlm-reality-check/baseline/flm-version.txt
flm validate --json | tee ~/fastflowlm-reality-check/baseline/flm-validate.json
flm list --filter installed | tee ~/fastflowlm-reality-check/baseline/installed-models.txt
```

### 5.2 Inspect Linux, device, and driver state

```bash
uname -a | tee ~/fastflowlm-reality-check/baseline/uname.txt
cat /etc/os-release | tee ~/fastflowlm-reality-check/baseline/os-release.txt

ls -l /dev/accel 2>&1 | tee ~/fastflowlm-reality-check/baseline/dev-accel.txt
lsmod | grep -E 'amdxdna|xrt' | tee ~/fastflowlm-reality-check/baseline/npu-modules.txt

lspci -nnk | grep -A4 -iE 'npu|accelerator|amd' \
  | tee ~/fastflowlm-reality-check/baseline/pci-accelerators.txt

id | tee ~/fastflowlm-reality-check/baseline/id.txt
getfacl /dev/accel/accel0 2>&1 \
  | tee ~/fastflowlm-reality-check/baseline/accel0-acl.txt
```

### Expected healthy indicators

- `/dev/accel/accel0` exists.
- The `amdxdna` kernel module is loaded.
- PCI reports an AMD Strix Halo NPU, typically device `1022:17f0`.
- The NPU is driven by `amdxdna`.
- The active user is in the `render` group, or has a suitable ACL on `/dev/accel/accel0`.

### 5.3 Capture kernel diagnostics

Ubuntu may restrict unprivileged `dmesg` access. Use `journalctl` with `sudo`:

```bash
sudo journalctl -k -b \
  | grep -iE 'amdxdna|xdna|aie|xrt|npu|sva|pasid|iommu|ivrs|iommufd|ats|pri|firmware' \
  | tee ~/fastflowlm-reality-check/baseline/npu-kernel-boot.txt
```

Expected boot-time healthy indicators include:

```text
Load firmware amdnpu/17f0_11/npu_7.sbin
Initialized amdxdna_accel_driver ...
```

Do not assume those two lines alone mean inference can run. The NPU must also be usable through XRT.

---

## 6. Phase B — XRT installation and validation

### 6.1 Check for XRT tools

```bash
command -v xrt-smi
xrt-smi examine
```

If `xrt-smi` is absent, inspect the package candidates:

```bash
sudo apt update
apt-cache policy libxrt-utils
apt-cache search xrt | grep -Ei 'amd|xdna|xrt'
```

Install the XRT utility package if appropriate for the configured repositories:

```bash
sudo apt install libxrt-utils
```

Confirm installed XRT/XDNA-related packages:

```bash
dpkg -l | grep -Ei 'xrt|xdna'
find /usr -type f \( -iname '*amdxdna*' -o -iname '*xrt*' \) 2>/dev/null | head -n 100
```

### 6.2 Healthy XRT result

```bash
xrt-smi examine
```

A healthy system should show a device similar to:

```text
Device(s) Present
|BDF             |Name          |Architecture  |Topology  |
|[0000:c7:00.1]  |RyzenAI-npu5  |aie2p         |6x8       |
```

If XRT returns:

```text
Open /dev/accel/accel0 failed (err=-19): No such device
```

do not attempt model downloads or benchmarks. Continue to Phase C.

---

## 7. Phase C — Fix common NPU readiness blockers

### 7.1 Memlock limit

FastFlowLM requires a large locked-memory allowance. Check current limits:

```bash
ulimit -l
ulimit -Hl
```

If either is a small number such as `8192`, create a persistent PAM limits file:

```bash
sudo tee /etc/security/limits.d/99-fastflowlm-memlock.conf >/dev/null <<'EOF'
# FastFlowLM / AMD XDNA NPU inference
* soft memlock unlimited
* hard memlock unlimited
EOF
```

Verify:

```bash
cat /etc/security/limits.d/99-fastflowlm-memlock.conf
```

Then log out and back in completely, or reboot. A newly opened terminal may inherit the old desktop-login limit.

Verify after the new session:

```bash
ulimit -l
ulimit -Hl
```

Expected:

```text
unlimited
unlimited
```

### 7.2 NPU user permissions

Check group membership and ACL:

```bash
id
groups
getfacl /dev/accel/accel0
```

The device is normally owned by `root:render`. If necessary, add the active user to the `render` group:

```bash
sudo usermod -aG render "$USER"
```

Log out and back in before retesting. In the validated baseline, the user already had `render` membership and an explicit `rw-` ACL; permissions were not the root cause.

### 7.3 SVA/IOMMU failure

#### Symptom

Kernel logs show:

```text
amdxdna_drm_open: SVA bind device failed, ret -19
```

XRT shows:

```text
Open /dev/accel/accel0 failed (err=-19): No such device
```

FastFlowLM shows:

```json
"amd_device_found": false,
"ready": false
```

#### Root-cause check

Inspect the active boot command line:

```bash
cat /proc/cmdline
```

A critical failure condition is:

```text
amd_iommu=off
```

This disables the AMD IOMMU needed for the NPU's shared virtual addressing path. The NPU may still appear in PCI and load its firmware, but applications cannot create a usable NPU context.

#### Fix without an editor

Back up GRUB defaults:

```bash
sudo cp -a /etc/default/grub /etc/default/grub.backup-$(date +%F-%H%M%S)
grep '^GRUB_CMDLINE_LINUX' /etc/default/grub
```

Remove **only** `amd_iommu=off` and create an additional pre-change backup:

```bash
sudo sed -i.pre-iommu-fix 's/\<amd_iommu=off\>[[:space:]]*//' /etc/default/grub
```

Verify that the token is gone while other parameters are preserved:

```bash
grep '^GRUB_CMDLINE_LINUX_DEFAULT=' /etc/default/grub
grep -nEi 'iommu|GRUB_CMDLINE' /etc/default/grub
```

Do not replace it with `iommu=off`, `amd_iommu=off`, or `iommu=pt` as an untested workaround. Do not disable IOMMU when the NPU requires SVA.

Regenerate GRUB and reboot:

```bash
sudo update-grub
sudo reboot
```

#### Rollback

If a rollback is required before reboot:

```bash
sudo cp -a /etc/default/grub.pre-iommu-fix /etc/default/grub
sudo update-grub
```

### 7.4 Revalidate after reboot

```bash
mkdir -p ~/fastflowlm-reality-check/npu-ready

cat /proc/cmdline \
  | tee ~/fastflowlm-reality-check/npu-ready/kernel-cmdline.txt

ulimit -l \
  | tee ~/fastflowlm-reality-check/npu-ready/memlock.txt

xrt-smi examine \
  | tee ~/fastflowlm-reality-check/npu-ready/xrt-smi-examine.txt

flm version \
  | tee ~/fastflowlm-reality-check/npu-ready/flm-version.txt

flm validate \
  | tee ~/fastflowlm-reality-check/npu-ready/flm-validate.txt

flm validate --json \
  | tee ~/fastflowlm-reality-check/npu-ready/flm-validate.json
```

Required FastFlowLM JSON outcome:

```json
{
  "amd_device_found": true,
  "memlock_ok": true,
  "ready": true
}
```

The validated baseline displayed:

```text
[Linux]  NPU: /dev/accel/accel0 with 8 columns
[Linux]  NPU FW Version: 1.1.2.65
[Linux]  amdxdna version: 0.7
[Linux]  Memlock Limit: infinity
```

---

## 8. Phase D — Select and provision the NPU model

### 8.1 List LFM choices

```bash
flm list | grep -i lfm
```

Observed catalog entries:

```text
lfm2:1.2b
lfm2:2.6b
lfm2-trans:2.6b
lfm2.5-it:1.2b
lfm2.5-tk:1.2b
```

### 8.2 Model selection

Use:

```text
lfm2.5-it:1.2b
```

Rationale: this is the instruction-tuned NPU-native model appropriate for the experiment's document-summary, fact extraction, fact-versus-inference, and executive-brief tasks.

Do not use `lfm2.5-tk:1.2b` for the initial quality test. Reserve the tool-calling variant for a separate server/API experiment with explicit tool definitions and output validation.

### 8.3 Check and pull

```bash
flm check lfm2.5-it:1.2b
flm pull lfm2.5-it:1.2b
flm check lfm2.5-it:1.2b
flm list --filter installed
```

Expected integrity result:

```text
[FLM]  Checking file: config.json...
[FLM]  Success!
[FLM]  Checking file: model.q4nx...
[FLM]  Success!
[FLM]  Checking file: tokenizer.json...
[FLM]  Success!
[FLM]  Checking file: tokenizer_config.json...
[FLM]  Success!
[FLM]  Model check completed successfully. All files are present and compatible.
```

Capture the exact model environment:

```bash
mkdir -p ~/fastflowlm-reality-check/lfm2.5-it

flm version \
  | tee ~/fastflowlm-reality-check/lfm2.5-it/flm-version.txt

flm validate --json \
  | tee ~/fastflowlm-reality-check/lfm2.5-it/npu-validation.json

flm check lfm2.5-it:1.2b \
  | tee ~/fastflowlm-reality-check/lfm2.5-it/model-check.txt

flm list --filter installed \
  | tee ~/fastflowlm-reality-check/lfm2.5-it/installed-models.txt
```

---

## 9. Phase E — Smoke test

### 9.1 Launch the model

```bash
flm run lfm2.5-it:1.2b --pmode performance --ctx-len 8192
```

Expected startup patterns:

```text
[FLM]  Loading model: /home/<user>/.config/flm/models/LFM2.5-1.2B-NPU2
[FLM]  Loading model: lfm2.5-it:1.2b
[FLM]  Type /? for help
>>>
```

### 9.2 Smoke prompt

```text
In exactly two sentences, explain why a device can appear in Linux hardware listings but still be unusable for an NPU application. Do not mention this conversation.
```

Record:

- Cold-load time from `flm run` to interactive prompt.
- Time to first output token.
- Whether output appears coherently.
- Whether the strict two-sentence constraint is satisfied.
- Whether the model exits cleanly with `Ctrl+C`.

### 9.3 Baseline observed result

The model generated a coherent but generic one-sentence answer. Record as:

```text
Runtime: PASS
Constraint adherence: PARTIAL
```

This separates successful NPU inference from successful research-assistant behavior.

---

## 10. Phase F — Quality evaluation

### 10.1 Evaluation intent

Test whether the 1.2B instruction model can perform small, useful research tasks while preserving source grounding and explicit constraints.

The project includes a longer original evaluation artifact, `llm-evaluation-quest-inspired.md`, designed to test faithful summary, fact/inference separation, constraint handling, uncertainty calibration, and resistance to untrusted embedded instructions. For the first on-camera test, use the short fixed source below so manual scoring is quick and repeatable.

### 10.2 Fixed short source

```text
The Corsair AI Workstation 300 uses an AMD Ryzen AI Max+ 395 processor. Its NPU was inaccessible while the Linux kernel boot parameter amd_iommu=off was active. After that parameter was removed and the system rebooted, XRT detected a RyzenAI-npu5 device with an 8-column topology. FastFlowLM then reported that the NPU stack was ready.
```

### 10.3 Test Q1 — Explicit fact extraction

```text
Read the following source. Answer with exactly three bullet points. Each bullet must state one fact explicitly present in the source. Do not infer, explain, or add information.

SOURCE:
The Corsair AI Workstation 300 uses an AMD Ryzen AI Max+ 395 processor. Its NPU was inaccessible while the Linux kernel boot parameter amd_iommu=off was active. After that parameter was removed and the system rebooted, XRT detected a RyzenAI-npu5 device with an 8-column topology. FastFlowLM then reported that the NPU stack was ready.
```

**Pass criteria**

- Exactly three bullets.
- Each bullet is explicitly grounded in the source.
- No causal claim or extra detail beyond the source.

**Observed baseline result:** Pass. The model returned three grounded bullets.

### 10.4 Test Q2 — Facts versus inference

```text
Using only the source below, produce exactly two sections titled FACTS and INFERENCE. FACTS must contain three bullet points copied or closely paraphrased from the source. INFERENCE must contain one cautious conclusion that follows from the facts. Do not add other sections.

SOURCE:
The Corsair AI Workstation 300 uses an AMD Ryzen AI Max+ 395 processor. Its NPU was inaccessible while the Linux kernel boot parameter amd_iommu=off was active. After that parameter was removed and the system rebooted, XRT detected a RyzenAI-npu5 device with an 8-column topology. FastFlowLM then reported that the NPU stack was ready.
```

**Pass criteria**

- Only the two named sections.
- FACTS has exactly three grounded bullet points.
- INFERENCE has exactly one cautious conclusion.
- No unsupported operational or causal claims.

**Observed baseline result:** Partial. The headings and three factual bullets appeared, but the model returned three inference bullets instead of one and used language that went beyond the supplied source.

### 10.5 Test Q3 — Executive brief

```text
Using only the source below, write an executive brief of no more than 70 words. Include: the problem, the corrective action, the evidence of success, and one limitation. Do not claim that model quality or benchmark speed has been tested.

SOURCE:
The Corsair AI Workstation 300 uses an AMD Ryzen AI Max+ 395 processor. Its NPU was inaccessible while the Linux kernel boot parameter amd_iommu=off was active. After that parameter was removed and the system rebooted, XRT detected a RyzenAI-npu5 device with an 8-column topology. FastFlowLM then reported that the NPU stack was ready.
```

**Pass criteria**

- 70 words or fewer.
- Identifies the problem and corrective action.
- Preserves XRT detection and/or FastFlowLM-ready evidence accurately.
- States a limitation supported by the prompt, such as no model-quality or benchmark-speed result.
- Makes no unsupported hardware claim.

**Observed baseline result:** Partial. The output covered the problem and action but reduced the evidence detail and introduced an unsupported limitation about underlying hardware constraints.

### 10.6 Optional long-form evaluation

Use the project evaluation artifact for a deeper test after the short suite:

- Faithful summary.
- Fact versus inference table.
- Constraint reconciliation.
- Decision critique.
- Prompt-injection resistance.
- Uncertainty-calibrated water-pump answer.
- Consistency check.
- Controlled creative extension.

Use the source's included grading rubric. Keep the model's context limit and prompt text constant across repeated runs.

### 10.7 Quality rubric

Score each row from 0 to 2.

| Dimension | 0 | 1 | 2 |
|---|---:|---:|---:|
| Grounded factual accuracy | Material error or invention | Mostly grounded; minor issue | Fully grounded |
| Format following | Ignores requested format | Partial compliance | Exact compliance |
| Constraint adherence | Violates major constraints | Minor violation | Meets all stated constraints |
| Useful synthesis | Vague or misleading | Understandable but thin | Clear, actionable, calibrated |

Interpretation:

| Score | Verdict |
|---:|---|
| 6–8 | Pass for narrow, supervised research tasks |
| 4–5 | Conditional pass; use strict templates and human review |
| 0–3 | NPU runtime may pass, but model is not suitable for this research-assistant task |

**Observed baseline score:** 5/8 — conditional pass.

### 10.8 Current usage recommendation

Appropriate uses:

- Extracting explicit facts from a short trusted source.
- Drafting a private local summary.
- Producing a first-pass status brief for human review.
- Starting from a blank page without sending source text to a cloud model.

Do not use without independent validation for:

- Hard output counts or formatting requirements.
- High-consequence executive reports.
- Root-cause or causal analysis.
- Precise fact-versus-inference distinctions.
- Autonomous agents that act on the output.

---

## 11. Phase G — Prove NPU offload

### 11.1 Objective

Show direct runtime evidence that FastFlowLM dispatched work to the AMD NPU. Do not rely only on the FastFlowLM startup text.

The primary evidence source is XRT's AIE-partition report.

### 11.2 Two-terminal method

#### Terminal 1: run FastFlowLM

```bash
flm run lfm2.5-it:1.2b --pmode performance --ctx-len 8192
```

Use a sufficiently long prompt so the monitor has time to refresh:

```text
Write a structured 500-word explanation of why local NPU inference can be useful in a home lab. Use six short titled sections. Include one practical limitation and do not mention this conversation.
```

#### Terminal 2: monitor XRT AIE partitions

```bash
watch -n 0.5 'clear; date; xrt-smi examine --report aie-partitions --verbose'
```

If the local XRT build does not support `--verbose` with this report:

```bash
watch -n 0.5 'clear; date; xrt-smi examine --report aie-partitions'
```

### 11.3 What to look for

Before model load or after the process exits, there should be no active FastFlowLM hardware contexts or allocated model partition.

During FastFlowLM model loading or token generation, look for:

- An AIE partition containing allocated NPU columns.
- One or more hardware contexts with `Active` status.
- A process PID associated with those contexts.
- Submission and completion counters increasing.
- Error counters at zero.
- Allocated columns returning to idle/released state when FastFlowLM exits.

### 11.4 Verified baseline offload evidence

A captured live report showed:

- Partition 0 using columns `[0, 1, 2, 3, 4, 5, 6, 7]`.
- Five active hardware contexts: IDs `1`, `2`, `3`, `4`, and `5`.
- PID `77769` associated with the contexts.
- Context 1: 2,563 submissions and 2,562 completions at the instant of capture.
- Context 2: 552 submissions and 552 completions.
- Context 3: 96 submissions and 96 completions.
- Context 4: 36 submissions and 36 completions.
- Context 5: 60 submissions and 60 completions.
- Zero errors for each context.
- Every NPU column 0–7 bound to context slots `[1, 2, 3, 4, 5]`.

Interpretation:

> FastFlowLM/XRT created active NPU hardware contexts, allocated the complete eight-column array, submitted thousands of work items, and completed them without reported errors. This is direct evidence of NPU offload.

A one-command difference between submissions and completions during a live refresh is expected: it indicates a command was still in flight at the moment of the snapshot.

### 11.5 Save before/during/after proof

```bash
mkdir -p ~/fastflowlm-reality-check/offload-proof

# Capture while FLM is idle or after the model exits.
xrt-smi examine --report aie-partitions --verbose \
  | tee ~/fastflowlm-reality-check/offload-proof/partitions-idle.txt

# Capture while FLM is actively generating a long answer.
xrt-smi examine --report aie-partitions --verbose \
  | tee ~/fastflowlm-reality-check/offload-proof/partitions-active.txt

# Exit FastFlowLM with Ctrl+C, then capture release state.
xrt-smi examine --report aie-partitions --verbose \
  | tee ~/fastflowlm-reality-check/offload-proof/partitions-released.txt
```

Optional telemetry view:

```bash
watch -n 0.5 'clear; date; xrt-smi examine --report telemetry'
```

Telemetry availability and displayed metrics vary by XRT version and platform. The AIE-partition/context report is the primary proof of offload.

### 11.6 Accurate on-camera language

Use:

> During FastFlowLM inference, XRT showed active NPU hardware contexts, full allocation across all eight NPU columns, thousands of completed submissions, and zero reported errors.

Avoid:

> The NPU is at 100%.

unless a supported monitoring metric explicitly supplies that percentage.

---

## 12. Optional server-mode experiment

Use server mode only after interactive validation succeeds.

```bash
flm serve lfm2.5-it:1.2b \
  --host 127.0.0.1 \
  --port 8000 \
  --pmode performance \
  --ctx-len 8192 \
  --cors 0
```

Notes:

- Keep `--host 127.0.0.1` for local-only access.
- Keep `--cors 0` unless a browser client specifically requires CORS.
- Use the offload monitor during requests.
- Do not expose the service externally as part of a first commissioning test.

---

## 13. Performance measurement plan

Quality and runtime validation come first. Once the pipeline is stable, capture performance separately.

### 13.1 Suggested measurement protocol

- Use the same model tag: `lfm2.5-it:1.2b`.
- Use the same `--pmode performance` setting.
- Use the same 8192-token context limit.
- Perform one warm-up prompt before timed runs.
- Run each fixed prompt three times.
- Report median and range, not one favorable run.
- Keep NPU-only conditions; do not run competing ROCm iGPU inference.

### 13.2 Measurements

| Metric | Definition |
|---|---|
| Cold load time | `flm run` command start to interactive prompt/model-ready state |
| First-token latency | Prompt submission to first visible output token |
| Generation rate | Tokens per second, if the runtime provides reliable token counts; otherwise record elapsed time and fixed output size |
| Stability | Number of complete task runs without crash, NPU reset, or accelerator fallback |
| NPU evidence | XRT contexts, column allocation, submission/completion progression, and error count |

### 13.3 Do not conflate versions

The baseline used FastFlowLM v1.0.1. If updating to a later FastFlowLM version, create a new experiment directory and repeat all key tests. Do not combine scores or throughput from distinct runtime versions.

---

## 14. Outcome template

### Environment

```text
Date:
Operator:
FastFlowLM version:
Model tag:
Model package path:
Ubuntu version:
Kernel:
XRT version:
amdxdna version:
NPU firmware:
NPU topology:
Power mode:
Context limit:
```

### Commissioning gates

| Gate | Pass/Fail/Partial | Evidence file | Notes |
|---|---|---|---|
| `/dev/accel/accel0` present | | | |
| `amdxdna` loaded | | | |
| IOMMU not forced off | | | |
| Memlock unlimited | | | |
| `xrt-smi examine` enumerates NPU | | | |
| `flm validate` ready | | | |
| Model files validate | | | |
| Model loads | | | |
| Model generates | | | |
| XRT offload evidence captured | | | |

### Quality scorecard

| Test | Grounded accuracy /2 | Format /2 | Constraints /2 | Synthesis /2 | Total /8 | Notes |
|---|---:|---:|---:|---:|---:|---|
| Smoke test | | | | | | |
| Q1 fact extraction | | | | | | |
| Q2 facts vs inference | | | | | | |
| Q3 executive brief | | | | | | |

### Overall verdict

Choose one:

- **Pass:** Operational NPU inference and quality sufficient for narrow, human-supervised research tasks.
- **Conditional pass:** NPU inference is operational, but format adherence, factual calibration, stability, or setup friction requires strict templates and human review.
- **Fail:** NPU is not operationally accessible, model cannot run reliably, or output is not useful for the intended task.

Baseline verdict:

> **Conditional pass.** FastFlowLM and the Liquid LFM2.5 instruction model run on the workstation's AMD NPU with direct XRT hardware-context evidence. The model handles simple explicit fact extraction but is inconsistent with strict formatting, output counts, and source-bounded inference; use it as a local first-pass draft assistant with human review.

---

## 15. YouTube narrative outline

1. **Cold open:** “Can an AMD NPU do useful local LLM work, or is it just a sticker?”
2. **Starting state:** FastFlowLM installed; generic LFM2.5 GGUF present; NPU still not automatically usable.
3. **Failure discovery:** FLM validation initially fails despite visible hardware.
4. **Root cause:** Linux booted with `amd_iommu=off`, blocking the SVA path needed by the NPU.
5. **Repair:** Remove only that GRUB parameter, regenerate GRUB, reboot, validate XRT and FastFlowLM.
6. **Model:** Pull/check/load `lfm2.5-it:1.2b` as FastFlowLM's NPU-native package.
7. **Quality test:** Show success on fact extraction and failures/partials on strict formatting and source-bounded inference.
8. **Offload proof:** XRT report shows active contexts, all eight columns allocated, thousands of submissions/completions, and zero errors.
9. **Verdict:** The NPU is real and running local inference, but a 1.2B model remains a supervised draft helper—not an autonomous technical analyst.

Suggested final line:

> The NPU is no longer a sticker on the box. It is running a real local model, and XRT proves the work reached the accelerator. But local inference success is not the same as autonomous judgment: use the small model to create a reviewable first draft, then let a human make the call.
