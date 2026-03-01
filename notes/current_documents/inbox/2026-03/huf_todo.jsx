import { useState, useEffect } from "react";

const INITIAL_ITEMS = [
  {
    id: "handbook",
    category: "PUBLICATIONS",
    title: "HUF Handbook v1.2.0",
    detail: "Comprehensive handbook — six parts, twelve chapters, three appendices. Root planted. Vocabulary defined. Failure mode taxonomy complete. Protocol established.",
    done: true,
    locked: true,
    date: "February 2026",
  },
  {
    id: "math-book",
    category: "PUBLICATIONS",
    title: "Mathematics of HUF",
    detail: "New book. Basic starting mathematics for the average reader. Build from fractions → ratios → unity constraint → formal notation. Data and directions incoming.",
    done: false,
    locked: false,
    date: null,
  },
  {
    id: "propositions",
    category: "FORMALIZATION",
    title: "Formalize the Four Propositions",
    detail: "Proposition 7.1 (Domain Invariance), 7.2 (Non-Invasive Sufficiency), 7.3 (Q-Sensitive Cross-Cycle Observation), 7.4 (Convergence Under Closed Feedback). Formal proofs required.",
    done: false,
    locked: false,
    date: null,
  },
  {
    id: "declaration-comparison",
    category: "DEMONSTRATION",
    title: "First Live Cross-Domain Declaration Comparison",
    detail: "Build first live comparison using the HUF Declaration Format. Two systems, different domains, same vocabulary. Proof of domain invariance in practice.",
    done: false,
    locked: false,
    date: null,
  },
  {
    id: "ramsar-diagnostic",
    category: "DEMONSTRATION",
    title: "Ramsar Pilot — Compliance Diagnostic",
    detail: "Run the Ramsar wetland portfolio through the eight-test compliance diagnostic. First real-world HUF compliance report. Cross-cycle data required.",
    done: false,
    locked: false,
    date: null,
  },
  {
    id: "vocabulary-standard",
    category: "PROTOCOL",
    title: "HUF Vocabulary — Publish as Standalone Standard",
    detail: "The 14-term vocabulary as a standalone published document. The protocol lives or dies by vocabulary adoption. Needs its own citable artifact.",
    done: false,
    locked: false,
    date: null,
  },
  {
    id: "diagnostic-tool",
    category: "TOOLS",
    title: "HUF Compliance Diagnostic Tool v1.0",
    detail: "Eight-test interactive diagnostic. React component built. Needs integration into canonical docs site and first real system run.",
    done: false,
    locked: false,
    date: null,
  },
];

const CATEGORY_COLORS = {
  PUBLICATIONS:  { bg: "rgba(184,134,11,0.12)",  border: "rgba(184,134,11,0.5)",  text: "#B8860B" },
  FORMALIZATION: { bg: "rgba(46,64,128,0.12)",   border: "rgba(46,64,128,0.5)",   text: "#4A6FBF" },
  DEMONSTRATION: { bg: "rgba(30,107,58,0.12)",   border: "rgba(30,107,58,0.5)",   text: "#1E6B3A" },
  PROTOCOL:      { bg: "rgba(100,60,140,0.12)",  border: "rgba(100,60,140,0.5)",  text: "#7B4FA6" },
  TOOLS:         { bg: "rgba(60,100,140,0.12)",  border: "rgba(60,100,140,0.5)",  text: "#3A6E9E" },
};

