"""Hand-built synthetic patients (no real PHI). `truth` is the ground-truth label used only by evals."""

PATIENTS = [
    {
        "id": "P001", "age": 58, "sex": "M", "truth": "Type 2 diabetes mellitus",
        "note": "Two months of increased thirst, frequent urination and fatigue. Blurry vision. Weight loss of 4 kg. Family history of diabetes.",
        "vitals": {"bp_systolic": 142, "bp_diastolic": 88, "heart_rate": 84, "temp_c": 36.8, "spo2": 97},
        "labs": [
            {"name": "glucose_fasting", "value": 186, "unit": "mg/dL"},
            {"name": "hba1c", "value": 8.4, "unit": "%"},
            {"name": "creatinine", "value": 1.0, "unit": "mg/dL"},
        ],
        "medications": ["lisinopril"],
    },
    {
        "id": "P002", "age": 67, "sex": "F", "truth": "Community-acquired pneumonia",
        "note": "Five days of productive cough with yellow sputum, fever and chills, right-sided pleuritic chest pain and shortness of breath.",
        "vitals": {"bp_systolic": 118, "bp_diastolic": 72, "heart_rate": 104, "temp_c": 38.9, "spo2": 91},
        "labs": [
            {"name": "wbc", "value": 15.2, "unit": "10^9/L"},
            {"name": "crp", "value": 120, "unit": "mg/L"},
            {"name": "creatinine", "value": 0.9, "unit": "mg/dL"},
        ],
        "medications": ["levothyroxine"],
    },
    {
        "id": "P003", "age": 61, "sex": "M", "truth": "Acute coronary syndrome",
        "note": "Crushing central chest pressure radiating to the left arm and jaw for 40 minutes, with sweating and nausea. Smoker, hypertensive.",
        "vitals": {"bp_systolic": 156, "bp_diastolic": 94, "heart_rate": 102, "temp_c": 36.9, "spo2": 96},
        "labs": [
            {"name": "troponin_i", "value": 2.8, "unit": "ng/mL"},
            {"name": "ldl", "value": 165, "unit": "mg/dL"},
            {"name": "creatinine", "value": 1.1, "unit": "mg/dL"},
        ],
        "medications": ["amlodipine", "aspirin"],
    },
    {
        "id": "P004", "age": 34, "sex": "F", "truth": "Iron deficiency anemia",
        "note": "Months of tiredness, pallor, dizziness on standing and brittle nails. Heavy menstrual periods. Craves ice.",
        "vitals": {"bp_systolic": 106, "bp_diastolic": 66, "heart_rate": 96, "temp_c": 36.7, "spo2": 98},
        "labs": [
            {"name": "hemoglobin", "value": 8.9, "unit": "g/dL"},
            {"name": "mcv", "value": 70, "unit": "fL"},
            {"name": "ferritin", "value": 6, "unit": "ng/mL"},
        ],
        "medications": [],
    },
    {
        "id": "P005", "age": 45, "sex": "F", "truth": "Hypothyroidism",
        "note": "Gradual weight gain, constipation, cold intolerance, dry skin and low mood over six months. Hair thinning.",
        "vitals": {"bp_systolic": 124, "bp_diastolic": 80, "heart_rate": 54, "temp_c": 36.2, "spo2": 98},
        "labs": [
            {"name": "tsh", "value": 12.5, "unit": "mIU/L"},
            {"name": "free_t4", "value": 0.5, "unit": "ng/dL"},
            {"name": "ldl", "value": 148, "unit": "mg/dL"},
        ],
        "medications": [],
    },
    {
        "id": "P006", "age": 72, "sex": "M", "truth": "Congestive heart failure",
        "note": "Worsening breathlessness on exertion, needs three pillows to sleep, ankle swelling and weight gain of 3 kg in one week.",
        "vitals": {"bp_systolic": 132, "bp_diastolic": 82, "heart_rate": 92, "temp_c": 36.8, "spo2": 92},
        "labs": [
            {"name": "bnp", "value": 980, "unit": "pg/mL"},
            {"name": "creatinine", "value": 1.6, "unit": "mg/dL"},
            {"name": "sodium", "value": 132, "unit": "mmol/L"},
        ],
        "medications": ["furosemide", "ibuprofen", "lisinopril"],
    },
]
