"""Deterministic clinical tools (lab ranges, drug interactions, ICD-10 lookup). Exposed to agents as plain functions."""

# (low, high, unit). Simplified adult reference ranges.
LAB_RANGES = {
    "glucose_fasting": (70, 99, "mg/dL"),
    "hba1c": (4.0, 5.6, "%"),
    "creatinine": (0.6, 1.3, "mg/dL"),
    "wbc": (4.0, 11.0, "10^9/L"),
    "crp": (0, 5, "mg/L"),
    "troponin_i": (0, 0.04, "ng/mL"),
    "ldl": (0, 100, "mg/dL"),
    "hemoglobin": (12.0, 17.5, "g/dL"),
    "mcv": (80, 100, "fL"),
    "ferritin": (15, 200, "ng/mL"),
    "tsh": (0.4, 4.0, "mIU/L"),
    "free_t4": (0.8, 1.8, "ng/dL"),
    "bnp": (0, 100, "pg/mL"),
    "sodium": (135, 145, "mmol/L"),
}

VITAL_RANGES = {
    "bp_systolic": (90, 130), "bp_diastolic": (60, 85), "heart_rate": (60, 100),
    "temp_c": (36.1, 37.8), "spo2": (95, 100),
}

# Unordered pair -> warning
INTERACTIONS = {
    frozenset({"ibuprofen", "lisinopril"}): "NSAID + ACE inhibitor: reduced antihypertensive effect, kidney injury risk.",
    frozenset({"ibuprofen", "furosemide"}): "NSAID blunts diuretic effect and can worsen kidney function / heart failure.",
    frozenset({"aspirin", "ibuprofen"}): "Ibuprofen can interfere with the antiplatelet effect of aspirin; GI bleeding risk.",
}

ICD10 = {
    "Type 2 diabetes mellitus": "E11",
    "Community-acquired pneumonia": "J18.9",
    "Acute coronary syndrome": "I24.9",
    "Iron deficiency anemia": "D50.9",
    "Hypothyroidism": "E03.9",
    "Congestive heart failure": "I50.9",
}


def lab_flag(name: str, value: float) -> str:
    rng = LAB_RANGES.get(name)
    if not rng:
        return "unknown"
    if value < rng[0]:
        return "low"
    if value > rng[1]:
        return "high"
    return "normal"


def vital_flag(name: str, value: float) -> str:
    rng = VITAL_RANGES.get(name)
    if not rng:
        return "unknown"
    return "low" if value < rng[0] else "high" if value > rng[1] else "normal"


def check_interactions(meds: list[str]) -> list[str]:
    meds = [m.lower() for m in meds]
    out = []
    for i, a in enumerate(meds):
        for b in meds[i + 1:]:
            msg = INTERACTIONS.get(frozenset({a, b}))
            if msg:
                out.append(f"{a} + {b}: {msg}")
    return out


def icd10_lookup(diagnosis: str) -> str | None:
    d = diagnosis.lower()
    for name, code in ICD10.items():
        if name.lower() in d or d in name.lower():
            return code
    return None
