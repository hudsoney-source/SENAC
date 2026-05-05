# Carrega os dados do arquivo CSV
#data = pd.read_csv('casos-covid-go.csv')

# Mostra as últimas linhas do dataset
#data.tail()

# Filtra apenas dados no nível de estado
#estados = data.loc[data.place_type == 'state']

# Filtra apenas o estado de Goiás (GO)
#estados_go = estados.loc[estados.state == 'GO']

# Agrupa por data e soma o número de mortes (deaths)
#estados_go_confirmados = estados_go.groupby('date').sum()['deaths'].reset_index()

# Converte a coluna de data para formato datetime
#estados_go_confirmados['date'] = pd.to_datetime(estados_go_confirmados['date'])

# Mostra as últimas linhas
#estados_go_confirmados.tail()

# Define os atributos (X) e o alvo (Y)
#atributos = ['date']
#atributos_prev = ['deaths']

# Separa os dados em entrada (X) e saída (Y)
#X = estados_go_confirmados[atributos].values
#Y = estados_go_confirmados[atributos_prev].values

# Divide os dados em treino (70%) e teste (30%)
#X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size=0.30)

# Cria o modelo KNN com 4 vizinhos
#knn = KNeighborsRegressor(n_neighbors=4)

# Treina o modelo
#knn.fit(X_treino, Y_treino)

# Faz uma previsão para uma data específica
#pred = knn.predict(np.array(pd.to_datetime(['2021-11-01'])).reshape(-1, 1))

# Mostra a previsão
#pred

# Avalia o modelo com dados de teste
#knn.score(X_teste, Y_teste)

# Cria o modelo Random Forest
#modelRF = RandomForestRegressor()

# Treina o modelo (usando ravel para ajustar o formato do Y)
#modelRF.fit(X_treino, Y_treino.ravel())

# Faz previsão com Random Forest
#predicaoRF = modelRF.predict(np.array(pd.to_datetime(['2021-11-01'])).reshape(-1, 1))

# Mostra a previsão
#predicaoRF

# Avalia o modelo
#modelRF.score(X_teste, Y_teste)


#Explicação simples:

#Você carrega os dados de COVID.
#Filtra apenas o estado de Goiás.
#Agrupa os dados por data e soma as mortes por dia.
#Converte a data para um formato que o modelo entende.
#Divide os dados em treino e teste.

#Depois aplica dois modelos de Machine Learning:
#- KNN (K-Nearest Neighbors): prevê com base em valores parecidos do passado.
#- Random Forest: usa várias árvores de decisão para prever.

#Ambos fazem previsão para uma data específica (01/11/2021).
#E por fim você avalia qual modelo teve melhor desempenho.