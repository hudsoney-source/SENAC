# Estrutura de Dados Redis - Sistema de Detecção de Fadiga

## 1. Schemas e Estruturas de Dados

### 1.1 Stream Redis - Histórico de Sensores

```redis
# Armazenar leitura de sensores em tempo real
XADD biometric_data:* "*" \
  bpm 75 \
  spo2 97 \
  temperature 36.5 \
  fatigue_level 25 \
  risk_level 0 \
  user_id "user123" \
  device_id "esp32_001"

# Exemplo de chave criada:
# biometric_data:user123:1713279600000-0
#   {bpm: 75, spo2: 97, temperature: 36.5, ...}

# Retenção: 7 dias de histórico
# Espaço: ~1KB por leitura × 86400 leituras/dia × 7 dias = ~600MB
```

### 1.2 Hash - Últimas Médias (10 minutos)

```redis
# Guardar médias das últimas leituras
HSET user123:metrics:recent \
  avg_bpm 72 \
  avg_spo2 96 \
  avg_temp 36.4 \
  bpm_variance 8.5 \
  spo2_variance 1.2 \
  sample_count 60 \
  last_update 1713279600

# Expirar após 15 minutos
EXPIRE user123:metrics:recent 900
```

### 1.3 Sorted Set - Alertas com Timestamp

```redis
# Manter registro de eventos de risco
ZADD user123:alerts \
  1713279600 "high_fatigue_detected" \
  1713279360 "oxygen_dip_detected" \
  1713279120 "abnormal_heartrate"

# Score = unix_timestamp, Member = descrição do alerta
# Manter últimos 30 dias
EXPIRE user123:alerts 2592000

# Recuperar alertas das últimas 24h
ZRANGEBYSCORE user123:alerts \
  1713193200 1713279600 \
  WITHSCORES
```

### 1.4 Hash - Perfil de Usuário

```redis
HSET user123:profile \
  name "João Silva" \
  age 35 \
  height 180 \
  weight 75 \
  gender "M" \
  device_id "esp32_001" \
  timezone "America/Sao_Paulo" \
  created_at 1712000000 \
  last_sync 1713279600 \
  notification_enabled true \
  threshold_bpm_high 120 \
  threshold_bpm_low 50 \
  threshold_spo2_low 92

# Sem expiração (dados permanentes)
```

### 1.5 Set - Dispositivos Ativos

```redis
# Registrar dispositivos conectados
SADD active_devices "esp32_001" "esp32_002" "esp32_003"

# Remover quando offline
SREM active_devices "esp32_001"

# Verificar se dispositivo está online
SISMEMBER active_devices "esp32_001"

# Expirar automaticamente após 5 minutos de inatividade
EXPIRE esp32_001:online_ttl 300
```

### 1.6 Double Sorted Set - Análise de Fadiga Diária

```redis
# Guardar índice de fadiga diário
ZADD user123:fatigue_daily \
  1713193200 30 \
  1713279600 45 \
  1713366000 35

# Score = date (unix_timestamp de meia-noite), Member = avg_fatigue_level
# Retenção: 90 dias
EXPIRE user123:fatigue_daily 7776000
```

### 1.7 List - Logs de Sincronização

```redis
# Manter registro de sincronizações
RPUSH user123:sync_log \
  "{\"timestamp\":1713279600,\"records\":600,\"status\":\"success\"}" \
  "{\"timestamp\":1713276000,\"records\":600,\"status\":\"success\"}" \
  "{\"timestamp\":1713272400,\"records\":580,\"status\":\"partial\"}"

# Manter últimos 100 eventos
LTRIM user123:sync_log 0 99

# Expirar após 30 dias
EXPIRE user123:sync_log 2592000
```

## 2. Estrutura de Chaves Recomendada

```
# Convenção: {entidade}:{sublevel}:{tipo}:{identifier}

# Exemplo de espaço de chaves para um usuário:
user123:profile                    # Hash - dados do usuário
user123:metrics:recent             # Hash - métricas recentes
user123:metrics:daily:2024-04-16   # Hash - métricas do dia
user123:fatigue_daily              # Sorted Set - histórico fadiga diária
user123:alerts                     # Sorted Set - alertas com timestamp
user123:sync_log                   # List - log de sincronizações
user123:device:esp32_001           # Hash - info do device
user123:readings:esp32_001         # Stream - leituras do device

# Índices para busca rápida:
devices:active                     # Set - devices conectados
devices:offline                    # Set - devices offline
users:online                       # Set - usuários com devices ativos
```

## 3. Operações Redis Principais

### 3.1 Registrar Nova Leitura

