import streamlit as st

from ihdss import db
from ihdss.agents.graph import diagnose
from ihdss.config import DISCLAIMER
from ihdss.setup_data import main as setup

st.set_page_config(page_title="IHDSS", page_icon="🩺", layout="wide")
st.title("Intelligent Healthcare Diagnosis Support System")
st.warning(DISCLAIMER)


@st.cache_resource
def _init():
    setup()
    return True


_init()
patients = {p["id"]: p for p in db.list_patients()}
pid = st.sidebar.selectbox("Patient", list(patients), format_func=lambda i: f"{i} ({patients[i]['age']}{patients[i]['sex']})")
p = patients[pid]

left, right = st.columns([1, 2])
with left:
    st.subheader("Record")
    st.write(p["note"])
    st.json({"vitals": p["vitals"], "labs": p["labs"], "medications": p["medications"]}, expanded=False)
    run = st.button("Run diagnostic agents", type="primary")

if run:
    with st.spinner("Agents working (local Ollama model)..."):
        st.session_state[pid] = diagnose(p)

result = st.session_state.get(pid)
with right:
    if not result:
        st.info("Select a patient and run the agents.")
    else:
        st.markdown(result["report"])
        st.subheader("Clinician review")
        for d in result["differential"]:
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(d["diagnosis"])
            if c2.button("Accept", key=f"a-{pid}-{d['diagnosis']}"):
                db.save_feedback(pid, d["diagnosis"], "accept")
                st.toast("Saved")
            if c3.button("Reject", key=f"r-{pid}-{d['diagnosis']}"):
                db.save_feedback(pid, d["diagnosis"], "reject")
                st.toast("Saved")
        with st.expander("Retrieved evidence"):
            for e in result["evidence"]:
                st.markdown(f"**{e['id']}** (distance {e['distance']:.3f})\n\n{e['text']}")
