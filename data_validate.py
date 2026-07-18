"""
data_validate.py — Shared validation for all HAZUS/CI hazard, damage-ratio,
and fragility data. Nothing in this module ever repairs, interpolates, or
zero-fills bad data: every problem is reported with enough detail to find
the offending cell, and the caller decides to exclude the curve.

Conventions used throughout:
  - A "problem" is a dict: {"reason": str, "curve_id": str, "sheet": str,
    "column": str|int, "detail": str}
  - Every validate_* function returns a list of problems. An empty list
    means the data passed every check.
"""
import math


def _problem(reason, curve_id="", sheet="", column="", detail=""):
    return {"reason": reason, "curve_id": str(curve_id), "sheet": str(sheet),
            "column": str(column), "detail": str(detail)}


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def validate_ratio(value, curve_id, sheet, column, lo=0.0, hi=1.0):
    """A single value that must be a real, finite number in [lo, hi]
    (damage ratio or exceedance probability). Missing (None) and
    non-numeric (e.g. text) values are both reported, never silently
    replaced."""
    problems = []
    if value is None:
        problems.append(_problem("missing_value", curve_id, sheet, column,
                                  "cell is empty"))
    elif not _is_number(value):
        problems.append(_problem("non_numeric_value", curve_id, sheet, column,
                                  f"value {value!r} is not a finite number"))
    elif not (lo - 1e-9 <= value <= hi + 1e-9):
        problems.append(_problem("out_of_range", curve_id, sheet, column,
                                  f"value {value} outside [{lo}, {hi}]"))
    return problems


def validate_ratio_array(values, curve_id, sheet, column_labels=None, lo=0.0, hi=1.0):
    """A full row/column of damage ratios or probabilities."""
    problems = []
    for i, v in enumerate(values):
        col = column_labels[i] if column_labels and i < len(column_labels) else i
        problems.extend(validate_ratio(v, curve_id, sheet, col, lo, hi))
    return problems


def validate_hazard_axis(xs, curve_id, sheet, strict=True):
    """Hazard intensity axis (wind speed, flood depth, PGA, ...) must be
    present and strictly increasing (or non-decreasing if strict=False)."""
    problems = []
    if not xs or len(xs) < 2:
        problems.append(_problem("insufficient_points", curve_id, sheet, "x-axis",
                                  f"only {len(xs) if xs else 0} hazard points"))
        return problems
    for i in range(1, len(xs)):
        if xs[i] is None or xs[i - 1] is None:
            problems.append(_problem("missing_value", curve_id, sheet, f"x[{i}]",
                                      "hazard axis has a missing point"))
            continue
        if strict and xs[i] <= xs[i - 1]:
            problems.append(_problem("non_increasing_hazard_axis", curve_id, sheet, f"x[{i}]",
                                      f"x[{i}]={xs[i]} is not > x[{i-1}]={xs[i-1]}"))
        elif not strict and xs[i] < xs[i - 1]:
            problems.append(_problem("decreasing_hazard_axis", curve_id, sheet, f"x[{i}]",
                                      f"x[{i}]={xs[i]} is less than x[{i-1}]={xs[i-1]}"))
    return problems


def validate_damage_curve(xs, ys, curve_id, sheet, hi=1.0):
    """Generic vulnerability curve (flood/wind): damage ratio against an
    increasing hazard axis. `hi` is configurable because the official
    HAZUS wind damage functions genuinely go slightly above 1.0 (up to
    ~1.1) at extreme wind speeds for some building types \u2014 confirmed
    against the source spreadsheet, not a parsing artifact \u2014 while
    flood functions stay within [0, 1]."""
    problems = []
    problems.extend(validate_hazard_axis(xs, curve_id, sheet))
    problems.extend(validate_ratio_array(ys, curve_id, sheet, column_labels=xs, hi=hi))
    if len(xs) != len(ys):
        problems.append(_problem("length_mismatch", curve_id, sheet, "",
                                  f"{len(xs)} hazard points vs {len(ys)} damage values"))
    return problems


DS_ORDER = ["Slight", "Moderate", "Extensive", "Complete"]


