import streamlit as st
import altair as alt


def show_url_stats(df_raw):
    df = df_raw.rename(columns={"clicks": "Acessos", "code": "Código", "long_url": "Url"})
    col1, col2 = st.columns([5, 5])
    selected_codes = None
    selected_urls = None
    with col1:
        codes = df["Código"].unique()
        selected_codes = st.multiselect(
            "Códigos:",
            options=codes,
            default=list(codes),
        )
    with col2:
        urls = df["Url"].unique()
        selected_urls = st.multiselect(
            "Urls:",
            options=urls,
            default=list(urls),
        )
    df = df[df["Código"].isin(selected_codes)]
    df = df[df["Url"].isin(selected_urls)]
    df_sorted = df.sort_values(by="Acessos", ascending=False)
    chart = (
        alt.Chart(df_sorted)
        .mark_bar()
        .encode(
            x=alt.X("Código:N", sort='-y', title="Código"),
            y=alt.Y("Acessos:Q", title="Quantidade de Acessos"),
            color="Código:N",
            tooltip=["Código", "Url", "Acessos"]
        )
        .properties(width=800, height=400, title="Acessos por URL")
    )
    st.altair_chart(chart, use_container_width=True)

def show_click_history(df_history):
    df = df_history.rename(columns={"code": "Código", "timestamp": "Data"})
    df = df.sort_values("Data")
    df["Cliques"] = df.groupby("Código").cumcount() + 1
    codes = df["Código"].unique()
    selected_codes = st.multiselect(
        "Códigos:",
        options=codes,
        default=list(codes),
    )
    df = df[df["Código"].isin(selected_codes)]

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Data:T", title="Data e Hora"),
            y=alt.Y("Cliques:Q", title="Acessos acumulados"),
            color="Código:N",
            tooltip=["Código", "Data", "Cliques"]
        )
        .properties(width=800, height=400, title="Evolução de Acessos por Código")
    )
    st.altair_chart(chart, use_container_width=True)