```python
import redis
import json
from datetime import datetime, timedelta

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def store_biometric_reading(user_id, device_id, bpm, spo2, temperature, fatigue_level, risk_level):
    """Armazenar nova leitura de sensor"""
    
    timestamp = int(datetime.now().timestamp())
    
    # 1. Adicionar ao stream (histórico completo)
    stream_key = f"biometric_data:{user_id}"
    r.xadd(stream_key, {
        'device_id': device_id,
        'bpm': bpm,
        'spo2': spo2,
        'temperature': temperature,
        'fatigue_level': fatigue_level,
        'risk_level': risk_level,
        'timestamp': timestamp
    })
    
    # 2. Atualizar hash de recentes
    recent_key = f"{user_id}:metrics:recent"
    current = r.hgetall(recent_key)
    
    new_avg_bpm = (int(current.get('avg_bpm', bpm)) * (int(current.get('sample_count', 1)) - 1) + bpm) / int(current.get('sample_count', 1))
    
    r.hset(recent_key, mapping={
        'last_bpm': bpm,
        'avg_bpm': int(new_avg_bpm),
        'last_spo2': spo2,
        'last_temperature': temperature,
        'last_fatigue': fatigue_level,
        'risk_level': risk_level,
        'last_update': timestamp,
        'sample_count': int(current.get('sample_count', 0)) + 1
    })
    r.expire(recent_key, 900)  # 15 minutos
    
    # 3. Registrar alerta se necessário
    if risk_level > 0:
        alert_key = f"{user_id}:alerts"
        alert_msg = f"Risk level {risk_level} - BPM:{bpm} SpO2:{spo2}"
        r.zadd(alert_key, {alert_msg: timestamp})
        r.expire(alert_key, 2592000)  # 30 dias
    
    # 4. Atualizar device online
    r.sadd('active_devices', device_id)
    device_ttl_key = f"{device_id}:online_ttl"
    r.setex(device_ttl_key, 300, '1')
```

### 3.2 Recuperar Dados Históricos

```python
def get_user_history(user_id, hours=24):
    """Recuperar histórico de um usuário"""
    
    stream_key = f"biometric_data:{user_id}"
    
    # Recuperar todas as entradas do stream nos últimas N horas
    since = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
    
    readings = r.xrange(stream_key, min=f"({since}", count=1000)
    
    return [{
        'id': entry[0],
        'data': entry[1]
    } for entry in readings]

def get_daily_stats(user_id, date):
    """Obter estatísticas de um dia específico"""
    
    daily_key = f"{user_id}:metrics:daily:{date}"
    stats = r.hgetall(daily_key)
    
    return {
        'avg_bpm': int(stats.get('avg_bpm', 0)),
        'peak_bpm': int(stats.get('peak_bpm', 0)),
        'min_bpm': int(stats.get('min_bpm', 0)),
        'avg_spo2': float(stats.get('avg_spo2', 0)),
        'avg_temperature': float(stats.get('avg_temperature', 0)),
        'avg_fatigue': int(stats.get('avg_fatigue', 0)),
        'total_readings': int(stats.get('total_readings', 0))
    }
```

### 3.3 Recalcular Agregações Diárias

```python
from croniter import croniter  # pip install croniter

def calculate_daily_aggregates(user_id, date):
    """Executar agregação diária (rodar às 23:59)"""
    
    stream_key = f"biometric_data:{user_id}"
    
    # Buscar todos os dados do dia
    start_ts = int(datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000)
    end_ts = int((datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).timestamp() * 1000)
    
    readings = r.xrange(stream_key, min=start_ts, max=end_ts)
    
    if not readings:
        return
    
    # Calcular estatísticas
    bpms = [int(entry[1]['bpm']) for entry in readings if entry[1]['bpm']]
    spo2s = [int(entry[1]['spo2']) for entry in readings if entry[1]['spo2']]
    temps = [float(entry[1]['temperature']) for entry in readings]
    fatigues = [int(entry[1]['fatigue_level']) for entry in readings]
    
    stats = {
        'avg_bpm': sum(bpms) // len(bpms) if bpms else 0,
        'peak_bpm': max(bpms) if bpms else 0,
        'min_bpm': min(bpms) if bpms else 0,
        'avg_spo2': sum(spo2s) // len(spo2s) if spo2s else 0,
        'avg_temperature': sum(temps) / len(temps) if temps else 0,
        'avg_fatigue': sum(fatigues) // len(fatigues) if fatigues else 0,
        'total_readings': len(readings),
        'date': date
    }
    
    # Salvar agregação
    daily_key = f"{user_id}:metrics:daily:{date}"
    r.hset(daily_key, mapping=stats)
    r.expire(daily_key, 7776000)  # 90 dias
    
    # Adicionar ao sorted set também
    fatigue_key = f"{user_id}:fatigue_daily"
    timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())
    r.zadd(fatigue_key, {timestamp: stats['avg_fatigue']})
```

