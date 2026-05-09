from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib as mat

mat.use("Agg")

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "autos.csv"


def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH, encoding="latin-1", low_memory=False)

    colunas_necessarias = [
        "seller",
        "price",
        "vehicleType",
        "yearOfRegistration",
        "gearbox",
        "powerPS",
        "brand",
    ]
    df = df[colunas_necessarias].copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["yearOfRegistration"] = pd.to_numeric(
        df["yearOfRegistration"], errors="coerce"
    )
    df["powerPS"] = pd.to_numeric(df["powerPS"], errors="coerce")

    for coluna in ["seller", "vehicleType", "gearbox", "brand"]:
        df[coluna] = df[coluna].astype("string").str.strip().str.lower()

    df = df.dropna(subset=["price", "vehicleType", "yearOfRegistration", "brand"])
    df = df[df["price"].between(1, 350000)]
    df = df[df["yearOfRegistration"].between(1900, 2016)]
    df = df[df["powerPS"].fillna(0).between(0, 2000)]

    return df


def salvar_plot(nome_arquivo: str) -> None:
    caminho = BASE_DIR / nome_arquivo
    plt.tight_layout()
    plt.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close()


def questao_1(df: pd.DataFrame) -> None:
    plt.figure(figsize=(14, 6))
    sb.histplot(
        data=df,
        x="yearOfRegistration",
        bins=np.arange(df["yearOfRegistration"].min(), df["yearOfRegistration"].max() + 2),
        color="#2a9d8f",
    )
    plt.title("Distribuicao de Veiculos com Base no Ano de Registro")
    plt.xlabel("Ano de Registro")
    plt.ylabel("Quantidade de Veiculos")
    plt.xticks(rotation=45)
    salvar_plot("01_distribuicao_ano_registro.png")


def questao_2(df: pd.DataFrame) -> None:
    ordem = df["vehicleType"].value_counts().index
    plt.figure(figsize=(14, 7))
    sb.boxplot(
        data=df,
        x="vehicleType",
        y="price",
        order=ordem,
        color="#8ecae6",
        showfliers=True,
    )
    plt.title("Boxplot da Faixa de Preco por Tipo de Veiculo")
    plt.xlabel("Tipo de Veiculo")
    plt.ylabel("Preco")
    plt.xticks(rotation=45)
    salvar_plot("02_boxplot_preco_por_tipo_veiculo.png")


def questao_3(df: pd.DataFrame) -> None:
    ordem = df["vehicleType"].value_counts().index
    plt.figure(figsize=(12, 6))
    sb.countplot(data=df, x="vehicleType", order=ordem, color="#219ebc")
    plt.title("Contagem Total de Veiculos por Tipo de Veiculo")
    plt.xlabel("Tipo de Veiculo")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45)
    salvar_plot("03_countplot_tipo_veiculo.png")


def questao_4(df: pd.DataFrame) -> None:
    contagem_marca = df["brand"].value_counts().sort_values(ascending=False)
    plt.figure(figsize=(14, 10))
    sb.barplot(
        x=contagem_marca.values,
        y=contagem_marca.index,
        color="#264653",
        orient="h",
    )
    plt.title("Numero de Veiculos por Marca")
    plt.xlabel("Quantidade")
    plt.ylabel("Marca")
    salvar_plot("04_plot_quantidade_por_marca.png")


def questao_5(df: pd.DataFrame) -> None:
    media_preco = (
        df.dropna(subset=["gearbox"])
        .groupby(["vehicleType", "gearbox"], as_index=False)["price"]
        .mean()
    )

    plt.figure(figsize=(14, 7))
    sb.barplot(data=media_preco, x="vehicleType", y="price", hue="gearbox")
    plt.title("Preco Medio por Tipo de Veiculo e Caixa de Cambio")
    plt.xlabel("Tipo de Veiculo")
    plt.ylabel("Preco Medio")
    plt.xticks(rotation=45)
    salvar_plot("05_preco_medio_tipo_veiculo_cambio.png")


