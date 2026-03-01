// HUF-DOC: HUF.DRAFT.SOFTWARE.CODE.HUF_DIAGNOSTIC | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:draft | RO:Peter Higgins
// CODES: SOFTWARE, UI | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:notes/code_snippets/huf_code/huf_diagnostic.jsx

import { useState, useCallback } from "react";

// ─── HUF COMPLIANCE ENGINE ─────────────────────────────────────────────────

function runDiagnostic(system) {
  const results = [];
  const { elements, cycles, systemName } = system;
  const current = cycles[cycles.length - 1];
  const previous = cycles.length > 1 ? cycles[cycles.length - 2] : null;

  // ── TEST 1: UNITY ──────────────────────────────────────────────────────
  const shareSum = elements.reduce((s, e) => s + (parseFloat(e.share) || 0), 0);
  const unitPass = Math.abs(shareSum - 1.0) < 0.011;
  results.push({
    id: "T1",
    name: "UNITY CONSTRAINT",
    description: "All element shares must sum to 1.0. This is the budget ceiling test — the system must account for 100% of its allocation.",
    status: unitPass ? "PASS" : "FAIL",
    detail: unitPass
      ? `Share sum = ${shareSum.toFixed(4)}. Budget ceiling fully accounted.`
      : `Share sum = ${shareSum.toFixed(4)}. ${shareSum > 1 ? "Overallocation detected" : "Unaccounted allocation detected"} — ${Math.abs(1 - shareSum).toFixed(4)} ${shareSum > 1 ? "above" : "below"} ceiling. Silent mass exists outside the declared ratio state.`,
    vocabulary: ["budget ceiling", "share", "ratio state"],
  });

  // ── TEST 2: DECLARATION ────────────────────────────────────────────────
  const missingWeights = elements.filter(e => !e.declaredWeight || e.declaredWeight === "");
  const weightSum = elements.reduce((s, e) => s + (parseFloat(e.declaredWeight) || 0), 0);
  const weightSumOk = Math.abs(weightSum - 1.0) < 0.011;
  const declarePass = missingWeights.length === 0 && weightSumOk;
  const declarePartial = missingWeights.length === 0 && !weightSumOk;
  results.push({
    id: "T2",
    name: "DECLARED WEIGHTS",
    description: "Every element must have a declared weight — the operator's stated intention for that element's share. Without declared weights, silent drift cannot be distinguished from intentional reweighting.",
    status: declarePass ? "PASS" : declarePartial ? "PARTIAL" : "FAIL",
    detail: declarePass
      ? `All ${elements.length} elements have declared weights. Weight sum = ${weightSum.toFixed(4)}. Self-referential reference is established.`
      : missingWeights.length > 0
      ? `${missingWeights.length} element(s) missing declared weights: ${missingWeights.map(e => e.name).join(", ")}. Without declaration, any share change is unclassifiable.`
      : `All elements declared but weight sum = ${weightSum.toFixed(4)}. Declared weights must also satisfy the unity constraint.`,
    vocabulary: ["declared weight", "silent drift", "intentional reweighting"],
  });

  // ── TEST 3: DRIFT DETECTION ────────────────────────────────────────────
  const driftItems = elements.map(e => {
    const share = parseFloat(e.share) || 0;
    const declared = parseFloat(e.declaredWeight) || 0;
    const gap = share - declared;
    return { name: e.name, share, declared, gap, traced: e.traced };
  });
  const significantDrift = driftItems.filter(d => Math.abs(d.gap) >= 0.05);
  const untracedDrift = significantDrift.filter(d => !d.traced);
  const allTraced = untracedDrift.length === 0;
  const driftStatus = significantDrift.length === 0 ? "PASS" : allTraced ? "PARTIAL" : "FAIL";
  results.push({
    id: "T3",
    name: "DRIFT CLASSIFICATION",
    description: "Every significant share gap (≥5 points) between observed share and declared weight must be classified as intentional (traced to a decision) or silent (no trace entry). Unclassified drift is the primary failure mode HUF is designed to detect.",
    status: driftStatus,
    detail: significantDrift.length === 0
      ? `No significant drift detected. All elements within 5 points of declared weight. System is near ground state.`
      : allTraced
      ? `${significantDrift.length} drift item(s) detected, all classified as intentional reweighting with trace entries. Drift is visible and accountable.`
      : `${untracedDrift.length} SILENT DRIFT item(s) detected:\n${untracedDrift.map(d => `  ${d.name}: observed ${(d.share * 100).toFixed(1)}% vs declared ${(d.declared * 100).toFixed(1)}% (gap: ${d.gap > 0 ? "+" : ""}${(d.gap * 100).toFixed(1)}pp) — NO TRACE`).join("\n")}`,
    vocabulary: ["silent drift", "intentional reweighting", "trace", "declared weight"],
    driftItems,
    significantDrift,
    untracedDrift,
  });

  // ── TEST 4: CONCENTRATION ──────────────────────────────────────────────
  const sorted = [...elements].sort((a, b) => (parseFloat(b.share) || 0) - (parseFloat(a.share) || 0));
  let cumulative = 0;
  let proofCount = 0;
  for (const el of sorted) {
    cumulative += parseFloat(el.share) || 0;
    proofCount++;
    if (cumulative >= 0.9) break;
  }
  const expectedProof = Math.ceil(elements.length * 0.4);
  const concentrated = proofCount <= Math.max(1, Math.floor(elements.length * 0.25)) && elements.length > 3;
  results.push({
    id: "T4",
    name: "CONCENTRATION DETECTION",
    description: "Measures how many elements cover 90% of total share (PROOF line). A healthy portfolio distributes mass according to declared weights. Concentration means a small number of elements are dominating the budget ceiling.",
    status: concentrated ? "FLAG" : "PASS",
    detail: `PROOF line: ${proofCount} of ${elements.length} elements cover 90% share.\n${concentrated ? `CONCENTRATION DETECTED: ${proofCount} element(s) hold the majority of portfolio share. Compare to declared weights — is this intentional? Check for silent reweighting toward dominant elements.` : `Distribution appears consistent with portfolio size. No concentration anomaly detected.`}`,
    vocabulary: ["concentration", "share", "silent reweighting", "budget ceiling"],
    proofCount,
    totalElements: elements.length,
  });

  // ── TEST 5: FRAGMENTATION ──────────────────────────────────────────────
  const threshold = 1 / (elements.length * 3);
  const fragmented = elements.filter(e => (parseFloat(e.share) || 0) < threshold && (parseFloat(e.declaredWeight) || 0) >= threshold);
  results.push({
    id: "T5",
    name: "FRAGMENTATION DETECTION",
    description: "Elements with share far below their declared weight may be too fragmented to function effectively. The reciprocal reading of the unity constraint makes fragmentation visible on the same instrument as concentration.",
    status: fragmented.length > 0 ? "FLAG" : "PASS",
    detail: fragmented.length > 0
      ? `${fragmented.length} element(s) below functional threshold (< ${(threshold * 100).toFixed(1)}% share):\n${fragmented.map(e => `  ${e.name}: ${((parseFloat(e.share) || 0) * 100).toFixed(1)}% observed vs ${((parseFloat(e.declaredWeight) || 0) * 100).toFixed(1)}% declared`).join("\n")}\nThese elements may be receiving insufficient allocation to operate at declared priority.`
      : `No fragmentation detected. All elements above functional threshold relative to declared weights.`,
    vocabulary: ["fragmentation", "share", "declared weight"],
  });

  // ── TEST 6: CYCLE HISTORY ──────────────────────────────────────────────
  results.push({
    id: "T6",
    name: "CROSS-CYCLE OBSERVATION",
    description: "HUF requires at least two cycles to distinguish phase from contribution. A single snapshot cannot detect silent drift — drift is a change in ratio state across cycles, not a property of any single observation.",
    status: cycles.length >= 2 ? "PASS" : "FAIL",
    detail: cycles.length >= 2
      ? `${cycles.length} cycle(s) on record. Cross-cycle comparison is available. Phase can be distinguished from contribution for elements with characteristic periods ≤ ${cycles.length} cycle(s).`
      : `Single cycle only. This is a snapshot. Snapshot observation cannot detect silent drift, cannot distinguish phase from contribution, and cannot identify correction oscillation. Minimum requirement: 2 cycles.`,
    vocabulary: ["cycle", "phase", "characteristic period", "silent drift"],
  });

  // ── TEST 7: CHARACTERISTIC PERIODS ─────────────────────────────────────
  const missingPeriods = elements.filter(e => !e.characteristicPeriod || e.characteristicPeriod === "");
  results.push({
    id: "T7",
    name: "CHARACTERISTIC PERIODS",
    description: "Each element should have a declared characteristic period — the time required to see its full contribution. Elements observed for less than one full characteristic period are susceptible to the phase misread failure mode.",
    status: missingPeriods.length === 0 ? "PASS" : missingPeriods.length < elements.length ? "PARTIAL" : "FAIL",
    detail: missingPeriods.length === 0
      ? `All ${elements.length} elements have declared characteristic periods. Phase misread risk is quantifiable.`
      : `${missingPeriods.length} element(s) missing characteristic periods: ${missingPeriods.map(e => e.name).join(", ")}. These elements cannot be assessed for phase misread risk. High-value, low-frequency contributors are most susceptible.`,
    vocabulary: ["characteristic period", "phase", "ratio blindness"],
  });

  // ── TEST 8: GROUND STATE ───────────────────────────────────────────────
  const totalGap = driftItems.reduce((s, d) => s + Math.abs(d.gap), 0) / 2;
  const groundPass = totalGap < 0.05;
  const groundPartial = totalGap >= 0.05 && totalGap < 0.15;
  results.push({
    id: "T8",
    name: "GROUND STATE ASSESSMENT",
    description: "Ground state is reached when observed shares match declared weights across all elements and the change log shows no silent drift. It is the ratio state in which the system's behavior matches its declared intent.",
    status: groundPass ? "PASS" : groundPartial ? "PARTIAL" : "FAIL",
    detail: groundPass
      ? `Mean drift gap = ${(totalGap * 100).toFixed(1)}pp. System is at or near ground state. Ratio state matches declared intent.`
      : `Mean drift gap = ${(totalGap * 100).toFixed(1)}pp. ${groundPartial ? "System is approaching ground state but drift remains." : "System is not at ground state."} The gap between declared weights and observed shares represents the accumulated distance from self-governing condition.`,
    vocabulary: ["ground state", "declared weight", "ratio state", "silent drift"],
  });

  // ── OVERALL ────────────────────────────────────────────────────────────
  const passes = results.filter(r => r.status === "PASS").length;
  const fails = results.filter(r => r.status === "FAIL").length;
  const flags = results.filter(r => r.status === "FLAG" || r.status === "PARTIAL").length;
  const hufCompliant = fails === 0 && flags <= 1;
  const hufCapable = fails <= 1;

  return {
    results,
    summary: { passes, fails, flags, hufCompliant, hufCapable, totalTests: results.length },
    driftItems,
  };
}

