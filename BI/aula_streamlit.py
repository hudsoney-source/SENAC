from pathlib import Path

import pandas as pd
import streamlit as st


CSV_PATH = Path(__file__).with_name("financiamentoPecuaria.csv")
YEAR_COLUMNS = [str(year) for year in range(2014, 2025)]


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, encoding="utf-8", sep=";")
    df = df.replace("-", "0")

    for column in YEAR_COLUMNS:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def main() -> None:
    st.set_page_config(page_title="Financiamento da Pecuaria", layout="wide")
    st.title("Financiamentos a Pecuaria em Goias")

    df = load_data()

    st.subheader("Base tratada")
    st.dataframe(df, use_container_width=True)

    total_2024 = df["2024"].sum()
    maior_cidade_2024 = df.loc[df["2024"].idxmax(), "Localidade"]

    col1, col2 = st.columns(2)
    col1.metric("Total financiado em 2024", f"R$ {total_2024:,.2f}")
    col2.metric("Maior valor em 2024", maior_cidade_2024)

    cidade = st.selectbox("Selecione uma localidade", sorted(df["Localidade"].unique()))
    serie_cidade = df.loc[df["Localidade"] == cidade, YEAR_COLUMNS].T
    serie_cidade.columns = ["Valor"]

    st.subheader(f"Evolucao anual de {cidade}")
    st.line_chart(serie_cidade)

    ranking_2024 = (
        df[["Localidade", "2024"]]
        .sort_values("2024", ascending=False)
        .head(10)
        .set_index("Localidade")
    )

    st.subheader("Top 10 localidades em 2024")
    st.bar_chart(ranking_2024)


if __name__ == "__main__":
    main()