"""Single Streamlit entry point for all three Python portfolio dashboards."""
import importlib.util
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
PROJECTS = {
    "Project 1 — Python Sales Analysis": ROOT / "project-1-python-sales-analysis" / "app.py",
    "Project 2 — Executive Sales Dashboard": ROOT / "project-2-excel-sales-dashboard" / "app.py",
    "Project 3 — Power BI-style Analytics": ROOT / "project-3-power-bi-analytics" / "app.py",
}


def load_project(path):
    spec = importlib.util.spec_from_file_location("portfolio_dashboard", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


st.set_page_config(page_title="Future DS Python Dashboards", page_icon="📊", layout="wide")
st.sidebar.title("Future DS dashboards")
choice = st.sidebar.radio("Choose a project", list(PROJECTS))
st.sidebar.caption("All three dashboards use the shared Superstore dataset.")
load_project(PROJECTS[choice]).main()