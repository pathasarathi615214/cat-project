"""Error Analysis page for CI Bottleneck Analyzer.

Provides a searchable table of error log entries (static mock data) and visualizes
frequency of error types. In a real system this would query a logs service.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict

# Mock error data
ERROR_DATA = [
    {"timestamp": "2026-09-07 12:34:56", "build_id": "build_0010", "error": "OutOfMemoryError", "message": "Java heap space"},
    {"timestamp": "2026-09-07 13:01:22", "build_id": "build_0034", "error": "TimeoutError", "message": "Step exceeded time limit"},
    {"timestamp": "2026-09-07 14:15:09", "build_id": "build_0056", "error": "ConnectionError", "message": "Failed to fetch artifact"},
    {"timestamp": "2026-09-07 15:42:33", "build_id": "build_0078", "error": "OutOfMemoryError", "message": "Java heap space"},
    {"timestamp": "2026-09-07 16:05:44", "build_id": "build_0099", "error": "DependencyError", "message": "Missing library"},
]


def run():
    st.title("⚠️ Error Analysis")
    st.markdown("---")

    st.subheader("Error Log Table")
    df = pd.DataFrame(ERROR_DATA)
    st.dataframe(df, use_container_width=True)

    st.subheader("Error Frequency")
    freq = df["error"].value_counts().reset_index()
    freq.columns = ["Error Type", "Count"]
    st.bar_chart(freq.set_index("Error Type"))

    st.markdown("---")
    st.caption("This is a static demonstration. In production, error logs would be fetched from a logging backend and correlated with builds.")
