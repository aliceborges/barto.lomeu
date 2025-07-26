import json
import os

import requests
import streamlit as st
import pandas as pd
import validators
from dotenv import load_dotenv
from streamlit_dynamic_filters import DynamicFilters

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost/")

with st.form("create_short_url", clear_on_submit=True, enter_to_submit=True, border=True, width="stretch", height="content"):
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image("front/assets/barto.png", width=50)
    with col2:
        st.title("barto.lomeu")
    long_url = st.text_input("Url*")
    code = st.text_input("Código")
    st.text("*Preenchimento Obrigatório")
    submitted = st.form_submit_button("Enviar")

    if submitted:
        if not long_url:
            st.error("O campo URL é obrigatório.")
        elif not validators.url(long_url):
            st.error("A URL informada não é válida.")
        else:
            payload = {
                "long_url": long_url
            }

            if code:
                payload = {
                    "long_url": long_url,
                    "code": code
                }

            response = requests.post(f"{BASE_URL}/shorten_url", json=payload)
            content = json.loads(response.content)
            if "error" in content:
                st.error(f"Erro: {content["error"]}")
            elif "code" in content:
                response_code = content['code']
                st.success(f"Url criada: {BASE_URL}/{response_code}")
            else:
                st.error(f"Erro inesperado.")

all_urls_stats = requests.get(f"{BASE_URL}/all/stats")
content = json.loads(all_urls_stats.content)
dataframe_urls = {
    "Cliques": [],
    "Código": [],
    "Url": []
}
for url in content:
    dataframe_urls["Cliques"].append(url["clicks"])
    dataframe_urls["Código"].append(url["code"])
    dataframe_urls["Url"].append(url["long_url"])

df = pd.DataFrame(dataframe_urls)
dynamic_filters = DynamicFilters(df=df, filters=['Código', 'Url'], filters_name='Filtros')
dynamic_filters.display_filters(location='sidebar')
dynamic_filters.display_df()