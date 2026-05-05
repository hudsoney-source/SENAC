# Importa os dados de um arquivo CSV para um DataFrame do pandas
#data = pd.read_csv('casos-covid-go.csv')

# Mostra as últimas linhas do dataset (útil para ver como os dados estão no final)
#data.tail()

# Remove algumas colunas que não serão usadas e calcula a correlação entre as restantes
# Correlação mostra o quanto as variáveis estão relacionadas entre si (-1 a 1)
#data.drop(["date","state","city","place_type","is_last"], axis = 1).corr()

# Filtra apenas os dados onde o tipo é "state" (ou seja, nível de estado)
#estados = data.loc[data.place_type == 'state']

# Filtra apenas os dados do estado de Goiás (GO)
#estados_go = estados.loc[data.state == 'GO']

# Agrupa os dados por data e soma os casos confirmados por dia
# reset_index() reorganiza o índice para virar uma coluna normal
#estados_go_casos = estados_go.groupby('date').sum()['confirmed'].reset_index()

# Mostra as últimas linhas desse resultado
#estados_go_casos.tail()

# Prepara os dados para o modelo Prophet
# Prophet exige colunas chamadas 'ds' (data) e 'y' (valor)
#estados_go_casos_previsao = estados_go_casos
#estados_go_casos_previsao.columns = ['ds','y']

# Mostra as últimas linhas já no formato correto
#estados_go_casos_previsao.tail()

# Filtra apenas dados de cidades e depois somente Goiânia
#cidade_goiania_mortes = data.loc[data.place_type=='city'] \
#    .loc[data.city=='Goiânia'] \
#    .groupby('date').sum()['confirmed'].reset_index()

# Renomeia as colunas para o padrão do Prophet
#cidade_goiania_mortes.columns = ['ds','y']

# Cria o modelo de previsão usando Prophet
#modelProphet = ph.Prophet()

# Treina o modelo com os dados históricos
#modelProphet.fit(cidade_goiania_mortes)

# Cria um DataFrame com datas futuras (60 dias à frente)
#futuro = modelProphet.make_future_dataframe(60)

# Gera a previsão para essas datas futuras
#previsao = modelProphet.predict(futuro)

# Mostra as últimas 10 previsões
# yhat = valor previsto
# yhat_lower = limite inferior da previsão
# yhat_upper = limite superior da previsão
#previsao[['ds','yhat_lower','yhat','yhat_upper']].tail(10)


#Explicação simples:

#Você carrega dados de COVID de um arquivo CSV.
#Depois filtra primeiro por estado (GO) e depois por cidade (Goiânia).
#Organiza os dados agrupando por data.
#Prepara os dados no formato que o modelo Prophet exige.
#Cria e treina o modelo de previsão.
#Gera datas futuras (60 dias à frente).
#E por fim mostra os valores previstos junto com uma margem de erro.