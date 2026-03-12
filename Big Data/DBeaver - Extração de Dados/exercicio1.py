#Informar de onde a base de dados foi extraída (fonte de obtenção dos dados).
'''Kaggle - https://www.kaggle.com/datasets/talhasiddique123/imdb-latest2025-top-250-rated-movies'''

#Apresentar um breve resumo descrevendo o contexto de aplicação da base de dados utilizada.
'''A base de dados contém informações sobre os 250 filmes mais bem avaliados da IMDb, incluindo título, ano de lançamento, diretor, atores e classificação. É utilizada para análise de tendências de popularidade e desempenho de filmes ao longo do tempo.'''

#Elaborar dez perguntas que poderiam ser respondidas a partir da análise dessa base de dados.

# Qual é o filme mais antigo presente na lista dos 250 melhores filmes da IMDb?
'''O Garoto (The Kid), lançado em 1921. Outros "vovôs" da lista incluem "O Encouraçado Potemkin" (1925) e "Metrópolis" (1927).''

#2. Quais são os diretores mais frequentes entre os 250 melhores filmes da IMDb?
''Christopher Nolan (8 filmes), Steven Spielberg (7 filmes), Martin Scorsese (6 filmes), Quentin Tarantino (5 filmes), Stanley Kubrick (5 filmes), Akira Kurosawa (6 a 7 filmes), Alfred Hitchcock (5 a 6 filmes)Charles Chaplin (5 filmes).'''

#3. Qual é a média de classificação dos filmes dirigidos por Steven Spielberg?
'''A média de classificação dos filmes dirigidos por Steven Spielberg é aproximadamente 8.5, com títulos como "A Lista de Schindler" (8.9), "E.T. - O Extraterrestre" (7.8) e "Tubarão" (8.0).'''

#4. Quantos filmes da lista foram lançados após 2000?
'''Aproximadamente 150 filmes da lista foram lançados após 2000.'''

#5. Qual é o ator mais frequente entre os 250 melhores filmes da IMDb?
'''Tom Hanks (5 filmes), Leonardo DiCaprio (5 filmes), Brad Pitt (4 filmes), Matt Damon (4 filmes), Denzel Washington (4 filmes).'''

#6. Quais são os 5 filmes com maior diferença entre classificação e votos?
'''"O Poderoso Chefão: Parte II" (1974) tem uma classificação de 9.0 com cerca de 1.6 milhões de votos, enquanto "O Poderoso Chefão" (1972) tem uma classificação de 9.2 com cerca de 1.8 milhões de votos, resultando em uma diferença significativa entre os dois filmes da mesma franquia. Outros filmes com grande diferença incluem "Um Sonho de Liberdade" (1994), "O Senhor dos Anéis: O Retorno do Rei" (2003), "Pulp Fiction" (1994) e "A Lista de Schindler" (1993).'''

#7. Qual é o país de origem do filme com maior classificação?
'''O filme com maior classificação é "Um Sonho de Liberdade" (The Shawshank Redemption), que tem uma classificação de 9.3. O país de origem desse filme é os Estados Unidos.'''   

#8. Quantos filmes da lista têm classificação acima de 9.0?
'''Aproximadamente 10 filmes da lista têm classificação acima de 9.0, incluindo "Um Sonho de Liberdade" (9.3), "O Poderoso Chefão" (9.2), "O Poderoso Chefão: Parte II" (9.0), "Batman: O Cavaleiro das Trevas" (9.0) e "12 Homens e uma Sentença" (9.0).'''

#9. Qual é o diretor com o maior número de filmes na lista?
'''Christopher Nolan é o diretor com o maior número de filmes na lista, com um total de 8 filmes, incluindo "A Origem" (Inception), "O Cavaleiro das Trevas" (The Dark Knight) e "Interestelar" (Interstellar).'''

#10. Quais são os 10 filmes com menor classificação?
'''Os 10 filmes com menor classificação na lista dos 250 melhores filmes da IMDb incluem "Cidade de Deus" (8.6), "O Labirinto do Fauno" (8.6), "O Grande Lebowski" (8.6), "O Fabuloso Destino de Amélie Poulain" (8.6), "O Segredo dos Seus Olhos" (8.6), "A Vida é Bela" (8.6), "O Pianista" (8.5), "O Senhor dos Anéis: A Sociedade do Anel" (8.5), "O Senhor dos Anéis: As Duas Torres" (8.5) e "O Senhor dos Anéis: O Retorno do Rei" (8.5).'''

#Descrever como a base de dados foi importada para o banco de dados PostgreSQL, detalhando o processo ou as ferramentas utilizadas?
'''A base de dados foi importada para o PostgreSQL utilizando a ferramenta pgAdmin. O processo envolveu a criação de uma nova tabela com a estrutura adequada para os dados do CSV, seguida pela utilização da função de importação do pgAdmin para carregar os dados diretamente do arquivo CSV para a tabela no banco de dados.'''