def questao_6(df: pd.DataFrame) -> None:
    media_preco_vendedor = (
        df.dropna(subset=["seller"])
        .groupby(["vehicleType", "seller"], as_index=False)["price"]
        .mean()
    )

    plt.figure(figsize=(14, 7))
    sb.barplot(data=media_preco_vendedor, x="vehicleType", y="price", hue="seller")
    plt.title("Preco Medio do Veiculo por Tipo de Veiculo e Tipo de Vendedor")
    plt.xlabel("Tipo de Veiculo")
    plt.ylabel("Preco Medio")
    plt.xticks(rotation=45)
    salvar_plot("06_preco_medio_tipo_veiculo_vendedor.png")


def questao_7(df: pd.DataFrame) -> None:
    potencia_media = (
        df.dropna(subset=["gearbox", "powerPS"])
        .groupby(["vehicleType", "gearbox"], as_index=False)["powerPS"]
        .mean()
    )

    plt.figure(figsize=(14, 7))
    sb.barplot(data=potencia_media, x="vehicleType", y="powerPS", hue="gearbox")
    plt.title("Potencia Media por Tipo de Veiculo e Caixa de Cambio")
    plt.xlabel("Tipo de Veiculo")
    plt.ylabel("Potencia Media (PS)")
    plt.xticks(rotation=45)
    salvar_plot("07_potencia_media_tipo_veiculo_cambio.png")


def questao_8(df: pd.DataFrame) -> pd.DataFrame:
    marcas = sorted(df["brand"].dropna().unique())
    tipos_veiculo = sorted(df["vehicleType"].dropna().unique())
    tabela_media = pd.DataFrame(index=marcas, columns=tipos_veiculo, dtype=float)

    for marca in marcas:
        for tipo in tipos_veiculo:
            filtro = df[(df["brand"] == marca) & (df["vehicleType"] == tipo)]
            tabela_media.loc[marca, tipo] = filtro["price"].mean()

    tabela_media = tabela_media.round(2)
    tabela_media.to_csv(BASE_DIR / "08_tabela_media_preco_marca_veiculo.csv", encoding="utf-8-sig")
    print("\n8 - Tabela com a media de preco por marca e por veiculo:\n")
    print(tabela_media.fillna("-"))
    return tabela_media


def questao_9(tabela_media: pd.DataFrame) -> None:
    plt.figure(figsize=(16, 12))
    sb.heatmap(tabela_media, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5)
    plt.title("Heatmap do Preco Medio por Marca e Tipo de Veiculo")
    plt.xlabel("Tipo de Veiculo")
    plt.ylabel("Marca")
    salvar_plot("09_heatmap_preco_medio_marca_tipo.png")


def main() -> None:
    sb.set_theme(style="whitegrid")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {DATASET_PATH}. Coloque o autos.csv nesta pasta."
        )

    df = carregar_dados()

    print("Dataset carregado com sucesso.")
    print(f"Registros apos limpeza: {len(df)}")

    print("1 - Gerando distribuicao por ano de registro...")
    questao_1(df)

    print("2 - Gerando boxplot de preco por tipo de veiculo...")
    questao_2(df)

    print("3 - Gerando count plot por tipo de veiculo...")
    questao_3(df)

    print("4 - Gerando plot de quantidade por marca...")
    questao_4(df)

    print("5 - Gerando preco medio por tipo de veiculo e caixa de cambio...")
    questao_5(df)

    print("6 - Gerando preco medio por tipo de veiculo e tipo de vendedor...")
    questao_6(df)

    print("7 - Gerando potencia media por tipo de veiculo e caixa de cambio...")
    questao_7(df)

    print("8 - Calculando tabela de media de preco por marca e por veiculo...")
    tabela_media = questao_8(df)

    print("9 - Gerando heatmap de preco medio por marca e tipo de veiculo...")
    questao_9(tabela_media)

    print("\nArquivos gerados na pasta do exercicio:")
    arquivos = [
        "01_distribuicao_ano_registro.png",
        "02_boxplot_preco_por_tipo_veiculo.png",
        "03_countplot_tipo_veiculo.png",
        "04_plot_quantidade_por_marca.png",
        "05_preco_medio_tipo_veiculo_cambio.png",
        "06_preco_medio_tipo_veiculo_vendedor.png",
        "07_potencia_media_tipo_veiculo_cambio.png",
        "08_tabela_media_preco_marca_veiculo.csv",
        "09_heatmap_preco_medio_marca_tipo.png",
    ]
    for arquivo in arquivos:
        print(f"- {arquivo}")


if __name__ == "__main__":
    main()
