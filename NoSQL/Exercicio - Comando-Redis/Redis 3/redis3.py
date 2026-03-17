import redis
import base64
import os

# Conexão com o Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def salvar_imagem_no_redis(caminho_imagem, chave):
    with open(caminho_imagem, "rb") as imagem:
        imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
        redis_client.set(chave, imagem_base64)
        print(f"Imagem salva no Redis com a chave: {chave}")

def recuperar_imagem_do_redis(chave, caminho_saida):
    imagem_base64 = redis_client.get(chave)
    if imagem_base64:
        with open(caminho_saida, "wb") as imagem:
            imagem.write(base64.b64decode(imagem_base64))
            print(f"Imagem recuperada do Redis e salva em: {caminho_saida}")
    else:
        print("Chave não encontrada no Redis.")

# Caminho absoluto para o arquivo de imagem
caminho_imagem = os.path.join(os.path.dirname(__file__), "redis_imagem.png")
caminho_saida = os.path.join(os.path.dirname(__file__), "imagem_recuperada.png")

# Exemplo de uso
salvar_imagem_no_redis(caminho_imagem, "imagem_teste")
recuperar_imagem_do_redis("imagem_teste", caminho_saida)