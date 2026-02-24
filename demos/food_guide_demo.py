"""
HUF Real Data Demo -- Canada's Food Guide recipes
https://food-guide.canada.ca/en/recipes/

This script demonstrates the HUF audit posture on real publicly available data.
Nutritional values should be verified at source before use.

Data source: Canada's Food Guide (Government of Canada, open licence)
Companion app: https://github.com/MoSchaub/BackApp

Usage:
    python food_guide_demo.py

Outputs:
    portfolio_share_table.csv       -- macronutrient profile per recipe
    trace_report.csv                -- operator weight declaration log
    portfolio_change_log.csv       -- which recipes shift the balance
    coverage_change_record.csv    -- recipes removed from portfolio

To use your own data: replace RECIPES below with values from
https://food-guide.canada.ca/en/recipes/
Verify numbers at source -- nutrient values are updated periodically.
"""

import pandas as pd
import io
from datetime import datetime
from pathlib import Path


# ── DATA ──────────────────────────────────────────────────────────────────────
# Source: Canada's Food Guide -- https://food-guide.canada.ca/en/recipes/
# Verify these values at source before using in any formal context.
# Values are per serving (protein g, carbs g, fat g).

RECIPES_CSV = """recipe,protein_g,carbs_g,fat_g,source
Chicken and vegetable stir-fry,28,22,8,food-guide.canada.ca/en/recipes/
Red lentil soup,14,38,4,food-guide.canada.ca/en/recipes/
Vegetable omelette,18,6,12,food-guide.canada.ca/en/recipes/
Overnight oats with berries,9,44,7,food-guide.canada.ca/en/recipes/
Salmon with roasted vegetables,32,18,14,food-guide.canada.ca/en/recipes/"""

# ── OPERATOR DECLARATION ──────────────────────────────────────────────────────
# The Operator (you, a dietitian, a household) declares the target balance.
# These are not arbitrary -- they reflect a dietary intention.
# Change these to reflect your own priorities.

OPERATOR_WEIGHTS = {
    'protein': 0.35,
    'carbs':   0.45,
    'fat':     0.20
}

# ── CORE ──────────────────────────────────────────────────────────────────────

OUT_DIR = Path('out/food_guide_demo')