def validate_ci_fragility_curve(curve):
    """Critical-infrastructure fragility curve: one exceedance-probability
    series per damage state (Slight/Moderate/Extensive/Complete), sharing
    one hazard-intensity axis. Requires, at every intensity level:
      - every probability is a finite number in [0, 1]
      - each damage-state series is non-decreasing with hazard intensity
        (exceedance probability cannot fall as the hazard gets worse)
      - Slight >= Moderate >= Extensive >= Complete at every intensity
        (it's easier to exceed a lower damage state than a higher one)
    'Extensive/Complete' is a valid combined label in this dataset and is
    treated as occupying the Extensive slot for the ordering check (there
    is nothing to compare it against past that point)."""
    problems = []
    cid = curve.get("id", "?")
    sheet = curve.get("hazard", "?") + " fragility"
    xs = curve.get("x") or []
    ds = curve.get("ds") or {}

    if not ds:
        problems.append(_problem("missing_damage_states", cid, sheet, "",
                                  "no damage-state columns found"))
        return problems

    problems.extend(validate_hazard_axis(xs, cid, sheet))

    series = {}
    for label, ys in ds.items():
        if ys is None:
            problems.append(_problem("missing_damage_state_series", cid, sheet, label,
                                      "damage state column has no data"))
            continue
        if len(ys) != len(xs):
            problems.append(_problem("length_mismatch", cid, sheet, label,
                                      f"{len(ys)} y-values vs {len(xs)} hazard points"))
            continue
        problems.extend(validate_ratio_array(ys, cid, sheet, column_labels=xs))
        problems.extend(
            _problem("non_monotonic_probability", cid, sheet, f"{label}[{i}]",
                      f"P({label}) drops from {ys[i-1]} to {ys[i]} as hazard increases")
            for i in range(1, len(ys))
            if _is_number(ys[i]) and _is_number(ys[i - 1]) and ys[i] < ys[i - 1] - 1e-9
        )
        series[label] = ys

    # Ordering across damage states at every shared intensity level.
    ordered_labels = [l for l in DS_ORDER if l in series]
    # Fold a combined "Extensive/Complete" label into the ordering check too.
    if "Extensive/Complete" in series and "Extensive" not in series and "Complete" not in series:
        ordered_labels = [l for l in ["Slight", "Moderate"] if l in series] + ["Extensive/Complete"]

    n = len(xs)
    for i in range(n):
        for a, b in zip(ordered_labels, ordered_labels[1:]):
            ya = series[a][i] if i < len(series[a]) else None
            yb = series[b][i] if i < len(series[b]) else None
            if _is_number(ya) and _is_number(yb) and ya < yb - 1e-9:
                problems.append(_problem(
                    "damage_state_ordering_violation", cid, sheet, f"x[{i}]={xs[i]}",
                    f"P({a})={ya} < P({b})={yb} \u2014 expected {a} >= {b} at every intensity"))

    return problems


def validate_eq_median_row(code, row):
    """Static HAZUS-MH fragility table (data_earthquake.py): for each
    design level (H/M/L/P), the four median PGA values (Slight, Moderate,
    Extensive, Complete) must all be positive and strictly increasing.
    A design level of None means 'combination does not exist in Hazus'
    and is skipped, not an error."""
    problems = []
    for level in ("H", "M", "L", "P"):
        vals = row.get(level)
        if vals is None:
            continue
        if not isinstance(vals, (list, tuple)) or len(vals) != 4:
            problems.append(_problem("malformed_median_row", code, "data_earthquake.py", level,
                                      f"expected 4 values [Slight,Moderate,Extensive,Complete], got {vals!r}"))
            continue
        for label, v in zip(DS_ORDER, vals):
            if not _is_number(v) or v <= 0:
                problems.append(_problem("non_positive_median", code, "data_earthquake.py",
                                          f"{level}.{label}", f"median PGA {v!r} must be > 0"))
        for i in range(1, 4):
            a, b = vals[i - 1], vals[i]
            if _is_number(a) and _is_number(b) and not (a < b):
                problems.append(_problem(
                    "median_ordering_violation", code, "data_earthquake.py",
                    f"{level}.{DS_ORDER[i-1]}->{DS_ORDER[i]}",
                    f"{DS_ORDER[i-1]}={a} must be < {DS_ORDER[i]}={b}"))
    return problems


def log_problems(problems, label, limit=20):
    """Print a concise, actionable report of validation problems."""
    if not problems:
        return
    print(f"    WARNING: {len(problems)} validation problem(s) in {label}:")
    for p in problems[:limit]:
        loc = f"{p['sheet']} / {p['curve_id']} / {p['column']}".strip(" /")
        print(f"      [{p['reason']}] {loc}: {p['detail']}")
    if len(problems) > limit:
        print(f"      ... and {len(problems) - limit} more")