export default function HUFTodo() {
  const [items, setItems] = useState(INITIAL_ITEMS);
  const [loaded, setLoaded] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDetail, setNewDetail] = useState("");
  const [newCategory, setNewCategory] = useState("PUBLICATIONS");
  const [adding, setAdding] = useState(false);

  // Load from storage
  useEffect(() => {
    (async () => {
      try {
        const result = await window.storage.get("huf-todo-items");
        if (result?.value) {
          setItems(JSON.parse(result.value));
        }
      } catch (_) {}
      setLoaded(true);
    })();
  }, []);

  // Save to storage whenever items change
  useEffect(() => {
    if (!loaded) return;
    window.storage.set("huf-todo-items", JSON.stringify(items)).catch(() => {});
  }, [items, loaded]);

  const toggle = (id) => {
    setItems(prev => prev.map(item =>
      item.id === id && !item.locked
        ? { ...item, done: !item.done, date: !item.done ? new Date().toLocaleDateString("en-CA", { month: "long", year: "numeric" }) : null }
        : item
    ));
  };

  const addItem = () => {
    if (!newTitle.trim()) return;
    const newItem = {
      id: `custom-${Date.now()}`,
      category: newCategory,
      title: newTitle.trim(),
      detail: newDetail.trim() || "No detail provided.",
      done: false,
      locked: false,
      date: null,
    };
    setItems(prev => [...prev, newItem]);
    setNewTitle("");
    setNewDetail("");
    setAdding(false);
  };

  const doneCount = items.filter(i => i.done).length;
  const totalCount = items.length;
  const progress = Math.round((doneCount / totalCount) * 100);

  const categories = [...new Set(items.map(i => i.category))];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0c0c14",
      color: "rgba(255,255,255,0.85)",
      fontFamily: "Georgia, serif",
      padding: "0",
    }}>
      {/* Header */}
      <div style={{
        borderBottom: "1px solid rgba(255,255,255,0.07)",
        padding: "20px 32px",
        background: "rgba(255,255,255,0.01)",
      }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: "16px", marginBottom: "4px" }}>
          <span style={{ fontFamily: "monospace", fontSize: "11px", fontWeight: 700, letterSpacing: "0.2em", color: "rgba(184,134,11,0.9)" }}>HUF</span>
          <span style={{ fontFamily: "monospace", fontSize: "11px", color: "rgba(255,255,255,0.35)", letterSpacing: "0.1em" }}>PROJECT TRACE</span>
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: "24px" }}>
          <span style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.25)" }}>
            HIGGINS UNITY FRAMEWORK · MARKHAM ONTARIO
          </span>
          <span style={{ marginLeft: "auto", fontFamily: "monospace", fontSize: "11px", color: "rgba(255,255,255,0.4)" }}>
            {doneCount}/{totalCount} COMPLETE · {progress}%
          </span>
        </div>
        {/* Progress bar */}
        <div style={{ marginTop: "12px", height: "3px", background: "rgba(255,255,255,0.07)", borderRadius: "2px" }}>
          <div style={{
            height: "100%",
            width: `${progress}%`,
            background: "linear-gradient(90deg, rgba(184,134,11,0.8), rgba(184,134,11,0.4))",
            borderRadius: "2px",
            transition: "width 0.5s ease",
          }} />
        </div>
      </div>

      <div style={{ maxWidth: "800px", margin: "0 auto", padding: "28px 24px" }}>

        {/* Items by category */}
        {categories.map(cat => {
          const catItems = items.filter(i => i.category === cat);
          const col = CATEGORY_COLORS[cat] || CATEGORY_COLORS.TOOLS;
          return (
            <div key={cat} style={{ marginBottom: "28px" }}>
              <div style={{
                fontFamily: "monospace",
                fontSize: "10px",
                letterSpacing: "0.15em",
                color: col.text,
                marginBottom: "10px",
                display: "flex",
                alignItems: "center",
                gap: "10px",
              }}>
                <span>{cat}</span>
                <span style={{ height: "1px", flex: 1, background: col.border, opacity: 0.3 }} />
                <span style={{ color: "rgba(255,255,255,0.25)" }}>
                  {catItems.filter(i => i.done).length}/{catItems.length}
                </span>
              </div>

              {catItems.map(item => (
                <div
                  key={item.id}
                  onClick={() => !item.locked && toggle(item.id)}
                  style={{
                    border: item.done
                      ? `1px solid ${col.border}`
                      : "1px solid rgba(255,255,255,0.08)",
                    borderLeft: `3px solid ${item.done ? col.text : "rgba(255,255,255,0.15)"}`,
                    borderRadius: "4px",
                    padding: "14px 16px",
                    marginBottom: "8px",
                    background: item.done ? col.bg : "rgba(255,255,255,0.02)",
                    cursor: item.locked ? "default" : "pointer",
                    transition: "all 0.2s",
                    opacity: item.done && !item.locked ? 0.85 : 1,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "flex-start", gap: "12px" }}>
                    {/* Checkbox */}
                    <div style={{
                      width: "18px",
                      height: "18px",
                      borderRadius: "3px",
                      border: item.done ? `2px solid ${col.text}` : "2px solid rgba(255,255,255,0.2)",
                      background: item.done ? col.bg : "transparent",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                      marginTop: "2px",
                    }}>
                      {item.done && (
                        <span style={{ color: col.text, fontSize: "12px", fontWeight: 700 }}>✓</span>
                      )}
                    </div>

                    <div style={{ flex: 1 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
                        <span style={{
                          fontFamily: "monospace",
                          fontSize: "13px",
                          fontWeight: 700,
                          letterSpacing: "0.04em",
                          color: item.done ? col.text : "rgba(255,255,255,0.85)",
                          textDecoration: item.done && !item.locked ? "none" : "none",
                        }}>
                          {item.title}
                        </span>
                        {item.locked && (
                          <span style={{
                            fontFamily: "monospace",
                            fontSize: "9px",
                            letterSpacing: "0.1em",
                            padding: "2px 6px",
                            border: `1px solid ${col.border}`,
                            borderRadius: "2px",
                            color: col.text,
                            background: col.bg,
                          }}>LOCKED</span>
                        )}
                        {item.date && (
                          <span style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(255,255,255,0.3)", marginLeft: "auto" }}>
                            {item.date}
                          </span>
                        )}
                      </div>
                      <p style={{
                        fontFamily: "Georgia, serif",
                        fontSize: "12px",
                        color: "rgba(255,255,255,0.45)",
                        lineHeight: 1.6,
                        margin: 0,
                      }}>
                        {item.detail}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          );
        })}

        {/* Add new item */}
        {!adding ? (
          <button onClick={() => setAdding(true)} style={{
            background: "none",
            border: "1px dashed rgba(255,255,255,0.15)",
            color: "rgba(255,255,255,0.35)",
            fontFamily: "monospace",
            fontSize: "11px",
            letterSpacing: "0.1em",
            padding: "10px 20px",
            borderRadius: "4px",
            cursor: "pointer",
            width: "100%",
          }}>
            + ADD ITEM TO TRACE
          </button>
        ) : (
          <div style={{
            border: "1px solid rgba(184,134,11,0.3)",
            borderRadius: "4px",
            padding: "16px",
            background: "rgba(184,134,11,0.05)",
          }}>
            <div style={{ fontFamily: "monospace", fontSize: "10px", color: "rgba(184,134,11,0.8)", letterSpacing: "0.1em", marginBottom: "12px" }}>
              NEW TRACE ITEM
            </div>
            <input
              placeholder="Title"
              value={newTitle}
              onChange={e => setNewTitle(e.target.value)}
              style={{ width: "100%", boxSizing: "border-box", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "3px", padding: "8px 10px", color: "rgba(255,255,255,0.85)", fontFamily: "monospace", fontSize: "12px", marginBottom: "8px", outline: "none" }}
            />
            <textarea
              placeholder="Detail (optional)"
              value={newDetail}
              onChange={e => setNewDetail(e.target.value)}
              rows={2}
              style={{ width: "100%", boxSizing: "border-box", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "3px", padding: "8px 10px", color: "rgba(255,255,255,0.85)", fontFamily: "Georgia, serif", fontSize: "12px", marginBottom: "8px", outline: "none", resize: "vertical" }}
            />
            <select
              value={newCategory}
              onChange={e => setNewCategory(e.target.value)}
              style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "3px", padding: "7px 10px", color: "rgba(255,255,255,0.7)", fontFamily: "monospace", fontSize: "11px", marginBottom: "12px", outline: "none" }}
            >
              {Object.keys(CATEGORY_COLORS).map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <div style={{ display: "flex", gap: "8px" }}>
              <button onClick={addItem} style={{ background: "rgba(184,134,11,0.15)", border: "1px solid rgba(184,134,11,0.4)", color: "rgba(184,134,11,0.9)", fontFamily: "monospace", fontSize: "11px", letterSpacing: "0.08em", padding: "8px 16px", borderRadius: "3px", cursor: "pointer" }}>
                ADD
              </button>
              <button onClick={() => setAdding(false)} style={{ background: "none", border: "1px solid rgba(255,255,255,0.1)", color: "rgba(255,255,255,0.4)", fontFamily: "monospace", fontSize: "11px", padding: "8px 16px", borderRadius: "3px", cursor: "pointer" }}>
                CANCEL
              </button>
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{ marginTop: "40px", paddingTop: "16px", borderTop: "1px solid rgba(255,255,255,0.05)", display: "flex", justifyContent: "space-between" }}>
          <span style={{ fontFamily: "monospace", fontSize: "9px", color: "rgba(255,255,255,0.2)", letterSpacing: "0.1em" }}>
            HIGGINS UNITY FRAMEWORK · MIT LICENSE
          </span>
          <span style={{ fontFamily: "monospace", fontSize: "9px", color: "rgba(255,255,255,0.2)", letterSpacing: "0.1em" }}>
            ROGUE WAVE AUDIO · MARKHAM ONTARIO
          </span>
        </div>
      </div>
    </div>
  );
}
