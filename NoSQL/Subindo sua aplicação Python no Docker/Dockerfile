# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY codigo.py /app

# Instala as dependências necessárias
RUN pip install flask

# Expõe a porta que a aplicação irá usar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "codigo.py"]