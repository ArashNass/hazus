"""
data_utility.py
Parses Hazus utility earthquake fragility medians/betas from:
  data_sources/hazus_4.2sp3_section8_utility_fragility.csv
"""
import csv
import os


STATE_ORDER = ["Slight", "Moderate", "Extensive", "Complete"]
STATE_ALIASES = {
    "Slight/Moderate": ("Slight", "Moderate"),
    "Moderate/Extensive": ("Moderate", "Extensive"),
    "Extensive/Complete": ("Extensive", "Complete"),
}


def _clean(value):
    if value is None:
        return ""
    return str(value).strip()


def _state_names(label):
    raw = _clean(label)
    if not raw:
        return ()
    if raw in STATE_ALIASES:
        return STATE_ALIASES[raw]
    return (raw,)


def extract_utility(csv_path):
    print(f"  Reading Hazus utility fragility from: {csv_path}")
    if not os.path.exists(csv_path):
        print(f"  SKIP: utility fragility CSV not found: {csv_path}")
        return []

    grouped = {}
    with open(csv_path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            system = _clean(row.get("system"))
            table = _clean(row.get("table"))
            facility = _clean(row.get("facility_type"))
            code = _clean(row.get("code"))
            size = _clean(row.get("size_category"))
            anchoring = _clean(row.get("anchoring")) or "N/A"
            ds = _clean(row.get("damage_state"))
            try:
                median_g = float(row.get("median_g"))
                beta = float(row.get("beta"))
            except (TypeError, ValueError):
                continue

            key = (system, table, facility, code, size, anchoring)
            if key not in grouped:
                grouped[key] = {}
            for name in _state_names(ds):
                grouped[key][name] = {"median_g": median_g, "beta": beta}

    records = []
    for (system, table, facility, code, size, anchoring), states in grouped.items():
        ordered_states = []
        for name in STATE_ORDER:
            if name in states:
                ordered_states.append(
                    {"name": name, "median_g": states[name]["median_g"], "beta": states[name]["beta"]}
                )
        if not ordered_states:
            continue

        rid = f"{code} [{table}] | {anchoring}"
        records.append({
            "id": rid,
            "label": f"{facility} — {code} — {anchoring}",
            "system": system,
            "table": table,
            "facility": facility,
            "code": code,
            "size": size,
            "anchoring": anchoring,
            "states": ordered_states,
        })

    records.sort(key=lambda r: (r["system"], r["facility"], r["code"], r["anchoring"]))
    print(f"    Utility fragility: {len(records)} grouped curves")
    return records

