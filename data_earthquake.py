# Hazus-MH fragility parameters
# Median PGA (%g) per damage state: [Slight, Moderate, Extensive, Complete]
# Source: Hazus-MH Technical Manual Table 5.16a-d / USGS ShakeCast
# Beta = 0.64 for all building types (Hazus default)
# None = combination does not exist in Hazus

EQ_DB = {
    "W1":   {"name": "Wood Light Frame",                 "material": "Wood",         "height": "Low-Rise",  "H": [26,55,128,201], "M": [24,43,91,134],  "L": [20,34,61,95],   "P": [18,29,51,77]},
    "W2":   {"name": "Wood Commercial/Industrial",       "material": "Wood",         "height": "All",       "H": [26,56,115,208], "M": [20,35,64,113],  "L": [14,23,48,75],   "P": [12,19,37,60]},
    "S1L":  {"name": "Steel Moment Frame",               "material": "Steel",        "height": "Low-Rise",  "H": [19,31,64,149],  "M": [15,22,42,80],   "L": [12,17,30,48],   "P": [9,13,22,38]},
    "S1M":  {"name": "Steel Moment Frame",               "material": "Steel",        "height": "Mid-Rise",  "H": [14,26,62,143],  "M": [13,21,44,82],   "L": [12,18,29,49],   "P": [9,14,23,39]},
    "S1H":  {"name": "Steel Moment Frame",               "material": "Steel",        "height": "High-Rise", "H": [10,21,52,131],  "M": [10,18,39,78],   "L": [10,15,28,48],   "P": [8,12,22,38]},
    "S2L":  {"name": "Steel Braced Frame",               "material": "Steel",        "height": "Low-Rise",  "H": [24,41,76,146],  "M": [20,26,46,84],   "L": [13,17,30,50],   "P": [11,14,23,39]},
    "S2M":  {"name": "Steel Braced Frame",               "material": "Steel",        "height": "Mid-Rise",  "H": [14,27,73,162],  "M": [14,22,53,97],   "L": [12,18,35,58],   "P": [10,14,28,47]},
    "S2H":  {"name": "Steel Braced Frame",               "material": "Steel",        "height": "High-Rise", "H": [11,22,65,160],  "M": [11,19,49,102],  "L": [11,17,36,63],   "P": [9,13,29,50]},
    "S3":   {"name": "Steel Light Frame",                "material": "Steel",        "height": "All",       "H": [15,26,54,100],  "M": [13,19,33,60],   "L": [10,13,20,38],   "P": [8,10,16,30]},
    "S4L":  {"name": "Steel Frame + Concrete Walls",     "material": "Steel",        "height": "Low-Rise",  "H": [24,39,71,133],  "M": [19,26,41,78],   "L": [13,16,26,46],   "P": [10,13,20,36]},
    "S4M":  {"name": "Steel Frame + Concrete Walls",     "material": "Steel",        "height": "Mid-Rise",  "H": [16,28,73,156],  "M": [14,22,51,92],   "L": [12,17,31,54],   "P": [9,13,25,43]},
    "S4H":  {"name": "Steel Frame + Concrete Walls",     "material": "Steel",        "height": "High-Rise", "H": [13,25,69,163],  "M": [12,21,51,97],   "L": [12,17,33,59],   "P": [9,14,27,47]},
    "S5L":  {"name": "Steel + URM Infill",               "material": "Steel",        "height": "Low-Rise",  "H": None, "M": None, "L": [13,17,28,45],   "P": [11,14,22,37]},
    "S5M":  {"name": "Steel + URM Infill",               "material": "Steel",        "height": "Mid-Rise",  "H": None, "M": None, "L": [11,18,34,53],   "P": [9,14,28,43]},
    "S5H":  {"name": "Steel + URM Infill",               "material": "Steel",        "height": "High-Rise", "H": None, "M": None, "L": [10,18,35,58],   "P": [8,14,29,46]},
    "C1L":  {"name": "Concrete Moment Frame",            "material": "Concrete",     "height": "Low-Rise",  "H": [21,35,70,137],  "M": [16,23,41,77],   "L": [12,15,27,45],   "P": [10,12,21,36]},
    "C1M":  {"name": "Concrete Moment Frame",            "material": "Concrete",     "height": "Mid-Rise",  "H": [15,27,73,161],  "M": [13,21,49,89],   "L": [12,17,32,54],   "P": [9,13,26,43]},
    "C1H":  {"name": "Concrete Moment Frame",            "material": "Concrete",     "height": "High-Rise", "H": [11,22,62,135],  "M": [11,18,41,74],   "L": [10,15,27,44],   "P": [8,12,21,35]},
    "C2L":  {"name": "Concrete Shear Walls",             "material": "Concrete",     "height": "Low-Rise",  "H": [24,45,90,155],  "M": [18,30,49,87],   "L": [14,19,30,52],   "P": [11,15,24,42]},
    "C2M":  {"name": "Concrete Shear Walls",             "material": "Concrete",     "height": "Mid-Rise",  "H": [17,36,87,195],  "M": [15,26,55,102],  "L": [12,19,38,63],   "P": [10,15,30,50]},
    "C2H":  {"name": "Concrete Shear Walls",             "material": "Concrete",     "height": "High-Rise", "H": [12,29,82,187],  "M": [12,23,57,107],  "L": [11,19,38,65],   "P": [9,15,31,52]},
    "C3L":  {"name": "Concrete + URM Infill",            "material": "Concrete",     "height": "Low-Rise",  "H": None, "M": None, "L": [12,17,26,44],   "P": [10,14,21,35]},
    "C3M":  {"name": "Concrete + URM Infill",            "material": "Concrete",     "height": "Mid-Rise",  "H": None, "M": None, "L": [11,17,32,51],   "P": [9,14,25,41]},
    "C3H":  {"name": "Concrete + URM Infill",            "material": "Concrete",     "height": "High-Rise", "H": None, "M": None, "L": [9,16,33,53],    "P": [8,13,27,43]},
    "PC1":  {"name": "Precast Concrete Tilt-Up",         "material": "Concrete",     "height": "All",       "H": [20,35,72,125],  "M": [18,24,44,71],   "L": [13,17,25,45],   "P": [11,14,21,35]},
    "PC2L": {"name": "Precast Concrete Frames",          "material": "Concrete",     "height": "Low-Rise",  "H": [24,36,69,123],  "M": [18,25,40,74],   "L": [13,15,24,44],   "P": [10,13,19,35]},
    "PC2M": {"name": "Precast Concrete Frames",          "material": "Concrete",     "height": "Mid-Rise",  "H": [17,29,67,151],  "M": [15,21,45,86],   "L": [11,16,31,52],   "P": [9,13,24,42]},
    "PC2H": {"name": "Precast Concrete Frames",          "material": "Concrete",     "height": "High-Rise", "H": [12,23,63,149],  "M": [12,19,46,90],   "L": [11,16,31,55],   "P": [9,13,25,43]},
    "RM1L": {"name": "Reinf. Masonry + Wood Diaphr.",    "material": "Masonry",      "height": "Low-Rise",  "H": [30,46,93,157],  "M": [22,30,50,85],   "L": [16,20,29,54],   "P": [13,16,24,43]},
    "RM1M": {"name": "Reinf. Masonry + Wood Diaphr.",    "material": "Masonry",      "height": "Mid-Rise",  "H": [20,37,81,190],  "M": [18,26,51,103],  "L": [14,19,35,63],   "P": [11,15,28,50]},
    "RM2L": {"name": "Reinf. Masonry + Precast Diaphr.", "material": "Masonry",      "height": "Low-Rise",  "H": [26,42,87,149],  "M": [20,28,47,81],   "L": [14,18,28,51],   "P": [12,15,22,41]},
    "RM2M": {"name": "Reinf. Masonry + Precast Diaphr.", "material": "Masonry",      "height": "Mid-Rise",  "H": [17,33,75,183],  "M": [16,23,48,99],   "L": [12,17,34,60],   "P": [10,14,26,47]},
    "RM2H": {"name": "Reinf. Masonry + Precast Diaphr.", "material": "Masonry",      "height": "High-Rise", "H": [12,24,67,178],  "M": [12,20,48,101],  "L": [11,17,35,62],   "P": [9,13,27,50]},
    "URML": {"name": "Unreinforced Masonry",             "material": "Masonry",      "height": "Low-Rise",  "H": None, "M": None, "L": [14,20,32,46],   "P": [13,17,26,37]},
    "URMM": {"name": "Unreinforced Masonry",             "material": "Masonry",      "height": "Mid-Rise",  "H": None, "M": None, "L": [10,16,27,46],   "P": [9,13,21,38]},
    "MH":   {"name": "Mobile / Manufactured Homes",     "material": "Manufactured", "height": "Single",    "H": [11,18,31,60],   "M": [11,18,31,60],   "L": [11,18,31,60],   "P": [8,11,18,34]},
}
