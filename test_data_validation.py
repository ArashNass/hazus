"""
test_data_validation.py — Plain-assertion tests for data_validate.py and its
integration into the flood/wind/CI/earthquake loaders. No pytest dependency;
run directly with:  python3 test_data_validation.py

Deliberately exercises: missing values, non-numeric (text) values,
out-of-range values, and non-monotonic sequences, for every hazard type
mentioned in the review (flood, wind, CI fragility, static EQ medians).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_validate import (
    validate_ratio, validate_ratio_array, validate_hazard_axis,
    validate_damage_curve, validate_ci_fragility_curve, validate_eq_median_row,
)

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


# ── 1. Single-value ratio/probability checks ──────────────────────────────
print("\n1. validate_ratio — missing / text / out-of-range")
check("valid value 0.5 passes", validate_ratio(0.5, "c1", "s1", "col1") == [])
check("None (missing cell) is reported", validate_ratio(None, "c1", "s1", "col1")[0]["reason"] == "missing_value")
check("text value is reported, not silently coerced", validate_ratio("N/A", "c1", "s1", "col1")[0]["reason"] == "non_numeric_value")
check("negative value is out_of_range", validate_ratio(-0.1, "c1", "s1", "col1")[0]["reason"] == "out_of_range")
check("value > 1 is out_of_range (default bounds)", validate_ratio(1.5, "c1", "s1", "col1")[0]["reason"] == "out_of_range")
check("value > 1 passes with a wider hi bound", validate_ratio(1.5, "c1", "s1", "col1", hi=2.0) == [])
check("problem carries curve_id/sheet/column for exact location", (
    lambda p: p["curve_id"] == "c1" and p["sheet"] == "s1" and p["column"] == "col1"
)(validate_ratio(None, "c1", "s1", "col1")[0]))


# ── 2. Hazard axis (must be strictly increasing) ───────────────────────────
print("\n2. validate_hazard_axis — non-monotonic hazard intensity")
check("strictly increasing axis passes", validate_hazard_axis([0, 1, 2, 3], "c1", "s1") == [])
check("flat/repeated axis value is reported", any(
    p["reason"] == "non_increasing_hazard_axis" for p in validate_hazard_axis([0, 1, 1, 3], "c1", "s1")))
check("decreasing axis value is reported", any(
    p["reason"] == "non_increasing_hazard_axis" for p in validate_hazard_axis([0, 2, 1, 3], "c1", "s1")))
check("too few points is reported", validate_hazard_axis([1], "c1", "s1")[0]["reason"] == "insufficient_points")


# ── 3. Flood/wind-style damage curve (the actual bug that was fixed) ──────
print("\n3. validate_damage_curve — flood/wind vulnerability curves")
check("clean curve passes", validate_damage_curve([0, 1, 2], [0.0, 0.3, 0.6], "c1", "s1") == [])
check("missing cell mid-curve is reported (not silently zeroed)", any(
    p["reason"] == "missing_value" for p in validate_damage_curve([0, 1, 2], [0.0, None, 0.6], "c1", "s1")))
check("text cell mid-curve is reported (not silently zeroed)", any(
    p["reason"] == "non_numeric_value" for p in validate_damage_curve([0, 1, 2], [0.0, "bad", 0.6], "c1", "s1")))
check("damage ratio > 1 is reported at the default (flood/ratio) ceiling", any(
    p["reason"] == "out_of_range" for p in validate_damage_curve([0, 1, 2], [0.0, 0.3, 1.4], "c1", "s1")))
check("damage ratio > 1 is NOT reported when hi is widened (wind downtime case)", not any(
    p["reason"] == "out_of_range" for p in validate_damage_curve([0, 1, 2], [0.0, 0.3, 1.4], "c1", "s1", hi=50.0)))
check("mismatched-length arrays are reported", any(
    p["reason"] == "length_mismatch" for p in validate_damage_curve([0, 1, 2], [0.0, 0.3], "c1", "s1")))


# ── 4. CI fragility curves: probabilities, monotonicity, DS ordering ──────
print("\n4. validate_ci_fragility_curve — CI exceedance-probability curves")
good = {
    "id": "T1", "hazard": "Earthquake",
    "x": [0.1, 0.2, 0.3, 0.4],
    "ds": {
        "Slight":    [0.10, 0.40, 0.70, 0.90],
        "Moderate":  [0.05, 0.30, 0.60, 0.85],
        "Extensive": [0.00, 0.10, 0.40, 0.70],
        "Complete":  [0.00, 0.05, 0.20, 0.50],
    },
}
check("well-formed fragility curve passes", validate_ci_fragility_curve(good) == [])

bad_range = {**good, "ds": {**good["ds"], "Slight": [0.10, 0.40, 0.70, 1.20]}}
check("probability > 1 is reported", any(
    p["reason"] == "out_of_range" for p in validate_ci_fragility_curve(bad_range)))

bad_text = {**good, "ds": {**good["ds"], "Slight": [0.10, "oops", 0.70, 0.90]}}
check("text value in a DS column is reported", any(
    p["reason"] == "non_numeric_value" for p in validate_ci_fragility_curve(bad_text)))

bad_missing = {**good, "ds": {**good["ds"], "Complete": [0.0, None, 0.2, 0.5]}}
check("missing value in a DS column is reported", any(
    p["reason"] == "missing_value" for p in validate_ci_fragility_curve(bad_missing)))

bad_mono = {**good, "ds": {**good["ds"], "Moderate": [0.05, 0.30, 0.20, 0.85]}}  # drops then rises
check("probability dropping as hazard increases is reported", any(
    p["reason"] == "non_monotonic_probability" for p in validate_ci_fragility_curve(bad_mono)))

bad_order = {**good, "ds": {**good["ds"], "Moderate": [0.50, 0.50, 0.60, 0.85]}}  # Moderate > Slight at x[0]
check("Slight < Moderate ordering violation is reported", any(
    p["reason"] == "damage_state_ordering_violation" for p in validate_ci_fragility_curve(bad_order)))

no_ds = {"id": "T2", "hazard": "Earthquake", "x": [0.1, 0.2], "ds": {}}
check("curve with no damage-state data is reported", any(
    p["reason"] == "missing_damage_states" for p in validate_ci_fragility_curve(no_ds)))


# ── 5. Static EQ median-PGA table (data_earthquake.py) ─────────────────────
print("\n5. validate_eq_median_row — static HAZUS-MH median PGA table")
good_row = {"H": [26, 55, 128, 201], "M": [24, 43, 91, 134], "L": None, "P": None}
check("well-formed row passes", validate_eq_median_row("W1", good_row) == [])

neg_row = {"H": [26, -5, 128, 201]}
check("negative median is reported", any(
    p["reason"] == "non_positive_median" for p in validate_eq_median_row("BAD", neg_row)))

zero_row = {"H": [0, 55, 128, 201]}
check("zero median is reported (must be strictly positive)", any(
    p["reason"] == "non_positive_median" for p in validate_eq_median_row("BAD", zero_row)))

unordered_row = {"H": [26, 55, 40, 201]}  # Extensive < Moderate
check("Slight<Moderate<Extensive<Complete violation is reported", any(
    p["reason"] == "median_ordering_violation" for p in validate_eq_median_row("BAD", unordered_row)))

equal_row = {"H": [26, 55, 55, 201]}  # not strictly increasing
check("equal adjacent medians (not strictly increasing) is reported", any(
    p["reason"] == "median_ordering_violation" for p in validate_eq_median_row("BAD", equal_row)))

malformed_row = {"H": [26, 55, 128]}  # only 3 values
check("wrong-length median array is reported", any(
    p["reason"] == "malformed_median_row" for p in validate_eq_median_row("BAD", malformed_row)))

none_row = {"H": None, "M": None, "L": None, "P": None}
check("all-None row (combination doesn't exist) is not an error", validate_eq_median_row("N/A", none_row) == [])


# ── 6. Integration: loaders never inject a value where the spreadsheet
#      genuinely had none, and real EQ_DB / real spreadsheets are clean ──
print("\n6. Integration checks against real data (where available)")
try:
    from data_earthquake import EQ_DB
    problems = []
    for code, row in EQ_DB.items():
        problems.extend(validate_eq_median_row(code, row))
    check("real EQ_DB table has zero validation problems", problems == [], f"{len(problems)} problems: {problems[:3]}")
except Exception as e:
    check("real EQ_DB table has zero validation problems", False, f"could not load: {e}")

import os
flood_path = Path(__file__).resolve().parent / "data_sources" / "HAZUS_FLOOD_DAMAGE_REPORT.xlsx"
wind_path  = Path(__file__).resolve().parent / "data_sources" / "HAZUS_WIND_DAMAGE_REPORT.xlsx"

if flood_path.exists():
    from data_flood import extract_flood
    curves = extract_flood(str(flood_path))
    all_vals = [v for c in curves for v in c["damage"]]
    check("no loaded flood curve contains a None damage value", all(v is not None for v in all_vals))
    check("no loaded flood curve contains a damage value outside [0,1]",
          all(0.0 <= v <= 1.0 + 1e-9 for v in all_vals))
else:
    print("  SKIP  flood integration check (data_sources/HAZUS_FLOOD_DAMAGE_REPORT.xlsx not present)")

if wind_path.exists():
    from data_wind import extract_wind
    curves = extract_wind(str(wind_path))
    all_vals = [v for c in curves for v in c["damage"]]
    check("no loaded wind curve contains a None damage value", all(v is not None for v in all_vals))
    check("no loaded wind curve contains a negative damage value", all(v >= -1e-9 for v in all_vals))
else:
    print("  SKIP  wind integration check (data_sources/HAZUS_WIND_DAMAGE_REPORT.xlsx not present)")


print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
