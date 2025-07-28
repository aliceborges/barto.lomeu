import streamlit as st
import validators
import requests
import os
import json

BASE_URL = os.getenv("BASE_URL", "http://localhost/")

def show_header():
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("front/assets/barto.png", width=50)
    with col2:
        st.title("barto.lomeu")

def url_form():
    with st.form("create_short_url", clear_on_submit=True, enter_to_submit=True, border=True, width="stretch", height="content"):
        long_url = st.text_input("Url*", help="Url do site que será encurtado", placeholder="https://codecon.dev/")
        code = st.text_input("Código", help="Código que será utilizado...", placeholder="CODECON")
        st.text("*Preenchimento Obrigatório")
        submitted = st.form_submit_button("Enviar")

        if submitted:
            if not long_url:
                st.error("O campo URL é obrigatório.")
            elif not validators.url(long_url):
                st.error("A URL informada não é válida.")
            else:
                payload = {"long_url": long_url}
                if code:
                    payload["code"] = code
                response = requests.post(f"{BASE_URL}/shorten_url", json=payload)
                content = json.loads(response.content)
                if "error" in content:
                    st.error(f"Erro: {content['error']}")
                elif "code" in content:
                    st.success(f"Url criada: {BASE_URL}/{content['code']}")
                else:
                    st.error("Erro inesperado.")
