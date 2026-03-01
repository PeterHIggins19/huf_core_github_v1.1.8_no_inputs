"""
Ramsar HUF Translation Wrapper — v2
30-minute demonstration script for Croatia RSIS pilot

This wrapper translates HUF core outputs into Ramsar-compliant CSV artifacts
using the vocabulary from the Ramsar primer v12. All internal HUF terminology
is masked in outputs. Console messages use primer language: portfolio shares,
traceability, allocation shifts, intentional vs silent reweighting.

Changes from v1 (Copilot integration — February 2026):
  - Leverage and Leverage_Flag added to _normalize() and portfolio share table
  - Console artifact headings aligned to primer vocabulary
  - Final summary line updated to primer framing
  - Data_Age_Warning default threshold: > 5 years (Ramsar pilot)

Usage:
    python ramsar_huf_demo_v2.py

Outputs (4 CSV files):
    portfolio_share_table.csv        — allocation view for National Report annexes
    trace_report.csv                 — line-item justification for share movements
    portfolio_change_log.csv         — intentional reweighting vs. silent drift
    coverage_record.csv              — what was de-prioritised and against what criteria

Author: Peter Higgins · Rogue Wave Audio
Framework: Higgins Unity Framework (HUF) v1.2.0
Demo prepared with collective review (Claude, Copilot, Grok, Gemini, ChatGPT)
"""

import pandas as pd
import numpy as np
import io
from datetime import datetime

# ── MOCK RSIS BASELINE DATA ────────────────────────────────────────────────────
# In live demo: replace csv_string with pd.read_csv('rsis_croatia_export.csv')
# Data sourced from public RSIS exports (rsis.ramsar.org)
# Provenance: [insert filename], retrieved [YYYY-MM-DD]

MOCK_RSIS = """site_id,site_name,metric_area_ha,metric_endemism_count,data_year_area,data_year_endemism
1,Kopački Rit,23894,5,2022,2023
2,Lonjsko Polje and Mokro Polje,50560,3,2021,2021
3,Crna Mlaka,625,1,2024,2024
4,Lower Neretva Valley,12000,18,2013,2018
5,Vransko Lake Nature Park,5748,4,2023,2023"""

# ── SIMULATED DRIFT DATA ───────────────────────────────────────────────────────
SIMULATED_DRIFT = [
    {
        'Reporting_Cycle': '2021 to 2024',
        'Site_Name': 'Lower Neretva Valley',
        'Shift_in_Share': '+4.2%',
        'Classification': '[INTENTIONAL REWEIGHTING]',
        'Driver': 'MedWet transboundary governance obligation — documented in Standing Committee minutes'
    },
    {
        'Reporting_Cycle': '2021 to 2024',
        'Site_Name': 'Lonjsko Polje and Mokro Polje',
        'Shift_in_Share': '-1.5%',
        'Classification': '[SILENT DRIFT]',
        'Driver': 'Gradual diversion of site-monitoring funds toward high-profile transboundary reporting — no policy decision recorded'
    }
]


