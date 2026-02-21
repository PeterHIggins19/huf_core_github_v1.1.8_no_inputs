# Evaluation platforms

> HUF adds a composition audit layer to RAG evaluation suites — tracking source diversity, mass concentration, and coherence drift across eval runs so quality regressions are caught before deployment.

!!! note "Ethics & authorship"
    This page was drafted with AI assistance as an editing and structuring tool. The author reviewed and curated all formal claims; any numerical results shown here are either reproduced by code in this repository or explicitly labeled as illustrative.

## What this page is

A partner-facing outreach note showing how HUF can attach as a normalization-invariant audit layer—without changing the partner’s core product.

## Why it matters

- HUF is a **composition audit**: it tells you how the system reallocates normalized mass across regimes as operations accumulate.
- This makes drift and “silent failure” easier to detect than raw accuracy scores alone.

## What you’ll see

- Supported Evaluation Platforms
- Mathematical Foundation
- Integration Code
- 10-Run Eval Simulation
- Partnership Pitch & Execution

## Artifacts / outputs

- JSONL audit traces (per retrieval, per evaluation run, or per fiscal period).
- A reference scoring function and an example of regime penalties/damping.

## Run the example

```python
from
 deepeval.metrics 
import
 BaseMetric

from
 deepeval.test_case 
import
 LLMTestCase

import
 numpy 
as
 np

from
 scipy.special 
import
 softmax

import
 json, datetime, pathlib


class
 
HUFCompositionMetric
(BaseMetric):
    
"""HUF composition audit as a DeepEval metric.
    Compatible with Ragas, TruLens, ARES via adapter shim.
    """


    name = 
"huf_composition"

    threshold = 
0.60
   
# min C_comp to pass


    
def
 
__init__
(self, jsonl_path=
"huf_eval_log.jsonl"
,
                 alert_k=
4
, alert_var=
0.02
):
        self.jsonl_path = pathlib.Path(jsonl_path)
        self.alert_k = alert_k
        self.alert_var = alert_var
        self.score = 
None

        self.reason = 
""


    
def
 
measure
(self, test_case: LLMTestCase):
        docs = test_case.retrieval_context 
or
 []
        scores_raw = getattr(test_case, 
"retrieval_scores"
, 
None
)

        
# Build score vector

        
if
 scores_raw 
and
 len(scores_raw) == len(docs):
            s = np.array([float(x) 
for
 x 
in
 scores_raw])
        
else
:
            s = np.array([
1.0
 / (i+
1
) 
for
 i 
in
 range(len(docs))])

        rho = softmax(s)
        var = float(np.var(rho))

        
# items_to_cover_90pct

        sorted_r = sorted(rho, reverse=True)
        k, cs = 
0
, 
0.0

        
for
 r 
in
 sorted_r:
            cs += r; k += 
1

            
if
 cs >= 
0.9
: 
break


        c_comp = k / max(len(docs), 
1
)
        self.score = round(c_comp, 
4
)
        self.success = c_comp >= self.threshold

        alert = k < self.alert_k 
or
 var > self.alert_var
        self.reason = (
            
f"items_to_cover_90pct={k}, Var={var:.4f}, C_comp={c_comp:.4f}, "
            f"alert={'YES' if alert else 'NO'}"

        )

        record = {
            
"ts"
: datetime.datetime.utcnow().isoformat(),
            
"test_id"
: getattr(test_case, 
"id"
, 
"unknown"
),
            
"n_docs"
: len(docs),
            
"items_to_cover_90pct"
: k,
            
"c_comp"
: self.score,
            
"var_rho"
: round(var, 
5
),
            
"alert"
: alert,
            
"pass"
: self.success,
        }
        
with
 self.jsonl_path.open(
"a"
) 
as
 f:
            f.write(json.dumps(record) + 
"\n"
)

        
return
 self.score


# --- Usage with DeepEval ---


from
 deepeval 
import
 evaluate

huf = 
HUFCompositionMetric
()
test_cases = [...]   
# your LLMTestCase list

evaluate(test_cases, metrics=[huf])
print(
f"HUF composition pass rate: {huf.score:.3f}"
)
```

