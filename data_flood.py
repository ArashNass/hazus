import pandas as pd


def extract_flood(path: str) -> list:
    print(f"  Reading flood: {path}")
    df = pd.read_excel(path, header=2)
    df.columns = [str(c).strip() for c in df.columns]

    depth_cols = [c for c in df.columns if c.lstrip('-').isdigit()]
    depth_m    = [round(int(c) * 0.3048, 2) for c in depth_cols]

    curves = []
    for _, row in df.iterrows():
        fn_id = row.get("FnID", "")
        if str(fn_id).strip() in ("", "nan"):
            continue

        dmg_vals = []
        for c in depth_cols:
            try:    dmg_vals.append(round(float(row[c]), 4))
            except: dmg_vals.append(0.0)

        curves.append({
            "fn_id":       int(fn_id) if str(fn_id).replace('.', '').isdigit() else str(fn_id),
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

    print(f"    Flood: {len(curves)} vulnerability functions loaded")
    return curves
