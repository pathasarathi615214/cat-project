"""Streamlit entry point for CI Bottleneck Analyzer dashboard.

Provides navigation between the different analysis pages.
"""

import streamlit as st

# Set page configuration
st.set_page_config(page_title="CI Bottleneck Analyzer", layout="wide")

# Sidebar navigation
pages = {
    "Dashboard": "pages/1_Dashboard.py",
    "Build Analysis": "pages/2_Build_Analysis.py",
    "Recommendations": "pages/3_Recommendations.py",
    "Experiments": "pages/4_Experiments.py",
    "Legacy Migration": "pages/5_Legacy_Migration.py",
    "Error Analysis": "pages/6_Error_Analysis.py",
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Dynamically import and run selected page module
module_path = pages[selection]

# Using importlib to load the page script
import importlib.util, sys, os

full_path = os.path.join(os.path.dirname(__file__), module_path)
spec = importlib.util.spec_from_file_location("page_module", full_path)
module = importlib.util.module_from_spec(spec)
sys.modules["page_module"] = module
spec.loader.exec_module(module)

# Each page script must expose a `run()` function
if hasattr(module, "run"):
    module.run()
else:
    st.error(f"Page {selection} does not define a run() function.")