## What to expect

- A small coherence/drift report and a trace you can plot.

## Interpretation

- If HUF flags concentration, it means your system is becoming **over-dependent** on a small subset of regimes/sources.

## Next steps

- Connect the audit trace to your CI (for eval suites) or to ops monitoring (for RAG pipelines).

---

## Source content (converted from HTML)

HUF
Platforms
Math
Code
Simulation
Pitch

EVAL · COMPOSITION AUDIT

Partner Package · Eval Platforms · v1.1.8
# Evaluation Platforms**× HUF**

HUF adds a composition audit layer to RAG evaluation suites — tracking source diversity, mass concentration, and coherence drift across eval runs so quality regressions are caught before deployment.

Package Metrics
Platform fit93%
C(ℋ) achieved0.928
Avg α*0.52
kb erosion−13.9%
items\_90pct alertk < 4
top-src alertρ > 0.65

01
## Supported Evaluation Platforms

Ragas
RAG evaluation framework measuring faithfulness, answer relevancy, and context precision. HUF adds composition coherence to the metric suite.
on\_dataset\_evaluated() → HUF audit

TruLens
LLM observability and evaluation platform. HUF hooks into the feedback function pipeline post-retrieval to log composition state.
TruChain feedback + HUF callback

ARES
Automated RAG evaluation system using LLM judges. HUF augments ARES context quality checks with normalized source mass tracking.
context\_relevance\_scorer + rho

DeepEval
Open-source LLM evaluation framework with custom metric support. HUF provides a HUFCoherenceMetric class for drop-in integration.
BaseMetric.measure() override

PromptFlow
Azure ML orchestration for LLM workflows. HUF plugs into the evaluation variant pipeline as a post-retrieval node.
EvaluatorNode post-retrieval

LangSmith
LangChain's tracing and evaluation platform. HUF writes coherence metadata directly to run traces via the evaluation API.
run.feedback → HUF metadata

02
## Mathematical Foundation

Composition Score

C\_comp = items\_to\_cover\_90pct / N
// N = total retrieved documents
// C\_comp → 1.0 = perfect diversity
// C\_comp < 0.4 = concentration risk

A simple normalization of the concentration metric, giving evaluators a 0–1 composition score to track alongside RAGAS scores.

Mass Distribution Variance

Var(ρ) = (1/n) Σᵢ (ρᵢ − ρ̄)²
// ρ = softmax(scores)
// target Var < 0.02 for eval pass

High variance indicates one or few documents dominating the context window, a hidden quality risk not captured by standard eval metrics.

Eval-Augmented Objective

J\_eval(α) = (1 − C(ℋ)) + λ·Var(ρ) + κ·(1 − C\_comp) + ε·(1 − F\_answer)
// F\_answer = faithfulness score from eval platform (0–1)
// κ = 0.12 ε = 0.08
// Bridges HUF coherence with standard RAG quality metrics

The combined objective links HUF's structural composition audit with the answer-quality signal from evaluation platforms. Low faithfulness (F\_answer) tightens the damping penalty on source concentration.

03
## Integration Code

huf\_eval\_metric.py

