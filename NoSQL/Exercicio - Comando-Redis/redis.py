import redis
import time
import base64

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# ALTO DESEMPENHO
start_time = time.time()
redis_client.set("chave_teste", "valor_teste")
retrieved_value = redis_client.get("chave_teste")
end_time = time.time()

print(f"Valor: {retrieved_value}")
print(f"Tempo: {end_time - start_time:.6f}s\n")

# ESCALABILIDADE
for i in range(1000):
    redis_client.set(f"chave_{i}", f"valor_{i}")

print(f"Exemplo: {redis_client.get('chave_500')}\n")

# FLEXIBILIDADE
redis_client.set("string_exemplo", "Hello Redis!")
print(f"String: {redis_client.get('string_exemplo')}")

redis_client.rpush("lista_exemplo", "item1", "item2", "item3")
print(f"Lista: {redis_client.lrange('lista_exemplo', 0, -1)}")

redis_client.hset("hash_exemplo", "campo1", "valor1")
redis_client.hset("hash_exemplo", "campo2", "valor2")
print(f"Hash: {redis_client.hgetall('hash_exemplo')}")

image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8")
redis_client.set("imagem_binario", image_data)
print(f"Base64: {redis_client.get('imagem_binario')[:20]}...\n")

# BAIXA LATÊNCIA
redis_client.set("configuracao_cache", "config_inicial")
for _ in range(5):
    start_time = time.time()
    cache_value = redis_client.get("configuracao_cache")
    end_time = time.time()
    print(f"Cache: {cache_value} | Tempo: {end_time - start_time:.6f}s")