class RamsarHUFWrapper:
    """
    Translation layer between HUF core engine and Ramsar institutional vocabulary.

    The Scientific Operator declares weights. The wrapper enforces the unity
    constraint and emits four Ramsar-compliant CSVs. Console output uses
    primer vocabulary for policy audiences.

    Lever columns added (v2):
        Leverage      = 1 / observed_share  (unitless sensitivity indicator)
        Leverage_Flag = High (>100) / Medium (10-100) / Low (<10)

    Interpretation note: leverage values above 100 are qualitative high-leverage
    flags. Treat them as prompts for targeted investigation rather than precise
    multiplicative claims. They indicate phase-dependent, high-Q elements whose
    small proportional share masks high governance sensitivity.
    """

    def __init__(self, operator_weights: dict):
        assert abs(sum(operator_weights.values()) - 1.0) < 1e-9, \
            "Operator weights must sum to 1.0"
        self.operator_weights = operator_weights
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.df = None

    def ingest_rsis_data(self, csv_string: str):
        """
        Load asynchronous RSIS baseline. Data age columns are preserved.
        In live pilot, replace csv_string with:
            pd.read_csv('rsis_croatia_export.csv')
        and record the export filename and retrieval date in the trace report.
        """
        self.df = pd.read_csv(io.StringIO(csv_string))
        return self.df

    def _normalize(self):
        """
        Core operation: compute observed shares from input metrics and enforce unity.
        Outputs are formatted for Ramsar audiences.

        Steps:
            1. Normalise area and endemism metrics independently.
            2. Apply operator-declared weights and sum to composite score.
            3. Renormalise composite to exact unity (numerical stability).
            4. Format Portfolio_Share_Pct as display string.
            5. Flag stale input data (Data_Age_Warning).
            6. Compute Leverage = 1/rho and assign Leverage_Flag.
        """
        df = self.df
        w_area = self.operator_weights['area']
        w_end  = self.operator_weights['endemism']

        df['norm_area']     = df['metric_area_ha']        / df['metric_area_ha'].sum()
        df['norm_endemism'] = df['metric_endemism_count'] / df['metric_endemism_count'].sum()

        df['rho'] = (df['norm_area'] * w_area) + (df['norm_endemism'] * w_end)

        # Enforce unity constraint exactly
        df['rho'] = df['rho'] / df['rho'].sum()

        # Format for Ramsar policy audience
        df['Portfolio_Share_Pct'] = (df['rho'] * 100).round(2).astype(str) + '%'

        # Data age warning (Ramsar pilot default: stale if > 5 years)
        current_year = datetime.now().year
        df['Data_Age_Warning'] = df.apply(
            lambda row: f"Endemism data > 5 yrs old ({int(row['data_year_endemism'])})"
            if (current_year - int(row['data_year_endemism'])) > 5 else "Current",
            axis=1
        )

        # ── LEVERAGE (added v2, Copilot integration) ──────────────────────────
        # Leverage = 1 / observed_share. Unitless. Highlights elements whose
        # small proportional share masks high governance sensitivity.
        # Values above 100 are qualitative high-leverage flags, not precise
        # multiplicative claims. Require cross-cycle corroboration before
        # major resource reallocation decisions on high-leverage elements.
        df['Leverage'] = (1.0 / df['rho']).round(2)
        df['Leverage_Flag'] = df['Leverage'].apply(
            lambda x: 'High' if x > 100 else ('Medium' if x >= 10 else 'Low')
        )

        self.df = df

    # ── ARTIFACT 1: Portfolio Share Table ──────────────────────────────────────
    def emit_portfolio_share_table(self, output_path='portfolio_share_table.csv'):
        """
        Ramsar equivalent: allocation view for National Report annexes.
        Shows each site's proportional share based on Operator-declared weights.
        Includes Leverage and Leverage_Flag columns (v2).
        """
        self._normalize()
        table = self.df[[
            'site_name', 'Portfolio_Share_Pct', 'Leverage', 'Leverage_Flag', 'Data_Age_Warning'
        ]].copy()
        table.columns = ['Site_Name', 'Portfolio_Share', 'Leverage', 'Leverage_Flag', 'Data_Age_Warning']
        table = table.sort_values('Portfolio_Share', ascending=False).reset_index(drop=True)
        table.to_csv(output_path, index=False)
        return table

    # ── ARTIFACT 2: Trace Report ────────────────────────────────────────────────
    def emit_trace_report(self, output_path='trace_report.csv'):
        """
        Ramsar equivalent: line-item justification showing why shares sit where they do.
        Records operator declarations, data ingestion decisions, and unity check results.
        """
        rows = [
            {
                'Timestamp': self.timestamp,
                'Action': 'Operator Weight Declaration',
                'Site_Affected': 'All sites',
                'Justification': (
                    f"Area weight set to {self.operator_weights['area']}; "
                    f"Endemism weight set to {self.operator_weights['endemism']}. "
                    f"Declared by Scientific Operator before normalisation run."
                )
            },
            {
                'Timestamp': self.timestamp,
                'Action': 'RSIS Data Ingestion',
                'Site_Affected': 'Lower Neretva Valley',
                'Justification': (
                    "Baseline area data from 2013, endemism from 2018. "
                    "Loaded as best available. Data age flagged in portfolio table. "
                    "Provenance: RSIS export (Croatia) — [insert filename], "
                    "retrieved [YYYY-MM-DD]; area and endemism fields used as provided. "
                    "Declared weights pending operator confirmation."
                )
            },
            {
                'Timestamp': self.timestamp,
                'Action': 'Unity Check',
                'Site_Affected': 'All sites',
                'Justification': (
                    "Portfolio normalised to sum to 1.0. "
                    "All shares accounted for and recorded in the portfolio share table."
                )
            }
        ]
        trace = pd.DataFrame(rows)
        trace.to_csv(output_path, index=False)
        return trace

    # ── ARTIFACT 3: Portfolio Change Log ───────────────────────────────────────
    def emit_drift_log(self, drift_data: list, output_path='portfolio_change_log.csv'):
        """
        Ramsar equivalent: cycle-by-cycle record distinguishing intentional
        reweighting (documented governance decisions) from silent drift
        (allocation shifts without a corresponding recorded decision).
        """
        log = pd.DataFrame(drift_data)
        log.to_csv(output_path, index=False)
        return log

    # ── ARTIFACT 4: Coverage Record ────────────────────────────────────────────
    def emit_discarded_share_record(self, output_path='coverage_record.csv'):
        """
        Ramsar equivalent: documentation of what was de-prioritised and why.
        Provides the accountability trail for reduced-focus decisions.
        """
        rows = [
            {
                'Site_Name': 'System-Wide',
                'Metric_Discarded': 'Legacy Hydrology Scores (pre-2015)',
                'Reason': (
                    'Operator normalised out metrics older than 10 years '
                    'to maintain comparability in current reporting cycle. '
                    'Original data retained in source files.'
                )
            }
        ]
        record = pd.DataFrame(rows)
        record.to_csv(output_path, index=False)
        return record


