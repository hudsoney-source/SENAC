# Perguntas e Respostas - Introdução aos Bancos de Dados Não-Relacionais
#
# 1. DEFINIÇÃO E CARACTERÍSTICAS
#
# a) O que caracteriza um banco de dados não-relacional?
#
# Banco de dados não-relacional é um banco que não usa tabelas com linhas e colunas
# como o SQL tradicional. Ele permite guardar dados de jeitos diferentes, sem precisar
# ter uma estrutura fixa. Pode guardar tudo em forma de documentos, pares de chave-valor,
# ou em grafos. É mais flexível do que o banco relacional.
#
#
# b) Quais são as vantagens desse tipo de banco em relação aos bancos relacionais?
#
# - Pode crescer mais facilmente (adicionar mais servidores sem problema)
# - Estrutura flexível (não precisa definir tudo antes)
# - Mais rápido para guarddar muitos dados
# - Funciona bem com dados que mudam de formato
# - Custa menos para infraestrutura na maioria das vezes
# - Facilita guardar dados relacionados entre si
#
#
# c) Cite ao menos 3 situações práticas em que um banco de dados não-relacional 
# é mais indicado:
#
# 1. Redes sociais (Instagram, Facebook) - guardar perfis e conexões
# 2. Apps de IoT - dados de sensores que mudam
# 3. E-commerce - produtos com características diferentes
# 4. Chat em tempo real
# 5. Armazenar cache para ficar mais rápido
#
#
# 2. TIPOS DE BANCOS DE DADOS NÃO-RELACIONAIS
#
# a) Explique as diferenças entre os quatro principais tipos:
#
# - Orientados a documentos: guarda dados como documentos (JSON), tipo MongoDB
# - Chave-valor: guarda partes de informação ligadas a uma chave simples, tipo Redis
# - Colunas amplas: organiza dados em colunas em vez de linhas, tipo Cassandra
# - Grafos: usa nós e conexões entre eles, tipo Neo4j
#
#
# b) Exemplos de ferramentas:
#
# Documentos: MongoDB, CouchDB, Firebase
# Chave-valor: Redis, Memcached, DynamoDB
# Colunas: HBase, Cassandra, Bigtable
# Grafos: Neo4j, ArangoDB
#
# 3. COMPARAÇÃO PRÁTICA
#
# a) Qual a principal diferença entre modelo relacional e modelo de grafos?
#
# Relacional: usa tabelas com linhas e colunas tipo Excel. Quando precisa conectar
# informações usa joins que podem ser lentos
#
# Grafos: usa nós (pontos) e conexões entre eles. É mais rápido para buscar
# relacionamentos complexos, tipo amigos de amigos
#
# b) Em redes sociais, qual tipo seria mais adequado?
#
# Grafos. Porque redes sociais é pessoas (nós) conectadas a outras pessoas (arestas).
# Com grafos fica mais rápido buscar amigos de amigos. Facebook, Instagram, Twitter usam.
#
# 4. ESCALABILIDADE E FLEXIBILIDADE
#
# a) Como a escalabilidade horizontal funciona?
#
# Escalabilidade horizontal é quando você adiciona mais servidores conforme precisa.
# Os dados são divididos entre os servidores, cada um fica com uma parte diferente.
# Também cada servidor pode ter cópias dos dados em outros servidores, então se um
# cair, o outro continua funcionando. Muitas empresas fazem isso
#
# b) Por que a flexibilidade de schema é importante em bancos orientados a documentos?
#
# No SQL tradicional, se você quer adicionar um campo novo, tem que parar o banco,
# fazer uma alteração (ALTER TABLE) e isso pode ser lento. No MongoDB (documentos),
# você simplesmente coloca o campo novo no próximo documento que inserir. Não precisa
# alterar nada. Outros documentos antigos continuam sem esse campo e tudo funciona.
# Isso facilita bastante quando o sistema está mudando
#
#
# 5. ESTUDO DE CASO
#
# a) Empresa que usa banco não-relacional:
#
# Netflix usa Cassandra (banco de colunas)
#
# b) Como é utilizado e benefícios:
#
# A Netflix tem 250 milhões de usuários do lado do mundo. Cada um assiste
# filmes, pausa, continua assistindo depois. Isso gera bilhões de eventos por dia.
# Com Cassandra, eles conseguem guardar todos esses eventos de forma rápida
# e distribuída em múltiplos servidores.
#
# Benefícios:
# - Consegue escalabilidade extrema (muitos servidores, muitos dados)
# - Alta disponibilidade (se um servidor cai, não afeta os usuários)
# - Performance muito rápida
# - Funciona bem com dados distribuídos em várias regiões