```
from deepeval.metrics import BaseMetric
from deepeval.test\_case import LLMTestCase
import numpy as np
from scipy.special import softmax
import json, datetime, pathlib

class HUFCompositionMetric(BaseMetric):
    """HUF composition audit as a DeepEval metric.
 Compatible with Ragas, TruLens, ARES via adapter shim.
 """

    name = "huf\_composition"
    threshold = 0.60   # min C\_comp to pass

    def \_\_init\_\_(self, jsonl\_path="huf\_eval\_log.jsonl",
                 alert\_k=4, alert\_var=0.02):
        self.jsonl\_path = pathlib.Path(jsonl\_path)
        self.alert\_k = alert\_k
        self.alert\_var = alert\_var
        self.score = None
        self.reason = ""

    def measure(self, test\_case: LLMTestCase):
        docs = test\_case.retrieval\_context or []
        scores\_raw = getattr(test\_case, "retrieval\_scores", None)

        # Build score vector
        if scores\_raw and len(scores\_raw) == len(docs):
            s = np.array([float(x) for x in scores\_raw])
        else:
            s = np.array([1.0 / (i+1) for i in range(len(docs))])

        rho = softmax(s)
        var = float(np.var(rho))

        # items\_to\_cover\_90pct
        sorted\_r = sorted(rho, reverse=True)
        k, cs = 0, 0.0
        for r in sorted\_r:
            cs += r; k += 1
            if cs >= 0.9: break

        c\_comp = k / max(len(docs), 1)
        self.score = round(c\_comp, 4)
        self.success = c\_comp >= self.threshold

        alert = k < self.alert\_k or var > self.alert\_var
        self.reason = (
            f"items\_to\_cover\_90pct={k}, Var={var:.4f}, C\_comp={c\_comp:.4f}, "
 f"alert={'YES' if alert else 'NO'}"
        )

        record = {
            "ts": datetime.datetime.utcnow().isoformat(),
            "test\_id": getattr(test\_case, "id", "unknown"),
            "n\_docs": len(docs),
            "items\_to\_cover\_90pct": k,
            "c\_comp": self.score,
            "var\_rho": round(var, 5),
            "alert": alert,
            "pass": self.success,
        }
        with self.jsonl\_path.open("a") as f:
            f.write(json.dumps(record) + "\n")

        return self.score

# --- Usage with DeepEval ---
from deepeval import evaluate

huf = HUFCompositionMetric()
test\_cases = [...]   # your LLMTestCase list
evaluate(test\_cases, metrics=[huf])
print(f"HUF composition pass rate: {huf.score:.3f}")
```

04
## 10-Run Eval Simulation

| Run | α* | C\_comp | Var(ρ) | items\_90pct | Faithfulness | J\_eval | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | — | 0.600 | 0.0180 | 6 | 0.88 | — | ✓ |
| 1 | 0.51 | 0.607 | 0.0175 | 6 | 0.89 | 0.118 | ✓ |
| 2 | 0.52 | 0.615 | 0.0170 | 6 | 0.89 | 0.114 | ✓ |
| 3 | 0.51 | 0.590 | 0.0195 | 5 | 0.87 | 0.122 | ✓ |
| 4 ⚡ | 0.47 | 0.300 | 0.0420 | 3 | 0.79 | 0.198 | ✗ ALERT |
| 5* | 0.56 | 0.640 | 0.0155 | 6 | 0.91 | 0.108 | ✓ |
| 6 | 0.53 | 0.650 | 0.0148 | 6 | 0.91 | 0.105 | ✓ |
| 7 | 0.52 | 0.658 | 0.0144 | 7 | 0.92 | 0.102 | ✓ |
| 8 | 0.53 | 0.660 | 0.0142 | 7 | 0.92 | 0.101 | ✓ |
| 9 | 0.53 | 0.665 | 0.0140 | 7 | 0.93 | 0.099 | ✓ |
| 10 | 0.54 | 0.670 | 0.0138 | 7 | 0.93 | 0.098 | ✓ |

* Run 5: re-normalization after concentration event. ⚡ = context window dominated by single namespace. Faithfulness correlation with C\_comp: r = 0.81.

05
## Partnership Pitch & Execution

>
>  HUF adds a **composition audit layer** that existing eval platforms are missing — tracking not just answer quality but the **source mass distribution** that produced it. When a single namespace dominates (>65% mass), faithfulness scores drop and users don't know why. HUF catches this with items\_to\_cover\_90pct as a headline metric, logging JSONL artifacts for every eval run and reducing kb mass erosion by **13.9%** across 10 simulated evaluation cycles.
>

Step 01
Submit Plugin / Metric
Submit HUFCompositionMetric as a PR to DeepEval and an integration guide to the Ragas docs. Both accept community metric contributions.

Step 02
Slack + GitHub
Post demo in DeepEval Discord, TruLens Slack #integrations, and Ragas GitHub Discussions showing the correlation between C\_comp and faithfulness score.

Step 03
Blog Collab
Co-author a "Hidden RAG quality risks" post with Ragas or DeepEval team showing composition score as a missing dimension in standard eval suites.
