"""Legacy Migration page for CI Bottleneck Analyzer.

Demonstrates how to migrate a legacy CI pipeline configuration to the new
analysis framework. Shows a side‑by‑side comparison of a sample legacy config
(YAML) and the generated modern configuration (JSON). The data is static for the
demo purposes.
"""

import streamlit as st
import yaml
import json

# Sample legacy YAML configuration (static example)
LEGACY_YAML = """
pipeline:
  name: legacy-ci
  steps:
    - name: checkout
      command: git checkout master
    - name: build
      command: make build
    - name: test
      command: make test
    - name: deploy
      command: ./deploy.sh
"""

# Function to convert legacy YAML to modern JSON config (simplified)
def convert_to_modern(yaml_str: str) -> dict:
    data = yaml.safe_load(yaml_str)
    # Simple conversion: map steps to list of dicts with id and cmd
    modern = {
        "pipeline_name": data.get("pipeline", {}).get("name", "unknown"),
        "steps": [
            {"id": idx + 1, "name": step.get("name"), "command": step.get("command")}
            for idx, step in enumerate(data.get("pipeline", {}).get("steps", []))
        ],
    }
    return modern

def run():
    st.title("🔧 Legacy Migration")
    st.markdown("---")
    st.subheader("Legacy YAML Configuration")
    st.code(LEGACY_YAML, language="yaml")

    st.subheader("Converted Modern JSON Configuration")
    modern_cfg = convert_to_modern(LEGACY_YAML)
    st.json(modern_cfg)

    st.markdown("---")
    st.caption("This page illustrates how a legacy CI pipeline can be translated into the new format used by the CI Bottleneck Analyzer.")
