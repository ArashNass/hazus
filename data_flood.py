import pandas as pd

from data_validate import validate_damage_curve, log_problems


def extract_flood(path: str) -> list:
    print(f"  Reading flood: {path}")
    df = pd.read_excel(path, header=2)
    df.columns = [str(c).strip() for c in df.columns]

    depth_cols = [c for c in df.columns if c.lstrip('-').isdigit()]
    depth_m    = [round(int(c) * 0.3048, 2) for c in depth_cols]

    curves = []
    excluded = 0
    all_problems = []

    for _, row in df.iterrows():
        fn_id = row.get("FnID", "")
        if str(fn_id).strip() in ("", "nan"):
            continue
        fn_id_out = int(fn_id) if str(fn_id).replace('.', '').isdigit() else str(fn_id)

        # Parse every damage cell as-is; missing/invalid stays None, never 0.0.
        dmg_vals = []
        for c in depth_cols:
            raw = row[c]
            try:
                v = float(raw)
                if v != v:  # NaN check without importing math/numpy here
                    v = None
            except (TypeError, ValueError):
                v = None
            dmg_vals.append(round(v, 4) if v is not None else None)

        problems = validate_damage_curve(depth_m, dmg_vals, fn_id_out, "HAZUS_FLOOD_DAMAGE_REPORT")
        if problems:
            excluded += 1
            all_problems.extend(problems)
            continue

        curves.append({
            "fn_id":       fn_id_out,
            "occupancy":   str(row.get("Occupancy",   "")).strip(),
            "category":    str(row.get("Category",    "")).strip(),
            "description": str(row.get("Description", "")).strip(),
            "source":      str(row.get("Source",      "")).strip(),
            "damage_type": str(row.get("damage_type", "")).strip(),
            "default":     str(row.get("Default",     "")).strip(),
            "flood_types": str(row.get("flood_types", "")).strip(),
            "depth_m":     depth_m,
            "damage":      dmg_vals,
        })

    log_problems(all_problems, "flood vulnerability functions")
    print(f"    Flood: {len(curves)} vulnerability functions loaded"
          + (f", {excluded} excluded (missing/invalid data \u2014 see warnings above)" if excluded else ""))
    return curves