### 3.4 Sistema de Alertas

```python
def check_alert_conditions(user_id, bpm, spo2, fatigue_level, risk_level):
    """Verificar e registrar condições de alerta"""
    
    alerts = []
    profile_key = f"{user_id}:profile"
    profile = r.hgetall(profile_key)
    
    # Verificar limites personalizados
    threshold_bpm_high = int(profile.get('threshold_bpm_high', 120))
    threshold_bpm_low = int(profile.get('threshold_bpm_low', 50))
    threshold_spo2_low = int(profile.get('threshold_spo2_low', 92))
    
    if bpm > threshold_bpm_high:
        alerts.append("HIGH_HEART_RATE")
    
    if bpm < threshold_bpm_low:
        alerts.append("LOW_HEART_RATE")
    
    if spo2 < threshold_spo2_low:
        alerts.append("LOW_OXYGEN")
    
    if fatigue_level > 75:
        alerts.append("SEVERE_FATIGUE")
    
    # Salvar alertas
    for alert in alerts:
        timestamp = int(datetime.now().timestamp())
        alert_key = f"{user_id}:alerts:{alert}"
        
        r.lpush(alert_key, f"{timestamp}")
        r.ltrim(alert_key, 0, 99)  # Manter últimos 100
        r.expire(alert_key, 2592000)  # 30 dias
    
    return alerts
```

### 3.5 Sincronização com ESP32

```python
def prepare_sync_package(user_id, device_id):
    """Preparar dados para sincronizar com ESP32"""
    
    recent_key = f"{user_id}:metrics:recent"
    profile_key = f"{user_id}:profile"
    
    recent_metrics = r.hgetall(recent_key)
    profile = r.hgetall(profile_key)
    
    sync_data = {
        'timestamp': int(datetime.now().timestamp()),
        'user_config': {
            'threshold_bpm_high': profile.get('threshold_bpm_high'),
            'threshold_bpm_low': profile.get('threshold_bpm_low'),
            'threshold_spo2_low': profile.get('threshold_spo2_low'),
        },
        'recent_metrics': recent_metrics,
        'status': 'sync_ready'
    }
    
    # Saurar como JSON
    sync_key = f"{device_id}:sync_data"
    r.set(sync_key, json.dumps(sync_data))
    r.expire(sync_key, 3600)  # 1 hora
    
    return sync_data
```

## 4. Política de Retenção de Dados

| Tipo de Dados         | TTL (Time To Live) | Razão                      |
|-------------------|--------------|-----------------------|
| Stream (Histórico)| 7 dias       | Backup local para sync        |
| Métricas Recentes | 15 minutos   | Apenas para referência rápida |
| Alertas           | 30 dias      | Auditoria e histórico        |
| Perfil Usuário    | Sem limite   | Dados permanentes           |
| Sincronização Log | 30 dias      | Debug e troubleshooting     |
| Métricas Diárias  | 90 dias      | Análise histórica           |
| Devices Ativos    | 5 minutos    | Heartbeat de conexão        |

## 5. Índices e Performance

```redis
# Para aplicações com Bloom filters (detecção duplicados)
BF.ADD fatigue_readings_bloom user123_2024_04_16_001

# Para busca por intervalo de tempo otimizada:
# Usar XRAD com índice de timestamp
XREAD COUNT 100 STREAMS biometric_data:user123 0

# Análise de performance
INFO stats
INFO memory
MONITOR  # Ver todos os comandos
```

## 6. Backup e Recuperação

```bash
# BackUp manual
redis-cli --rdb /backup/dump_$(date +%Y%m%d).rdb

# Restaurar
redis-cli SHUTDOWN
cp /backup/dump_YYYYMMDD.rdb /var/lib/redis/dump.rdb
redis-server

# AOF (Append-Only File) para maior durabilidade
CONFIG SET appendonly yes
```

## 7. Monitoramento Redis

```python
def redis_health_check():
    """Verificar saúde do Redis"""
    
    try:
        info = r.info()
        
        health = {
            'connected': True,
            'memory_used_mb': info['used_memory'] / (1024**2),
            'memory_limit_mb': info.get('maxmemory', 'unlimited'),
            'connected_clients': info['connected_clients'],
            'total_operations': info['total_commands_processed'],
            'evictions': info.get('evicted_keys', 0),
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0)
        }
        
        hit_rate = health['keyspace_hits'] / (health['keyspace_hits'] + health['keyspace_misses'] + 1)
        health['hit_rate'] = f"{hit_rate*100:.1f}%"
        
        return health
    except Exception as e:
        return {'connected': False, 'error': str(e)}
```

