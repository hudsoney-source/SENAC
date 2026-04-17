# QUICK START - Sistema de Detecção de Fadiga

## ⚡ Início Rápido (5 minutos)

### Pré-requisitos
- Arduino IDE instalada
- ESP32 S3 DevKit conectado via USB
- Python 3.11+
- Docker & Docker Compose (opcional)

---

## 🔧 Passo 1: Upload do Firmware ESP32 (5 min)

### 1.1 Instalar Board Support

```
Arduino IDE → Arquivo → Preferências
URL Adicionais: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
OK
Ferramentas → Placa → Boards Manager
Buscar: "esp32"
Instalar: "esp32 by Espressif Systems" (versão 2.0+)
```

### 1.2 Instalar Biblioteca MAX30102

```
Sketch → Include Library → Manage Libraries
Buscar: "MAX30102"
Instalar: "MAX30102 by Sparkfun"
```

### 1.3 Upload do Código

```
1. Abrir: smartwatch_fadiga.ino
2. Ferramentas → Placa → ESP32-S3-DevKitC-1
3. Ferramentas → Port → COM X (seu ESP32)
4. Ctrl+U para fazer upload
5. Aguardar: "Compiled Successfully"
```

### 1.4 Verificar Funcionamento

```
Ferramentas → Monitor Serial → 115200
# Esperado:
[INIT] Inicializando MAX30102...
[OK] MAX30102 calibrado!
[OK] Bluetooth iniciado!
[OK] Sistema pronto!
```

**✓ Hardware pronto!**

---

## 🚀 Passo 2: Iniciar Backend (3 min)

### 2.1 Usando Docker (Recomendado)

```bash
# Na raiz do projeto
docker-compose up -d

# Verificar status
docker ps
```

**Serviços iniciados automaticamente:**
- Backend API: http://localhost:3000
- Redis: localhost:6379
- PostgreSQL: localhost:5432
- pgAdmin: http://localhost:5050
- Redis Commander: http://localhost:8081

### 2.2 Sem Docker (Manual)

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: PostgreSQL (deve estar rodando)
# (Configurar manualmente conforme seu OS)

# Terminal 3: Backend
cd backend
npm install
npm start
```

**Teste rápido:**
```bash
curl http://localhost:3000/health
# Esperado: {"status":"OK","timestamp":"2024-04-16T..."}
```

**✓ Backend pronto!**

---

## 📱 Passo 3: Testar Conexão Bluetooth (2 min)

### Teste Manual com Smartphone

#### Android / iOS
```
1. Abrir Configurações → Bluetooth
2. Buscar: "SmartWatch_Fadiga"
3. Conectar (nenhuma senha necessária na primeira vez)
4. Abrir app de terminal (ex: Termux no Android)
5. Conectar via APP em desenvolvimento

Esperado em Serial Monitor:
[BLE TX] {"bpm":72,"spo2":98,"temp":36.5,"fatigue":15,"risk":0,"ts":1234567}
```

#### Teste com Python (no PC)

```python
# test_ble.py
import asyncio
from bleak import BleakClient, BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        if "SmartWatch" in device.name:
            print(f"Encontrado: {device.name} ({device.address})")

asyncio.run(scan())
```

**✓ Bluetooth pronto!**

---

## 🤖 Passo 4: Testar IA (1 min)

```bash
cd PI
python fatigue_ai.py

# Esperado:
========================================
SISTEMA DE DETECÇÃO DE FADIGA - IA
========================================

📊 Gerando dados de teste...

========================================
RELATÓRIO DE FADIGA
========================================

📈 Pontuação de Fadiga: 35.4/100

🎯 Classificação: RISCO MODERADO
   Recomendação: ⚠ Fadiga moderada detectada...

❤️ Frequência Cardíaca Média: 85 BPM
...
```

**✓ IA pronto!**

---

## 📊 Passo 5: Acessar Dashboard

### Iniciar Frontend

```bash
cd web-dashboard
npm install
npm run dev

# Acesso: http://localhost:5173
```

### Login Padrão (teste)

```
Email: test@smartwatch.com
Senha: SmartWatch123!
```

**✓ Dashboard pronto!**

---

## 📱 Passo 6: Compilar App Mobile

### Flutter (Recomendado)

```bash
cd mobile
flutter pub get
flutter run -d android   # para Android
flutter run -d ios       # para iOS
```

### React Native

```bash
cd mobile-rn
npm install
npx react-native run-android
```

**✓ App Mobile pronto!**

---

## 🔄 Fluxo Completo de Teste

```
ESP32 (Hardware)
    ↓ Lê BPM/SpO2/Temp a cada 1s
    ↓ Bluetooth JSON
    ↓
App Mobile
    ↓ Recebe dados (1-2Hz)
    ↓ SQLite local
    ↓ IA local
    ↓ API POST /readings
    ↓
Backend
    ↓ Redis + PostgreSQL
    ↓ WebSocket update
    ↓
Dashboard
    ↓ Gráficos em tempo real ✓
```

---

## 🧪 Comandos Úteis

### Verificar Conectividade

```bash
# Backend API
curl http://localhost:3000/health

# Redis
redis-cli ping
# Esperado: PONG

# PostgreSQL
psql -U smartwatch_user -d fatigue_db -c "SELECT 1;"
```

### Ver Dados em Tempo Real

```bash
# Redis Stream
redis-cli XREAD STREAMS biometric_data:user1 0

# Logs Backend
docker logs -f smartwatch-backend

# Monitor Redis
redis-cli MONITOR
```

### Limpar Dados de Teste

```bash
# Remover DB local
rm -rf data/sqlite.db

# Limpar Redis
redis-cli FLUSHALL

# Recriar tables PostgreSQL
docker exec smartwatch-postgres psql -U smartwatch_user -d fatigue_db -f /docker-entrypoint-initdb.d/init.sql
```

---

## ⚠️ Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| "Device not found" | Verificar USB, reiniciar Arduino IDE |
| "Firmware upload failed" | Apertar BOOT no ESP32 durante upload |
| "Conexão Redis recusada" | `redis-server` não está rodando |
| "BD locked" | `sudo lsof /dev/ttyUSB0` e matar processo |
| "BLE fraco" | Afastar de Wi-Fi, aproximar do ESP32 |
| "App não conecta" | Verificar UUID do serviço GATT |

---

## 📚 Próximos Passos

1. **Calibração**: Rodar testes com dados reais para calibrar limiares
2. **Deployment**: Fazer deploy staging antes de produção
3. **Mobile Release**: Submeter apps às lojas (App Store, Play Store)
4. **Analytics**: Configurar Sentry/DataDog para monitoramento
5. **Documentação**: Criar guias de usuário e API docs

---

## 📞 Suporte Rápido

- **Issue no Hardware?** → Ver [HARDWARE_CONNECTIONS.md](HARDWARE_CONNECTIONS.md)
- **Dúvida na IA?** → Ver comentários em [fatigue_ai.py](fatigue_ai.py)
- **API Documentation?** → Ver [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)
- **Deploy em Produção?** → Ver [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)

---

**Status**: ✓ Sistema operacional e pronto para uso!

**Tempo Total**: ~15 minutos do zero ao funcionando

**Próxima**: Customize os thresholds de fadiga conforme necessário

