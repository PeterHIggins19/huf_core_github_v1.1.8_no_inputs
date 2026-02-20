\
# Higgins Unity Framework: Mathematical form and function

This page is the “math spine” that connects the HUF contract (artifacts + stability packet) to a minimal formal model.

> **Not ML class imbalance:** here “long tail” means **mass distribution + exception reweighting** (baseline vs filtered view).

## 1) The object HUF normalizes

HUF starts from a **non‑negative contribution table** and turns it into a unity budget.

- Finite elements: indices \(i = 1..N\)
- Raw contributions: \(w_i \ge 0\)
- Unity‑budget weights (“mass share” or “energy share”):
  - **Mass**: \(\rho_i = \frac{w_i}{\sum_k w_k}\)
  - **Energy / Parseval**: \(\rho_i = \frac{|x_i|^2}{\sum_k |x_k|^2}\)

### Proof sketch: unity is enforced
Let \(S = \sum_k w_k\). Then:
- \(\rho_i \ge 0\) because \(w_i \ge 0\)
- \(\sum_i \rho_i = \sum_i \frac{w_i}{S} = \frac{1}{S}\sum_i w_i = 1\)

This is the core invariant HUF treats as sacred: **global unity**.

## 2) Regimes (local views that stay auditable)

A **regime** is a partition (or nested partition) of finite elements:
- Regimes \(R_1, \dots, R_m\) where \(R_j \subseteq \{1..N\}\)
- Regime mass:
  \[
  \rho(R_j) = \sum_{i \in R_j} \rho_i
  \]

The **coherence map** artifact is exactly “\(\rho(R_j)\) for all regimes” plus ranking, so you can answer:
> “Where did the budget go?”

## 3) Exclusion / reduction as a truncation operator

Most practical HUF runs *reduce* the system to an auditable subset.

### 3.1 Threshold form (τ)
Define a truncation operator:
\[
T_\tau(\rho)_i = \rho_i \cdot \mathbf{1}[\rho_i \ge \tau]
\]

Discarded budget (explicitly reported in `artifact_4_error_budget.json`):
\[
\delta(\tau) = 1 - \sum_i T_\tau(\rho)_i
\]

Renormalized retained distribution:
\[
\hat\rho_i(\tau) = \frac{T_\tau(\rho)_i}{\sum_k T_\tau(\rho)_k}
\]

**Proof sketch (renormalized unity):**
\[
\sum_i \hat\rho_i(\tau) = \frac{\sum_i T_\tau(\rho)_i}{\sum_k T_\tau(\rho)_k} = 1
\]

This is why HUF can be “compression + audit”: you can *discard* mass, but you must (1) declare it, and (2) renormalize what remains.

### 3.2 Retained‑target form (α)
Sometimes you don’t choose \(\tau\) directly. You choose a retained target \(\alpha\) (e.g. 0.90), and HUF keeps the **smallest** set \(K\) such that:
\[
\sum_{i \in K} \rho_i \ge \alpha
\]

Operationally: sort by \(\rho_i\) descending; take the shortest prefix that reaches \(\alpha\).

This is exactly the “**items to cover 90%**” headline used in the long‑tail demo:
- baseline run: items_to_cover_90pct = 37
- anomaly run: items_to_cover_90pct = 12  
→ concentration increased.

## 4) Fixed points (why the cycle is stable)

### 4.1 Normalization is idempotent on the simplex
Define normalization:
\[
N(w) = \frac{w}{\sum_k w_k}
\]

If \(\rho\) already satisfies \(\sum \rho = 1\), then:
\[
N(\rho) = \rho
\]
So **all unity‑budget distributions are fixed points** of \(N\).

### 4.2 A Lyapunov view (stability to unity)
A simple “distance to unity” function:
\[
V(\rho) = 1 - \sum_i \rho_i
\]
After normalization, \(V(\rho)=0\). Any drift away from unity is measurable, correctable, and auditable.

In practice, HUF treats “unity drift” as a **bug**: either a numerical issue (float accumulation) or a forbidden operation (non‑conservative propagation).

## 5) Information theory (optional, but useful)

Once \(\rho\) is a probability‑like distribution, information tools become usable:

### 5.1 Entropy as “concentration”
\[
H(\rho) = -\sum_i \rho_i \log \rho_i
\]

- High entropy → diffuse mass (less concentrated)
- Low entropy → concentrated mass (few items dominate)

A friendly scalar is the **effective number of items**:
\[
N_{\mathrm{eff}} = \exp(H(\rho))
\]
When your anomaly run concentrates, \(H\) tends to drop and \(N_{\mathrm{eff}}\) shrinks.

### 5.2 Regime shift as divergence
Let \(\rho^{(base)}\) be baseline (Traffic Phase) and \(\rho^{(anom)}\) be exception view (Traffic Anomaly). A regime‑shift measure is KL divergence:
\[
D_{KL}(\rho^{(anom)} \Vert \rho^{(base)}) = \sum_i \rho^{(anom)}_i \log \frac{\rho^{(anom)}_i}{\rho^{(base)}_i}
\]
You don’t need this to run HUF — but it’s a clean way to quantify “the mass moved”.

## 6) How this maps to the three “artifact-first” pillars

HUF’s elevator pitch is not “math for math’s sake.” It’s math that *forces auditability*:

- **Coherence map** → \(\rho(R_j)\) (where the budget went, by regime)
- **Active set** → \(K\) (what you kept, explicitly)
- **Trace report** → provenance map (why each kept item is kept, and what it came from)

If you can’t show all three, you’re not doing HUF — you’re doing storytelling.

## Next
- For the accounting‑facing explanation and the baseline→exception→variance flow, see:
  - **Long tail (accounting lens)** (`docs/long_tail_accounting_lens.md`)
- For command discovery and artifact labels, see:
  - **CLI command lists + terminology** (`docs/cli_huf_reference.md`)