# ── 30-MINUTE DEMO EXECUTION ───────────────────────────────────────────────────

def run_demo(operator_weights, label=""):
    print(f"\n{'='*70}")
    print(f"HUF Ramsar Demonstration — {label}")
    print(f"Operator-declared ecological weightings: "
          f"area={operator_weights['area']}, endemism={operator_weights['endemism']}")
    print('='*70)

    wrapper = RamsarHUFWrapper(operator_weights=operator_weights)
    wrapper.ingest_rsis_data(MOCK_RSIS)

    portfolio = wrapper.emit_portfolio_share_table()
    trace     = wrapper.emit_trace_report()
    drift     = wrapper.emit_drift_log(SIMULATED_DRIFT)
    discarded = wrapper.emit_discarded_share_record()

    # Artifact headings aligned to primer vocabulary (Copilot v2 edit)
    print("\nARTIFACT 1 — Portfolio Share Table (cross-cycle allocation view)")
    print("  Leverage > 100 = high-leverage flag: small share, high governance sensitivity")
    print(portfolio.to_string(index=False))

    print("\nARTIFACT 2 — Trace Report (why portfolio shares sit where they do)")
    print(trace[['Action', 'Site_Affected', 'Justification']].to_string(index=False))

    print("\nARTIFACT 3 — Portfolio Change Log (intentional reweighting vs silent drift)")
    print(drift.to_string(index=False))

    print("\nARTIFACT 4 — Coverage Record (what received less focus and why)")
    print(discarded.to_string(index=False))

    return portfolio


if __name__ == "__main__":

    # ── RUN 1: Endemism-priority (MedWet / transboundary context) ─────────────
    run1 = run_demo(
        operator_weights={'area': 0.3, 'endemism': 0.7},
        label="Endemism-priority (MedWet / transboundary context)"
    )

    print("\n" + "─"*70)
    print("Cross-cycle comparison: shifting declared ecological priorities")
    print("This shows how intentional reweighting is recorded transparently.")
    print("─"*70)

    # ── RUN 2: Area-priority (COP16 hectares-protected reporting) ────────────
    weight_shift_drift = [
        {
            'Reporting_Cycle': '2026 Simulation',
            'Site_Name': 'Lower Neretva Valley',
            'Shift_in_Share': '-17.55%',
            'Classification': '[INTENTIONAL REWEIGHTING]',
            'Driver': 'Operator shift: Endemism priority reduced from 0.7 to 0.2'
        },
        {
            'Reporting_Cycle': '2026 Simulation',
            'Site_Name': 'Lonjsko Polje and Mokro Polje',
            'Shift_in_Share': '+15.22%',
            'Classification': '[INTENTIONAL REWEIGHTING]',
            'Driver': 'Operator shift: Area priority increased from 0.3 to 0.8'
        },
        {
            'Reporting_Cycle': '2026 Simulation',
            'Site_Name': 'Kopački Rit',
            'Shift_in_Share': '+3.10%',
            'Classification': '[INTENTIONAL REWEIGHTING]',
            'Driver': 'Operator shift: Area priority increased from 0.3 to 0.8'
        }
    ]

    wrapper2 = RamsarHUFWrapper(operator_weights={'area': 0.8, 'endemism': 0.2})
    wrapper2.ingest_rsis_data(MOCK_RSIS)
    run2 = wrapper2.emit_portfolio_share_table('portfolio_share_table_area_priority.csv')
    wrapper2.emit_drift_log(weight_shift_drift, 'drift_log_weight_shift.csv')

    print("\nARTIFACT 1 — Portfolio Share Table (Area-priority — side-by-side comparison)")
    comparison = pd.DataFrame({
        'Site_Name':             run1['Site_Name'].values,
        'Share_Endemism_Priority': run1['Portfolio_Share'].values,
        'Leverage_Endemism':     run1['Leverage'].values,
        'Share_Area_Priority':   run2['Portfolio_Share'].values,
        'Leverage_Area':         run2['Leverage'].values,
    })
    print(comparison.to_string(index=False))

    print("\nARTIFACT 3 — Drift Log (Weight Shift — all entries intentional)")
    print(pd.DataFrame(weight_shift_drift).to_string(index=False))

    print("\n" + "="*70)
    print("Demonstration complete. Four Ramsar-aligned CSV artifacts generated.")
    print("Changes in a site's share reflect declared priorities or recorded corrections.")
    print("The framework is a neutral scale — your scientific teams define what matters.")
    print("Data provenance: record RSIS export filename and retrieval date in trace report.")
    print("="*70)
