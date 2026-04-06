import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Obter o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "consulta.csv")

df = pd.read_csv(csv_path, sep=';', encoding='latin-1', index_col=0)

# Remover a coluna "Variável" 
df = df.drop(columns=['Variável'])

# Converter strings com pontos para números
for col in df.columns:
    df[col] = df[col].astype(str).str.replace('.', '').astype(float)

# Transpor para ter anos nas colunas
df_transposed = df.T

# Criar gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_transposed, marker='o')

plt.title("Evolução dos dados ao longo dos anos")
plt.xlabel("Ano")
plt.ylabel("Valores")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()