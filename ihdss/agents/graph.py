from langgraph.graph import END, START, StateGraph

from .. import db
from .nodes import (critic_agent, differential_agent, intake_agent, pattern_agent,
                    report_agent, retrieval_agent)
from .state import DiagnosisState


def build_graph():
    g = StateGraph(DiagnosisState)
    for name, fn in [
        ("intake", intake_agent), ("pattern", pattern_agent), ("retrieval", retrieval_agent),
        ("differential", differential_agent), ("critic", critic_agent), ("report", report_agent),
    ]:
        g.add_node(name, fn)
    g.add_edge(START, "intake")
    g.add_edge("intake", "pattern")
    g.add_edge("pattern", "retrieval")
    g.add_edge("retrieval", "differential")
    g.add_edge("differential", "critic")
    g.add_edge("critic", "report")
    g.add_edge("report", END)
    return g.compile()


def diagnose(patient: dict) -> DiagnosisState:
    """Run the full pipeline. The ground-truth label is never shown to the agents."""
    visible = {k: v for k, v in patient.items() if k != "truth"}
    result = build_graph().invoke({"patient": visible})
    db.audit(patient["id"], "diagnosis_run", {
        "differential": [(d["diagnosis"], d["confidence"]) for d in result.get("differential", [])],
        "red_flags": result.get("red_flags", []),
    })
    return result
