"""Agent nodes. Each takes the shared state and returns a partial update."""
import difflib

from .. import tools
from ..config import DISCLAIMER
from ..kb.store import search
from ..llm import chat_json
from .state import DiagnosisState


def intake_agent(state: DiagnosisState) -> dict:
    p = state["patient"]
    out = chat_json(
        'Extract clinical symptoms from the note. Reply as JSON: {"symptoms": ["short symptom phrase", ...]}. '
        "Only include what the note states; do not infer or add.",
        p["note"],
    )
    symptoms = [str(s).strip() for s in out.get("symptoms", []) if str(s).strip()]
    return {"symptoms": symptoms}


def pattern_agent(state: DiagnosisState) -> dict:
    p = state["patient"]
    abnormal = []
    for lab in p.get("labs", []):
        flag = tools.lab_flag(lab["name"], lab["value"])
        if flag in ("low", "high"):
            abnormal.append({"kind": "lab", **lab, "flag": flag})
    for name, value in p.get("vitals", {}).items():
        flag = tools.vital_flag(name, value)
        if flag in ("low", "high"):
            abnormal.append({"kind": "vital", "name": name, "value": value, "unit": "", "flag": flag})

    red_flags = []
    labs = {l["name"]: l["value"] for l in p.get("labs", [])}
    v = p.get("vitals", {})
    if labs.get("troponin_i", 0) > 0.04:
        red_flags.append("Elevated troponin: possible myocardial injury. Urgent ECG and escalation.")
    if v.get("spo2", 100) < 90:
        red_flags.append("SpO2 below 90%: significant hypoxemia.")
    if v.get("bp_systolic", 120) < 90:
        red_flags.append("Systolic BP below 90: hypotension.")

    return {
        "abnormal": abnormal,
        "red_flags": red_flags,
        "interactions": tools.check_interactions(p.get("medications", [])),
    }


def _summary(state: DiagnosisState) -> str:
    p = state["patient"]
    ab = "; ".join(f"{a['name']}={a['value']}{a['unit']} ({a['flag']})" for a in state.get("abnormal", []))
    return (
        f"Age {p['age']}, sex {p['sex']}.\n"
        f"Symptoms: {', '.join(state.get('symptoms', []))}.\n"
        f"Abnormal findings: {ab or 'none'}.\n"
        f"Medications: {', '.join(p.get('medications', [])) or 'none'}."
    )


def retrieval_agent(state: DiagnosisState) -> dict:
    return {"evidence": search(_summary(state))}


def differential_agent(state: DiagnosisState) -> dict:
    docs = "\n\n".join(f"[{d['id']}]\n{d['text']}" for d in state["evidence"])
    out = chat_json(
        "You are a clinical decision-support assistant helping a doctor. Using ONLY the patient summary and the "
        "reference documents, list up to 3 probable diagnoses, most likely first. Reply as JSON: "
        '{"differential": [{"diagnosis": str, "confidence": number 0-1, '
        '"supporting_evidence": [str, ...], "sources": [doc ids], "next_tests": [str, ...]}]}. '
        "Cite only document ids shown in brackets. Supporting evidence must come from the patient summary.",
        f"PATIENT SUMMARY:\n{_summary(state)}\n\nREFERENCE DOCUMENTS:\n{docs}",
    )
    return {"differential": out.get("differential", [])}


def critic_agent(state: DiagnosisState) -> dict:
    """Deterministic safety pass: validate citations, normalise confidence, attach ICD-10, escalate red flags."""
    valid_ids = {d["id"] for d in state["evidence"]}
    notes, cleaned = [], []
    for d in state.get("differential", []):
        name = str(d.get("diagnosis", "")).strip()
        if not name:
            continue
        close = difflib.get_close_matches(name, tools.ICD10, n=1, cutoff=0.85)
        if close and close[0] != name:
            notes.append(f"{name}: normalised to '{close[0]}'.")
            name = close[0]
        sources = [s for s in d.get("sources", []) if s in valid_ids]
        dropped = len(d.get("sources", [])) - len(sources)
        if dropped:
            notes.append(f"{name}: removed {dropped} citation(s) not in retrieved evidence.")
        if not sources:
            notes.append(f"{name}: no valid citation, flagged as unsupported.")
        try:
            conf = max(0.0, min(1.0, float(d.get("confidence", 0))))
        except (TypeError, ValueError):
            conf = 0.0
        if not sources:
            conf = min(conf, 0.2)
        cleaned.append({
            "diagnosis": name,
            "confidence": conf,
            "supporting_evidence": [str(e) for e in d.get("supporting_evidence", [])],
            "sources": sources,
            "next_tests": [str(t) for t in d.get("next_tests", [])],
            "icd10": tools.icd10_lookup(name),
            "supported": bool(sources),
        })
    cleaned.sort(key=lambda x: x["confidence"], reverse=True)
    for rf in state.get("red_flags", []):
        notes.append(f"RED FLAG: {rf}")
    if not cleaned:
        notes.append("No usable differential produced; clinician review required.")
    return {"differential": cleaned, "critic_notes": notes}


def report_agent(state: DiagnosisState) -> dict:
    p = state["patient"]
    lines = [f"# Diagnostic support report: {p['id']}", f"_{DISCLAIMER}_", ""]
    if state.get("red_flags"):
        lines += ["## Urgent flags"] + [f"- **{r}**" for r in state["red_flags"]] + [""]
    lines += ["## Abnormal findings"]
    lines += [f"- {a['name']}: {a['value']} {a['unit']} ({a['flag']})" for a in state.get("abnormal", [])] or ["- none"]
    if state.get("interactions"):
        lines += ["", "## Medication interaction warnings"] + [f"- {i}" for i in state["interactions"]]
    lines += ["", "## Probable diagnoses"]
    for i, d in enumerate(state.get("differential", []), 1):
        code = f" ({d['icd10']})" if d.get("icd10") else ""
        lines.append(f"{i}. **{d['diagnosis']}**{code}: confidence {d['confidence']:.0%}")
        if d["supporting_evidence"]:
            lines.append("   - Evidence: " + "; ".join(d["supporting_evidence"]))
        if d["next_tests"]:
            lines.append("   - Suggested tests: " + "; ".join(d["next_tests"]))
        lines.append("   - Sources: " + (", ".join(d["sources"]) or "NONE (unsupported)"))
    if state.get("critic_notes"):
        lines += ["", "## Safety review notes"] + [f"- {n}" for n in state["critic_notes"]]
    return {"report": "\n".join(lines)}
