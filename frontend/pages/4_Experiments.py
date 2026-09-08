"""Experiments page for CI Bottleneck Analyzer.

Allows the user to create a new experiment (associating it with a build) and view
existing experiment results. Data is fetched from the FastAPI backend.
"""

import streamlit as st
import requests
from typing import List, Dict, Any

BASE_URL = "http://localhost:8000"

def create_experiment(build_id: str, description: str) -> Dict[str, Any]:
    payload = {"build_id": build_id, "description": description}
    try:
        resp = requests.post(f"{BASE_URL}/experiments", json=payload)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to create experiment: {e}")
        return {}

def fetch_experiment(build_id: str) -> Dict[str, Any]:
    try:
        resp = requests.get(f"{BASE_URL}/experiments/{build_id}")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch experiment: {e}")
        return {}

def run():
    st.title("🔬 Experiments")
    st.markdown("---")

    st.subheader("Create New Experiment")
    with st.form(key="exp_form"):
        build_id = st.text_input("Build ID")
        description = st.text_area("Description (optional)")
        submit = st.form_submit_button("Create")
        if submit:
            if not build_id:
                st.warning("Build ID is required.")
            else:
                result = create_experiment(build_id, description)
                if result:
                    st.success("Experiment created!")
                    st.json(result)

    st.subheader("View Experiment Results")
    view_id = st.text_input("Enter Build ID to view experiment")
    if st.button("Fetch"):
        if view_id:
            data = fetch_experiment(view_id)
            if data:
                st.json(data)
        else:
            st.warning("Please provide a Build ID.")
