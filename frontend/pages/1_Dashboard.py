"""Dashboard page for CI Bottleneck Analyzer.

Provides an overview of key metrics such as cache hit rate, parallel efficiency,
average queue time, and recent build summaries. Data is fetched from the FastAPI
backend endpoints.
"""

import streamlit as st
import requests
from typing import Dict, Any

# Backend base URL – adjust if running via Docker or different host.
BASE_URL = "http://localhost:8000"

def fetch_metrics() -> Dict[str, Any]:
    try:
        resp = requests.get(f"{BASE_URL}/metrics")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch metrics: {e}")
        return {}

def fetch_recent_builds(limit: int = 5):
    try:
        resp = requests.get(f"{BASE_URL}/builds?skip=0&limit={limit}")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch recent builds: {e}")
        return []

def run():
    st.title("🚀 CI Bottleneck Analyzer – Dashboard")
    st.markdown("---")

    # Fetch and display metrics
    metrics = fetch_metrics()
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Cache Hit Rate", value=f"{metrics.get('cache_hit_rate', 0):.2%}")
    with col2:
        st.metric(label="Parallel Efficiency", value=f"{metrics.get('parallel_efficiency', 0):.2%}")

    st.subheader("Average Queue Time (seconds)")
    st.metric(label="Avg Queue Time", value=f"{metrics.get('avg_queue_time_seconds', 0):.1f}")
    st.metric(label="Total Queued Builds", value=metrics.get('total_queued_builds', 0))

    st.subheader("Recent Builds")
    recent = fetch_recent_builds()
    if recent:
        for b in recent:
            st.write(f"- **{b['build_id']}** – {b['status'].upper()} – {b['service_name']} / {b['pipeline_name']}")
    else:
        st.info("No recent builds available.")

    st.markdown("---")
    st.caption("Data refreshed on each page load. Use the navigation pane to explore deeper analyses.")
