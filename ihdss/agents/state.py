from typing import TypedDict


class DiagnosisState(TypedDict, total=False):
    patient: dict
    symptoms: list[str]          # Intake
    abnormal: list[dict]         # Pattern: flagged labs/vitals
    red_flags: list[str]         # Pattern
    interactions: list[str]      # Pattern
    evidence: list[dict]         # Retrieval: [{id, text, distance}]
    differential: list[dict]     # Differential -> Critic
    critic_notes: list[str]      # Critic
    report: str                  # Report
