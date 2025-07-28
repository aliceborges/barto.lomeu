import streamlit as st
from utils import layout, api, charts

st.set_page_config(
    page_title="barto.lomeu",
    page_icon="front/assets/barto.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

layout.show_header()
layout.url_form()

st.title("Estatísticas")
df_stats = api.get_all_stats()
charts.show_url_stats(df_stats)

st.subheader("Histórico de Acessos")
df_history = api.get_history()
charts.show_click_history(df_history)
