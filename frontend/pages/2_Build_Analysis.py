"""Build Analysis page for CI Bottleneck Analyzer.

Shows a table of recent builds with sortable columns and allows filtering by status,
service, or pipeline. Displays detailed info for a selected build.
"""

import streamlit as st
import requests
from typing import List, Dict, Any

BASE_URL = "http://localhost:8000"

def fetch_builds(limit: int = 100) -> List[Dict[str, Any]]:
    try:
        resp = requests.get(f"{BASE_URL}/builds?skip=0&limit={limit}")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch builds: {e}")
        return []

def run():
    st.title("🔎 Build Analysis")
    st.markdown("---")

    builds = fetch_builds()
    if not builds:
        st.info("No build data available.")
        return

    # Convert timestamps to readable format
    for b in builds:
        for key in ["queued_at", "started_at", "finished_at"]:
            if b.get(key):
                b[key] = b[key].replace("T", " ")[:19]

    # Sidebar filters
    st.sidebar.header("Filters")
    status_options = sorted(set(b["status"] for b in builds))
    service_options = sorted(set(b["service_name"] for b in builds))
    pipeline_options = sorted(set(b["pipeline_name"] for b in builds))

    selected_status = st.sidebar.multiselect("Status", status_options, default=status_options)
    selected_service = st.sidebar.multiselect("Service", service_options, default=service_options)
    selected_pipeline = st.sidebar.multiselect("Pipeline", pipeline_options, default=pipeline_options)

    filtered = [b for b in builds if b["status"] in selected_status and b["service_name"] in selected_service and b["pipeline_name"] in selected_pipeline]

    st.subheader(f"Showing {len(filtered)} builds")
    st.dataframe(filtered, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.caption("Select a row in the table above to view more details (not implemented in this static view).")