// ─── COMPONENTS ────────────────────────────────────────────────────────────

const STATUS_COLORS = {
  PASS: "#4ade80",
  FAIL: "#f87171",
  FLAG: "#fbbf24",
  PARTIAL: "#fb923c",
};

const STATUS_BG = {
  PASS: "rgba(74,222,128,0.08)",
  FAIL: "rgba(248,113,113,0.08)",
  FLAG: "rgba(251,191,36,0.08)",
  PARTIAL: "rgba(251,146,60,0.08)",
};

function StatusBadge({ status }) {
  return (
    <span style={{
      fontFamily: "monospace",
      fontSize: "11px",
      fontWeight: 700,
      letterSpacing: "0.12em",
      padding: "3px 8px",
      borderRadius: "2px",
      border: `1px solid ${STATUS_COLORS[status]}`,
      color: STATUS_COLORS[status],
      background: STATUS_BG[status],
    }}>
      {status}
    </span>
  );
}

function TestCard({ test, index }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{
      border: `1px solid ${open ? STATUS_COLORS[test.status] : "rgba(255,255,255,0.08)"}`,
      borderLeft: `3px solid ${STATUS_COLORS[test.status]}`,
      borderRadius: "4px",
      marginBottom: "8px",
      background: open ? STATUS_BG[test.status] : "rgba(255,255,255,0.02)",
      transition: "all 0.2s",
      cursor: "pointer",
    }} onClick={() => setOpen(!open)}>
      <div style={{ padding: "12px 16px", display: "flex", alignItems: "center", gap: "12px" }}>
        <span style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.3)", minWidth: "24px" }}>
          {test.id}
        </span>
        <StatusBadge status={test.status} />
        <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: "12px", fontWeight: 600, letterSpacing: "0.08em", color: "rgba(255,255,255,0.85)", flex: 1 }}>
          {test.name}
        </span>
        <span style={{ color: "rgba(255,255,255,0.3)", fontSize: "12px" }}>{open ? "▲" : "▼"}</span>
      </div>
      {open && (
        <div style={{ padding: "0 16px 16px 52px" }}>
          <p style={{ fontFamily: "Georgia, serif", fontSize: "13px", color: "rgba(255,255,255,0.6)", lineHeight: 1.6, marginBottom: "12px" }}>
            {test.description}
          </p>
          <pre style={{
            fontFamily: "'IBM Plex Mono', monospace",
            fontSize: "12px",
            color: STATUS_COLORS[test.status],
            background: "rgba(0,0,0,0.3)",
            padding: "12px",
            borderRadius: "3px",
            whiteSpace: "pre-wrap",
            marginBottom: "10px",
            lineHeight: 1.6,
          }}>
            {test.detail}
          </pre>
          {test.vocabulary && (
            <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
              <span style={{ fontSize: "10px", color: "rgba(255,255,255,0.3)", fontFamily: "monospace", marginRight: "4px" }}>VOCABULARY:</span>
              {test.vocabulary.map(v => (
                <span key={v} style={{
                  fontSize: "10px",
                  fontFamily: "monospace",
                  padding: "2px 6px",
                  border: "1px solid rgba(255,200,100,0.3)",
                  borderRadius: "2px",
                  color: "rgba(255,200,100,0.7)",
                }}>
                  {v}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function ElementRow({ element, onChange, onRemove, index }) {
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "1fr 90px 90px 80px 120px 32px",
      gap: "6px",
      marginBottom: "6px",
      alignItems: "center",
    }}>
      {[
        { key: "name", placeholder: "Element name", type: "text" },
        { key: "share", placeholder: "0.00", type: "number", step: "0.01" },
        { key: "declaredWeight", placeholder: "0.00", type: "number", step: "0.01" },
        { key: "characteristicPeriod", placeholder: "cycles", type: "number" },
      ].map(field => (
        <input
          key={field.key}
          type={field.type}
          step={field.step}
          placeholder={field.placeholder}
          value={element[field.key] || ""}
          onChange={e => onChange(index, field.key, e.target.value)}
          style={inputStyle}
        />
      ))}
      <label style={{ display: "flex", alignItems: "center", gap: "6px", cursor: "pointer" }}>
        <input
          type="checkbox"
          checked={element.traced || false}
          onChange={e => onChange(index, "traced", e.target.checked)}
          style={{ accentColor: "#4ade80" }}
        />
        <span style={{ fontSize: "10px", fontFamily: "monospace", color: "rgba(255,255,255,0.4)" }}>TRACED</span>
      </label>
      <button onClick={() => onRemove(index)} style={{
        background: "none",
        border: "1px solid rgba(248,113,113,0.3)",
        color: "rgba(248,113,113,0.7)",
        borderRadius: "2px",
        cursor: "pointer",
        fontSize: "14px",
        padding: "2px 6px",
      }}>×</button>
    </div>
  );
}

const inputStyle = {
  background: "rgba(255,255,255,0.04)",
  border: "1px solid rgba(255,255,255,0.1)",
  borderRadius: "3px",
  padding: "7px 10px",
  color: "rgba(255,255,255,0.85)",
  fontFamily: "'IBM Plex Mono', monospace",
  fontSize: "12px",
  outline: "none",
  width: "100%",
  boxSizing: "border-box",
};

const btnStyle = {
  background: "rgba(255,180,50,0.1)",
  border: "1px solid rgba(255,180,50,0.4)",
  color: "rgba(255,200,80,0.9)",
  padding: "9px 18px",
  fontFamily: "'IBM Plex Mono', monospace",
  fontSize: "12px",
  fontWeight: 600,
  letterSpacing: "0.08em",
  cursor: "pointer",
  borderRadius: "3px",
};

// ─── MAIN APP ───────────────────────────────────────────────────────────────

export default function HUFDiagnostic() {
  const [step, setStep] = useState(1);
  const [systemName, setSystemName] = useState("");
  const [cycleName, setCycleName] = useState("");
  const [numCycles, setNumCycles] = useState(1);
  const [elements, setElements] = useState([
    { name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false },
    { name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false },
    { name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false },
  ]);
  const [report, setReport] = useState(null);

  const addElement = () => setElements([...elements, { name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false }]);
  const removeElement = (i) => setElements(elements.filter((_, idx) => idx !== i));
  const updateElement = (i, key, val) => {
    const updated = [...elements];
    updated[i] = { ...updated[i], [key]: val };
    setElements(updated);
  };

  const runTest = () => {
    const validElements = elements.filter(e => e.name.trim());
    const system = {
      systemName,
      elements: validElements,
      cycles: Array.from({ length: numCycles }, (_, i) => ({ id: i + 1 })),
    };
    const result = runDiagnostic(system);
    setReport(result);
    setStep(3);
  };

  const shareTotal = elements.reduce((s, e) => s + (parseFloat(e.share) || 0), 0);
  const weightTotal = elements.reduce((s, e) => s + (parseFloat(e.declaredWeight) || 0), 0);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0f",
      color: "rgba(255,255,255,0.85)",
      fontFamily: "Georgia, serif",
      padding: "0",
    }}>
      {/* Header */}
      <div style={{
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        padding: "20px 32px",
        display: "flex",
        alignItems: "baseline",
        gap: "16px",
        background: "rgba(255,255,255,0.01)",
      }}>
        <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: "11px", fontWeight: 700, letterSpacing: "0.2em", color: "rgba(255,180,50,0.9)" }}>
          HUF
        </span>
        <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: "11px", color: "rgba(255,255,255,0.3)", letterSpacing: "0.1em" }}>
          COMPLIANCE DIAGNOSTIC v1.0
        </span>
        <span style={{ marginLeft: "auto", fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.2)" }}>
          HIGGINS UNITY FRAMEWORK
        </span>
      </div>

      <div style={{ maxWidth: "820px", margin: "0 auto", padding: "32px 24px" }}>

        {/* Step indicator */}
        <div style={{ display: "flex", gap: "0", marginBottom: "32px" }}>
          {["01 DECLARE SYSTEM", "02 INPUT ELEMENTS", "03 DIAGNOSTIC REPORT"].map((label, i) => (
            <div key={i} style={{
              flex: 1,
              padding: "8px 12px",
              borderBottom: step === i + 1 ? "2px solid rgba(255,180,50,0.9)" : "2px solid rgba(255,255,255,0.08)",
              fontFamily: "'IBM Plex Mono', monospace",
              fontSize: "10px",
              letterSpacing: "0.1em",
              color: step === i + 1 ? "rgba(255,180,50,0.9)" : "rgba(255,255,255,0.3)",
              cursor: step > i + 1 ? "pointer" : "default",
            }} onClick={() => step > i + 1 && setStep(i + 1)}>
              {label}
            </div>
          ))}
        </div>

        {/* STEP 1 */}
        {step === 1 && (
          <div>
            <h2 style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: "14px", letterSpacing: "0.12em", color: "rgba(255,180,50,0.9)", marginBottom: "6px", fontWeight: 600 }}>
              SYSTEM DECLARATION
            </h2>
            <p style={{ color: "rgba(255,255,255,0.45)", fontSize: "13px", lineHeight: 1.7, marginBottom: "28px" }}>
              Declare the system you are submitting for HUF compliance testing. Any finite-budget system qualifies — a governance portfolio, a retrieval pipeline, a civic budget, a conservation program, an acoustic array. If it has a budget ceiling and elements that share it, HUF can read it.
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
              <div>
                <label style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.4)", letterSpacing: "0.1em", display: "block", marginBottom: "6px" }}>
                  SYSTEM NAME
                </label>
                <input value={systemName} onChange={e => setSystemName(e.target.value)} placeholder="e.g. Ramsar Wetland Portfolio" style={{ ...inputStyle, width: "100%" }} />
              </div>
              <div>
                <label style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.4)", letterSpacing: "0.1em", display: "block", marginBottom: "6px" }}>
                  CURRENT CYCLE LABEL
                </label>
                <input value={cycleName} onChange={e => setCycleName(e.target.value)} placeholder="e.g. Q1 2026" style={{ ...inputStyle, width: "100%" }} />
              </div>
            </div>
            <div style={{ marginBottom: "28px" }}>
              <label style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.4)", letterSpacing: "0.1em", display: "block", marginBottom: "6px" }}>
                CYCLES ON RECORD (how many complete observation cycles exist?)
              </label>
              <input type="number" min="1" value={numCycles} onChange={e => setNumCycles(parseInt(e.target.value) || 1)} style={{ ...inputStyle, width: "120px" }} />
              {numCycles === 1 && (
                <span style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(251,191,36,0.7)", marginLeft: "12px" }}>
                  ⚠ Single cycle — cross-cycle test will flag
                </span>
              )}
            </div>
            <button onClick={() => setStep(2)} disabled={!systemName.trim()} style={{ ...btnStyle, opacity: systemName.trim() ? 1 : 0.4 }}>
              DECLARE SYSTEM →
            </button>
          </div>
        )}

        {/* STEP 2 */}
        {step === 2 && (
          <div>
            <h2 style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: "14px", letterSpacing: "0.12em", color: "rgba(255,180,50,0.9)", marginBottom: "6px", fontWeight: 600 }}>
              ELEMENT INPUT — {systemName}
            </h2>
            <p style={{ color: "rgba(255,255,255,0.45)", fontSize: "13px", lineHeight: 1.7, marginBottom: "20px" }}>
              Enter each element of your system. Share and declared weight are expressed as decimals (0.25 = 25%). Mark "TRACED" if any share change from the previous cycle has a recorded decision. Characteristic period is in cycles.
            </p>

            {/* Column headers */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 90px 90px 80px 120px 32px", gap: "6px", marginBottom: "8px" }}>
              {["ELEMENT NAME", "SHARE", "DECL. WEIGHT", "CHAR. PERIOD", "CHANGE TRACED?", ""].map((h, i) => (
                <span key={i} style={{ fontFamily: "monospace", fontSize: "9px", color: "rgba(255,255,255,0.3)", letterSpacing: "0.1em" }}>{h}</span>
              ))}
            </div>

            {elements.map((el, i) => (
              <ElementRow key={i} element={el} onChange={updateElement} onRemove={removeElement} index={i} />
            ))}

            {/* Running totals */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 90px 90px 80px 120px 32px", gap: "6px", margin: "10px 0", padding: "8px 0", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
              <span style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.3)" }}>TOTALS</span>
              <span style={{ fontFamily: "monospace", fontSize: "11px", color: Math.abs(shareTotal - 1) < 0.011 ? "#4ade80" : "#f87171" }}>
                {shareTotal.toFixed(4)}
              </span>
              <span style={{ fontFamily: "monospace", fontSize: "11px", color: Math.abs(weightTotal - 1) < 0.011 ? "#4ade80" : "#f87171" }}>
                {weightTotal.toFixed(4)}
              </span>
            </div>

            <div style={{ display: "flex", gap: "10px", marginTop: "16px" }}>
              <button onClick={addElement} style={{ ...btnStyle, background: "rgba(255,255,255,0.04)", borderColor: "rgba(255,255,255,0.15)", color: "rgba(255,255,255,0.6)" }}>
                + ADD ELEMENT
              </button>
              <button onClick={runTest} style={btnStyle} disabled={elements.filter(e => e.name.trim()).length < 2}>
                RUN DIAGNOSTIC →
              </button>
            </div>
          </div>
        )}

        {/* STEP 3 — REPORT */}
        {step === 3 && report && (
          <div>
            {/* Summary bar */}
            <div style={{
              border: `1px solid ${report.summary.hufCompliant ? "rgba(74,222,128,0.4)" : report.summary.hufCapable ? "rgba(251,191,36,0.4)" : "rgba(248,113,113,0.4)"}`,
              borderRadius: "4px",
              padding: "20px 24px",
              marginBottom: "24px",
              background: report.summary.hufCompliant ? "rgba(74,222,128,0.05)" : report.summary.hufCapable ? "rgba(251,191,36,0.05)" : "rgba(248,113,113,0.05)",
            }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: "16px", marginBottom: "12px" }}>
                <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: "11px", letterSpacing: "0.15em", color: "rgba(255,255,255,0.4)" }}>
                  HUF DIAGNOSTIC — {systemName} — {cycleName || "CYCLE 1"}
                </span>
              </div>
              <div style={{
                fontFamily: "'IBM Plex Mono', monospace",
                fontSize: "22px",
                fontWeight: 700,
                letterSpacing: "0.1em",
                color: report.summary.hufCompliant ? "#4ade80" : report.summary.hufCapable ? "#fbbf24" : "#f87171",
                marginBottom: "10px",
              }}>
                {report.summary.hufCompliant ? "HUF COMPLIANT" : report.summary.hufCapable ? "HUF CAPABLE — REMEDIATION REQUIRED" : "NON-COMPLIANT — RATIO BLINDNESS DETECTED"}
              </div>
              <div style={{ display: "flex", gap: "20px" }}>
                {[
                  { label: "PASS", val: report.summary.passes, color: "#4ade80" },
                  { label: "FAIL", val: report.summary.fails, color: "#f87171" },
                  { label: "FLAG/PARTIAL", val: report.summary.flags, color: "#fbbf24" },
                ].map(s => (
                  <div key={s.label} style={{ display: "flex", gap: "8px", alignItems: "baseline" }}>
                    <span style={{ fontFamily: "monospace", fontSize: "20px", fontWeight: 700, color: s.color }}>{s.val}</span>
                    <span style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.3)", letterSpacing: "0.1em" }}>{s.label}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Tests */}
            <div style={{ marginBottom: "24px" }}>
              <div style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.3)", letterSpacing: "0.1em", marginBottom: "12px" }}>
                CLICK ANY TEST TO EXPAND DIAGNOSTIC DETAIL
              </div>
              {report.results.map((test, i) => (
                <TestCard key={test.id} test={test} index={i} />
              ))}
            </div>

            {/* Ratio state snapshot */}
            {report.driftItems.length > 0 && (
              <div style={{ border: "1px solid rgba(255,255,255,0.08)", borderRadius: "4px", padding: "16px", marginBottom: "20px" }}>
                <div style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.3)", letterSpacing: "0.1em", marginBottom: "12px" }}>
                  RATIO STATE SNAPSHOT
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 80px 80px 80px 80px", gap: "4px" }}>
                  {["ELEMENT", "OBSERVED", "DECLARED", "GAP", "STATUS"].map(h => (
                    <span key={h} style={{ fontFamily: "monospace", fontSize: "9px", color: "rgba(255,255,255,0.25)", letterSpacing: "0.08em" }}>{h}</span>
                  ))}
                  {report.driftItems.map((d, i) => {
                    const status = Math.abs(d.gap) < 0.05 ? "ALIGNED" : d.traced ? "INTENTIONAL" : "SILENT DRIFT";
                    const col = status === "ALIGNED" ? "#4ade80" : status === "INTENTIONAL" ? "#fb923c" : "#f87171";
                    return [
                      <span key={`n${i}`} style={{ fontFamily: "monospace", fontSize: "11px", color: "rgba(255,255,255,0.7)" }}>{d.name}</span>,
                      <span key={`s${i}`} style={{ fontFamily: "monospace", fontSize: "11px", color: "rgba(255,255,255,0.7)" }}>{(d.share * 100).toFixed(1)}%</span>,
                      <span key={`w${i}`} style={{ fontFamily: "monospace", fontSize: "11px", color: "rgba(255,255,255,0.5)" }}>{(d.declared * 100).toFixed(1)}%</span>,
                      <span key={`g${i}`} style={{ fontFamily: "monospace", fontSize: "11px", color: Math.abs(d.gap) < 0.05 ? "rgba(255,255,255,0.4)" : col }}>{d.gap > 0 ? "+" : ""}{(d.gap * 100).toFixed(1)}pp</span>,
                      <span key={`st${i}`} style={{ fontFamily: "monospace", fontSize: "9px", color: col, letterSpacing: "0.05em" }}>{status}</span>,
                    ];
                  })}
                </div>
              </div>
            )}

            <div style={{ display: "flex", gap: "10px" }}>
              <button onClick={() => { setStep(2); setReport(null); }} style={{ ...btnStyle, background: "none", borderColor: "rgba(255,255,255,0.15)", color: "rgba(255,255,255,0.5)" }}>
                ← REVISE INPUT
              </button>
              <button onClick={() => { setStep(1); setSystemName(""); setCycleName(""); setNumCycles(1); setElements([{ name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false }, { name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false }, { name: "", share: "", declaredWeight: "", characteristicPeriod: "", traced: false }]); setReport(null); }} style={{ ...btnStyle }}>
                NEW SYSTEM →
              </button>
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{ marginTop: "48px", paddingTop: "16px", borderTop: "1px solid rgba(255,255,255,0.05)", display: "flex", justifyContent: "space-between" }}>
          <span style={{ fontFamily: "monospace", fontSize: "9px", color: "rgba(255,255,255,0.2)", letterSpacing: "0.1em" }}>
            HIGGINS UNITY FRAMEWORK · HUF v1.1.8 · MIT LICENSE
          </span>
          <span style={{ fontFamily: "monospace", fontSize: "9px", color: "rgba(255,255,255,0.2)", letterSpacing: "0.1em" }}>
            ROGUE WAVE AUDIO · MARKHAM ONTARIO
          </span>
        </div>
      </div>
    </div>
  );
}