def run_demo(recipes_csv, operator_weights):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(io.StringIO(recipes_csv))

    # Normalize each recipe's macros to sum to 1.0 (unity constraint per recipe)
    macro_cols = ['protein_g', 'carbs_g', 'fat_g']
    df['total_macros'] = df[macro_cols].sum(axis=1)
    df['protein_share'] = df['protein_g'] / df['total_macros']
    df['carbs_share']   = df['carbs_g']   / df['total_macros']
    df['fat_share']     = df['fat_g']     / df['total_macros']

    # Apply operator weights to score each recipe against declared intention
    df['alignment_score'] = (
        (1 - abs(df['protein_share'] - operator_weights['protein'])) * operator_weights['protein'] +
        (1 - abs(df['carbs_share']   - operator_weights['carbs']))   * operator_weights['carbs']   +
        (1 - abs(df['fat_share']     - operator_weights['fat']))     * operator_weights['fat']
    )

    # Portfolio mass fraction (normalized alignment across recipes)
    df['portfolio_mass'] = df['alignment_score'] / df['alignment_score'].sum()
    df['portfolio_share_pct'] = (df['portfolio_mass'] * 100).round(2).astype(str) + '%'

    # Flag recipes that pull strongly away from declared weights
    df['drift_flag'] = df.apply(lambda r:
        'HIGH PROTEIN PULL'  if r['protein_share'] > operator_weights['protein'] + 0.15 else
        'HIGH CARB PULL'     if r['carbs_share']   > operator_weights['carbs']   + 0.15 else
        'HIGH FAT PULL'      if r['fat_share']     > operator_weights['fat']     + 0.10 else
        'Aligned', axis=1)

    # ── ARTIFACT 1: Portfolio Share Table ─────────────────────────────────────
    portfolio = df[[
        'recipe', 'portfolio_share_pct',
        'protein_share', 'carbs_share', 'fat_share', 'drift_flag'
    ]].copy()
    portfolio.columns = [
        'Recipe', 'Portfolio_Share',
        'Protein_Fraction', 'Carbs_Fraction', 'Fat_Fraction', 'Balance_Note'
    ]
    portfolio = portfolio.sort_values('Portfolio_Share', ascending=False)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    portfolio.to_csv(OUT_DIR / 'portfolio_share_table.csv', index=False)

    # ── ARTIFACT 2: Trace Report ───────────────────────────────────────────────
    trace = pd.DataFrame([{
        'Timestamp': timestamp,
        'Action': 'Operator Weight Declaration',
        'Detail': (f"Protein target={operator_weights['protein']}, "
                   f"Carbs target={operator_weights['carbs']}, "
                   f"Fat target={operator_weights['fat']}. "
                   f"Declared before normalization run."),
        'Data_Source': 'food-guide.canada.ca/en/recipes/ -- verify values at source'
    }])
    trace.to_csv(OUT_DIR / 'trace_report.csv', index=False)

    # ── ARTIFACT 3: Allocation Change Log ─────────────────────────────────────
    drifting = df[df['drift_flag'] != 'Aligned'][[
        'recipe', 'drift_flag', 'protein_share', 'carbs_share', 'fat_share'
    ]].copy()
    drifting['Classification'] = '[PORTFOLIO DRIFT -- review against dietary intention]'
    drifting.columns = [
        'Recipe', 'Pull_Direction',
        'Protein_Fraction', 'Carbs_Fraction', 'Fat_Fraction', 'Classification'
    ]
    drifting.to_csv(OUT_DIR / 'portfolio_change_log.csv', index=False)

    # ── ARTIFACT 4: Dropped Attention Record ──────────────────────────────────
    dropped = pd.DataFrame([{
        'Recipe': 'None removed in this run',
        'Reason': 'All five recipes retained. No dietary criteria applied for exclusion.',
        'Note': 'To exclude a recipe, remove it from RECIPES_CSV and record reason here.'
    }])
    dropped.to_csv(OUT_DIR / 'coverage_change_record.csv', index=False)

    # ── CONSOLE OUTPUT ────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("HUF Real Data Demo -- Canada's Food Guide recipes")
    print(f"Data source: food-guide.canada.ca/en/recipes/")
    print(f"Operator weights: Protein={operator_weights['protein']}, "
          f"Carbs={operator_weights['carbs']}, Fat={operator_weights['fat']}")
    print("="*60)

    print("\nARTIFACT 1 -- Portfolio Share Table")
    print(portfolio[['Recipe', 'Portfolio_Share', 'Balance_Note']].to_string(index=False))

    if not drifting.empty:
        print("\nARTIFACT 3 -- Allocation Change Log (recipes pulling away from declared weights)")
        print(drifting[['Recipe', 'Pull_Direction']].to_string(index=False))
    else:
        print("\nARTIFACT 3 -- Allocation Change Log: all recipes aligned with declared weights.")

    print("\n4 CSV artifacts written to:", OUT_DIR)
    print("Verify nutritional values at: food-guide.canada.ca/en/recipes/")
    print("="*60)

    return portfolio



if __name__ == "__main__":
    # Verify operator weights sum to 1.0
    assert abs(sum(OPERATOR_WEIGHTS.values()) - 1.0) < 1e-9, \
        "Operator weights must sum to 1.0"

    run_demo(RECIPES_CSV, OPERATOR_WEIGHTS)

    # ── WEIGHT SHIFT DEMO ─────────────────────────────────────────────────────
    # Uncomment to see how a dietary priority shift changes the portfolio:
    #
    # print("\n--- WEIGHT SHIFT: switching to high-protein intention ---")
    # high_protein = {'protein': 0.50, 'carbs': 0.30, 'fat': 0.20}
    # run_demo(RECIPES_CSV, high_protein)
