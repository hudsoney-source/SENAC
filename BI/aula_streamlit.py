from pathlib import Path

import pandas as pd
import streamlit as st


CSV_PATH = Path(__file__).with_name("financiamentoPecuaria.csv")
COLUNAS_ANOS = [str(ano) for ano in range(2014, 2025)]


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, encoding="utf-8", sep=";")
    df = df.replace("-", "0")

    for coluna in COLUNAS_ANOS:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0)

    df["Localidade"] = df["Localidade"].astype(str).str.strip()
    df["Md_Invest"] = df[COLUNAS_ANOS].mean(axis=1).round(2)
    return df


st.set_page_config(layout="wide")
st.title("Dashboard Financeiro - Agro Goias - 2014-2024")
st.write("Dashboard Financeiro - Tabela")

df = carregar_dados()
st.dataframe(df.style.format({"Md_Invest": "{:.2f}"}), use_container_width=True)

localidades = df.loc[df["Localidade"] != "Media", "Localidade"].unique().tolist()
opcoes_localidade = ["Todos"] + sorted(localidades)
localidade_selecionada = st.sidebar.selectbox("Selecione a Localidade:", opcoes_localidade)

colunas_anos = COLUNAS_ANOS
df_local = df[df["Localidade"] == localidade_selecionada]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if localidade_selecionada == "Todos":
        df_plot = df[df["Localidade"] != "Media"]
        investimentos_ano = df_plot[colunas_anos].mean()
        st.write("### Media dos investimentos por ano")
        st.bar_chart(investimentos_ano)
    elif not df_local.empty:
        investimentos_local = df_local.iloc[0][colunas_anos]
        st.write(f"### Evolucao dos investimentos para {localidade_selecionada}")
        st.bar_chart(investimentos_local)
    else:
        st.error("Nenhum dado encontrado para essa localidade.")

with col2:
    st.write("### Grafico de linhas")
    if localidade_selecionada == "Todos":
        investimentos_ano = df[df["Localidade"] != "Media"][colunas_anos].mean()
        st.line_chart(investimentos_ano)
    elif not df_local.empty:
        investimentos_ano = df_local.iloc[0][colunas_anos]
        st.line_chart(investimentos_ano)
    else:
        st.info("Selecione uma localidade valida.")

with col3:
    st.write("### Comparacao com a media geral")
    if localidade_selecionada != "Todos" and not df_local.empty:
        investimentos_local = df_local.iloc[0][colunas_anos]
        investimentos_media = df[df["Localidade"] != "Media"][colunas_anos].mean()

        df_comparacao = pd.DataFrame(
            {
                "Ano": colunas_anos,
                localidade_selecionada: investimentos_local.values,
                "Media Geral": investimentos_media.values,
            }
        ).set_index("Ano")

        st.bar_chart(df_comparacao)
    else:
        st.info("Selecione uma localidade para visualizar a comparacao.")

with col4:
    st.write("### Ano com maior investimento")
    if localidade_selecionada != "Todos" and not df_local.empty:
        investimentos_local = df_local.iloc[0][colunas_anos]
        ano_max = investimentos_local.idxmax()
        valor_max = float(investimentos_local.max())
        st.metric("Ano com Maior Investimento", ano_max, f"R$ {valor_max:,.2f}")
    else:
        st.info("Selecione uma localidade especifica para visualizar o maior investimento.")
