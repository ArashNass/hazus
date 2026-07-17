"""
data_wind.py
Reads HAZUS wind vulnerability functions from local Excel file.

File: data_sources/HAZUS_WIND_DAMAGE_REPORT.xlsx
Sheet: 'Wind Damage Functions'
Structure:
  Row 1-2: description text
  Row 3:   headers — SBT Code, SBT Group, Material, Occupancy, Height Class,
                     Description, Damage Type, then wind speeds in m/s
  Row 4:   wind speeds in km/h (row[7:])
  Row 5:   wind speeds in mph  (row[7:])
  Row 6+:  one curve per row

Source: FEMA Hazus 6.1 / OS-Climate physrisk
Licence: Apache 2.0
"""

import os
import openpyxl


def extract_wind(path: str = None) -> list:
    if path is None:
        folder = os.path.dirname(os.path.abspath(__file__))
        path   = os.path.join(folder, 'data_sources', 'HAZUS_WIND_DAMAGE_REPORT.xlsx')

    print(f'  Reading HAZUS wind functions from: {path}')
    if not os.path.exists(path):
        print(f'  ERROR: file not found: {path}')
        return []

    wb   = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws   = wb['Wind Damage Functions']
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    # Row index 2 (0-based) = header row with column names and m/s values
    # Row index 3 = km/h values, row index 4 = mph values
    header   = rows[2]   # SBT Code, ..., 22.4\nm/s, 24.6\nm/s ...
    kmh_row  = rows[3]   # km/h values starting at col 7
    mph_row  = rows[4]   # mph values starting at col 7

    # Extract wind speed arrays from header (strip \n and unit)
    wind_ms  = []
    wind_kmh = []
    wind_mph = []
    for i, h in enumerate(header[7:], 7):
        if h is None:
            break
        try:
            ms = float(str(h).split('\n')[0].replace('m/s','').strip())
            wind_ms.append(round(ms, 1))
            wind_kmh.append(float(kmh_row[i]) if kmh_row[i] else round(ms*3.6, 1))
            wind_mph.append(float(mph_row[i]) if mph_row[i] else round(ms*2.237, 1))
        except (ValueError, TypeError):
            break

    n_speeds = len(wind_ms)

    curves = []
    for row in rows[5:]:
        if not row[0] or not isinstance(row[0], str):
            continue
        sbt  = str(row[0]).strip()
        dmg  = [round(float(v), 4) if v is not None else 0.0
                for v in row[7:7+n_speeds]]
        if len(dmg) < n_speeds:
            dmg += [0.0] * (n_speeds - len(dmg))

        curves.append({
            'sbt':         sbt,
            'sbt_group':   str(row[1]).strip() if row[1] else '',
            'material':    str(row[2]).strip() if row[2] else '',
            'occupancy':   str(row[3]).strip() if row[3] else '',
            'height':      str(row[4]).strip() if row[4] else '',
            'description': str(row[5]).strip() if row[5] else '',
            'damage_type': str(row[6]).strip() if row[6] else '',
            'wind_ms':     wind_ms,
            'wind_kmh':    wind_kmh,
            'wind_mph':    wind_mph,
            'damage':      dmg,
        })

    print(f'    Wind: {len(curves)} vulnerability functions loaded')
    return curves
