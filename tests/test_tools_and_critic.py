from ihdss import tools
from ihdss.agents.nodes import critic_agent, pattern_agent
from ihdss.data.synthetic import PATIENTS


def test_lab_flags():
    assert tools.lab_flag("hba1c", 8.4) == "high"
    assert tools.lab_flag("hemoglobin", 8.9) == "low"
    assert tools.lab_flag("sodium", 140) == "normal"
    assert tools.lab_flag("nonexistent", 1) == "unknown"


def test_interactions():
    assert tools.check_interactions(["furosemide", "ibuprofen", "lisinopril"])
    assert tools.check_interactions(["metformin"]) == []


def test_pattern_red_flag_troponin():
    p = next(x for x in PATIENTS if x["id"] == "P003")
    out = pattern_agent({"patient": p})
    assert any("troponin" in r.lower() for r in out["red_flags"])


def test_critic_removes_bad_citations_and_caps_confidence():
    state = {
        "evidence": [{"id": "pneumonia", "text": "", "distance": 0}],
        "differential": [
            {"diagnosis": "Community-acquired pneumonia", "confidence": 0.9, "sources": ["pneumonia", "fake"]},
            {"diagnosis": "Made up disease", "confidence": 0.95, "sources": ["fake"]},
        ],
        "red_flags": [],
    }
    out = critic_agent(state)
    top, second = out["differential"]
    assert top["sources"] == ["pneumonia"] and top["supported"]
    assert second["confidence"] <= 0.2 and not second["supported"]
    assert top["icd10"] == "J18.9"
