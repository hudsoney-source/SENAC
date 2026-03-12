import kagglehub
import pandas

# Download latest version
path = kagglehub.dataset_download("talhasiddique123/imdb-latest2025-top-250-rated-movies")

print("Path to dataset files:", path)

# Carregar os dados do arquivo CSV
data = pd.read_csv(path)

# Encontrar o filme mais antigo
oldest_movie = data.loc[data['Year'].idxmin()]

# Exibir apenas o ano de lançamento do filme mais antigo
print(f"Ano de lançamento do filme mais antigo: {oldest_movie['Year']}")