"""Neon dark theme: Jet Black #0A0A0A, Cerulean Blue #007BA7, Neon Rose #FF2D95."""
import streamlit as st

CSS = """
<style>
h1 {
    background: linear-gradient(90deg, #1FB6E8, #FF2D95);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
h2, h3 { color: #1FB6E8; }
div[data-testid="stMetric"] {
    background: #14141C;
    border: 1px solid #22303a;
    border-left: 4px solid #FF2D95;
    padding: 14px 16px;
    border-radius: 12px;
}
div[data-testid="stMetricValue"] { color: #1FB6E8; }
button[kind="primary"] { border-radius: 10px; font-weight: 700; }
section[data-testid="stSidebar"] { border-right: 1px solid #22303a; }
</style>
"""


def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)
