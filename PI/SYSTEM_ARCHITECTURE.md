# Arquitetura Completa - Sistema de Detecção de Fadiga

## 1. Diagrama de Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                              │
├──────────────────────────┬──────────────────────┬──────────────────────┤
│   📱 APP MOBILE          │   🖥️ DASHBOARD       │   ⌚ SMARTWATCH      │
│  (Flutter/React Native) │  (React/Vue)         │   (ESP32 S3)         │
│  └─ UI Nativa           │  └─ Web UI           │   └─ Firmware C++    │
│  └─ BLE Client          │  └─ Charts           │   └─ Sensores        │
│  └─ Local DB (SQLite)   │  └─ Analytics       │   └─ Bluetooth GATT  │
└──────────────────────────┴──────────────────────┴──────────────────────┘
                                     ▲ Sincronização BLE / Http
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE LÓGICA / PROCESSAMENTO                     │
├──────────────────────────┬──────────────────────┬──────────────────────┤
│   🤖 IA LOCAL            │   🔄 API REST        │   🎯 PROCESSAMENTO   │
│  (Modelo Fadiga)         │  (Node/Flask)        │   (Alertas)          │
│  └─ Análise BPM          │  └─ CRUD User       │   └─ Validação      │
│  └─ Detecção Padrões    │  └─ Sync Manager    │   └─ Notificações   │
│  └─ Recomendações        │  └─ Auth JWT        │   └─ Transformação  │
│  └─ Classificação Risco  │  └─ Rate Limiter    │       de Dados       │
└──────────────────────────┴──────────────────────┴──────────────────────┘
                                     ▲ JSON / Binary Protocols
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE DADOS / PERSISTÊNCIA                       │
├──────────────────────────┬──────────────────────┬──────────────────────┤
│   ⚡ REDIS               │   🗄️ DATABASE        │   💾 LOCAL STORAGE   │
│  (Cache/Real-time)       │  (PostgreSQL/MySQL) │  (SQLite/IndexedDB) │
│  └─ Streams (histórico) │  └─ User profiles  │  └─ Readings buffer │
│  └─ Sorted Sets (rank)  │  └─ Medical data   │  └─ Config cache    │
│  └─ Hashes (métricas)   │  └─ Analytics      │  └─ Offline mode    │
│  └─ TTL (limpeza auto)  │  └─ Audit log      │  └─ Images cache    │
└──────────────────────────┴──────────────────────┴──────────────────────┘
                                     ▲ SQL / Protocols
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE INFRAESTRUTURA                             │
├──────────────────────────┬──────────────────────┬──────────────────────┤
│   ☁️ CLOUD               │   🔐 SECURITY        │   📊 MONITORAMENTO   │
│  (AWS/GCP/Azure)         │  (TLS/Encryption)    │  (Prometheus/ELK)    │
│  └─ Hosting             │  └─ API Keys        │  └─ Logs             │
│  └─ CDN                 │  └─ JWT/OAuth2      │  └─ Metrics          │
│  └─ Backup              │  └─ SSL Certs       │  └─ Alerts           │
│  └─ Escalabilidade      │  └─ Rate Limiting   │  └─ Dashboards       │
└──────────────────────────┴──────────────────────┴──────────────────────┘
```

## 2. Fluxo de Dados End-to-End

```
┌──────────────────────────────────────────────────────────────────────┐
│  SENSOR (MAX30102 no ESP32)                                          │
│  ├─ Lê BPM, SpO2, Temperatura a cada 1s                             │
│  └─ Processa localmente (estimativas)                               │
└────────────────┬─────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│  ANÁLISE LOCAL NO ESP32                                               │
│  ├─ Buffer de 60 amostras (1 minuto)                                 │
│  ├─ Cálculo de média e desvio padrão                                 │
│  └─ Classificação de risco (0-2)                                     │
└────────────────┬─────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  TRANSMISSÃO BLUETOOTH (JSON)                                          │
│  Example: {"bpm":75,"spo2":97,"temp":36.5,"fatigue":25,"risk":0}      │
│  Frequência: 1-2 Hz (a cada 1-2 segundos)                            │
└────────────────┬──────────────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌─────────────────┐  ┌──────────────────────────┐
│ APP MOBILE      │  │ DASHBOARD WEB            │
├─────────────────┤  ├──────────────────────────┤
│ • SQLite Local  │  │ • WebSocket real-time    │
│ • Análise IA    │  │ • Charts (Chart.js)      │
│ • Notificações  │  │ • Agregações             │
└────────┬────────┘  └────────┬─────────────────┘
         │                    │
         └────────────┬───────┘
                      ▼
              ┌──────────────────┐
              │  BACKEND API     │
              ├──────────────────┤
              │ • Validação      │
              │ • Rate Limiting  │
              │ • Transformação  │
              │ • Autenticação   │
              └────────┬─────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │ Redis  │  │Database │  │ S3/Cloud │
    │(Cache) │  │(Persist)│  │(Backup)  │
    └────────┘  └─────────┘  └──────────┘
         │             │             │
         └─────────────┼─────────────┘
                       ▼
              ┌──────────────────┐
              │  8. IA NO BACKEND│
              ├──────────────────┤
              │ • Análise profunda
              │ • Patterns        │
              │ • Previsões       │
              └──────────────────┘
```

## 3. Stack Tecnológico Completo

### Backend

```
├─ Runtime: Node.js / Python 3.11
│
├─ Framework Web:
│  ├─ Express.js / Fastify (Node)
│  └─ Flask / FastAPI (Python)
│
├─ Banco de Dados:
│  ├─ PostgreSQL (Dados estruturados)
│  ├─ Redis (Cache e time-series)
│  └─ MongoDB (Opcional - logs flexíveis)
│
├─ Autenticação:
│  ├─ JWT (JSON Web Tokens)
│  ├─ OAuth 2.0
│  └─ Refresh Tokens
│
├─ API REST:
│  ├─ OpenAPI/Swagger
│  ├─ CORS configurado
│  └─ Rate Limiting (Redis)
│
├─ WebSocket:
│  ├─ Socket.io / Ws
│  └─ Para real-time dashboard
│
├─ Task Queue:
│  ├─ Bull (Redis) / Celery (Python)
│  └─ Para processamento assíncrono
│
└─ Deployment:
   ├─ Docker
   ├─ Docker Compose
   ├─ Kubernetes (opcional)
   └─ CI/CD (GitHub Actions / GitLab CI)
```

### Mobile

```
├─ Framework: Flutter / React Native
│
├─ BLE Library:
│  ├─ flutter_blue_plus (Flutter)
│  └─ react-native-ble-plx (RN)
│
├─ Local Storage:
│  ├─ Sqflite (Flutter)
│  ├─ SQLite (React Native)
│  └─ SharedPreferences / AsyncStorage
│
├─ HTTP Client:
│  ├─ Dio / Http (Flutter)
│  └─ Axios / Fetch (RN)
│
├─ State Management:
│  ├─ Provider / Riverpod (Flutter)
│  └─ Redux / Zustand (RN)
│
├─ Notificações:
│  ├─ Firebase Cloud Messaging
│  └─ Local Notifications Plugin
│
└─ UI Framework:
   ├─ Material (Flutter)
   └─ React Native Paper / Native Base
```

### Dashboard / Frontend Web

```
├─ Framework: React.js / Vue.js
│
├─ State Management:
│  ├─ Redux / Zustand / Jotai (React)
│  └─ Vuex / Pinia (Vue)
│
├─ HTTP Client:
│  ├─ Axios / Fetch API
│
├─ Charting:
│  ├─ Chart.js / Recharts
│  ├─ D3.js (visualizações complexas)
│  └─ ECharts
│
├─ Real-time:
│  ├─ Socket.IO Client
│
├─ Styling:
│  ├─ Tailwind CSS
│  ├─ Material-UI
│  └─ Styled Components
│
├─ Build Tool:
│  ├─ Vite / Webpack
│  ├─ TypeScript
│
└─ Deployment:
   ├─ Netlify / Vercel
   └─ AWS S3 + CloudFront
```

## 4. Modelo de Dados

### Diagrama Entidade-Relacionamento (ER)

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ password_hash   │
│ name            │
│ age             │─────┐
│ weight          │     │ 1:N
│ height          │     │
│ created_at      │     │
└─────────────────┘     │
                        │
                        ▼
┌─────────────────┐  ┌──────────────────┐
│  DEVICES        │  │    READINGS      │
├─────────────────┤  ├──────────────────┤
│ id (PK)         │  │ id (PK)          │
│ user_id (FK)    │  │ device_id (FK)   │
│ device_uuid     │  │ user_id (FK)     │
│ name            │◀─┤ timestamp        │
│ mac_address     │  │ bpm              │
│ firmware_ver    │  │ spo2             │
│ battery_level   │  │ temperature      │
│ last_sync       │  │ fatigue_level    │
│ created_at      │  │ risk_level       │
└─────────────────┘  └──────────────────┘
                              │
                              │ 1:N
                              ▼
                     ┌──────────────────┐
                     │     ALERTS       │
                     ├──────────────────┤
                     │ id (PK)          │
                     │ reading_id (FK)  │
                     │ alert_type       │
                     │ severity         │
                     │ message          │
                     │ acknowledged     │
                     │ created_at       │
                     └──────────────────┘
```

## 5. Pipeline de Processamento de IA

```
Entrada: Leitura de Sensor
    │
    ▼
┌──────────────────────────────────────┐
│  1. EXTRAÇÃO DE FEATURES             │
├──────────────────────────────────────┤
│  • BPM (valor bruto)                  │
│  • HR Variability (desvio padrão)     │
│  • SpO2 (valor bruto)                 │
│  • Temperatura (valor bruto)          │
│  • Tendência (polyfit últimas 5 leit) │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│  2. NORMALIZAÇÃO (0-1)               │
├──────────────────────────────────────┤
│  • Z-score normalization              │
│  • Min-max scaling                    │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│  3. PONDERAÇÃO                       │
├──────────────────────────────────────┤
│  • BPM Deviation:    0.25             │
│  • SpO2 Reduction:   0.30             │
│  • Temp Elevation:   0.15             │
│  • HRV Reduction:    0.20             │
│  • Recent Trend:     0.10             │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│  4. CÁLCULO DE SCORE (0-100)         │
├──────────────────────────────────────┤
│  score = Σ(feature * weight)          │
│  clipped = min(100, max(0, score))    │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│  5. CLASSIFICAÇÃO                    │
├──────────────────────────────────────┤
│  • 0-30: Baixo Risco   (Verde)       │
│  • 31-65: Médio Risco  (Amarelo)     │
│  • 66-100: Alto Risco  (Vermelho)    │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│  6. GERAÇÃO DE ALERTAS               │
├──────────────────────────────────────┤
│  • Se score > 70: ALERTA urgente      │
│  • Se score > 50: Aviso               │
│  • Debounce: 5min entre alertas       │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│  7. INSIGHTS & RECOMENDAÇÕES         │
├──────────────────────────────────────┤
│  • Tendência: piorando/estável/melhora│
│  • Padrões: detectar horários com alta│
│    fadiga (ex: após almoço)           │
│  • Sugestões personalizadas           │
└──────────────────────────────────────┘
    │
    ▼
Saída: Análise de Fadiga com Classificação e Alertas
```

## 6. Fluxo de Autenticação

```
Usuário (Mobile/Web)
    │
    ├─ 1. POST /auth/register
    │      └─ Email, Password, Perfil
    ▼
┌──────────────────────────┐
│ Backend - Validação      │
├──────────────────────────┤
│ • Email válido?          │
│ • Password forte?        │
│ • User já existe?        │
└──────────────────────────┘
    │
    ├─ 2. Hash Password (bcrypt)
    │
    ├─ 3. Armazenar em Database
    │
    ├─ 4. Gerar JWT Token
    │      ├─ Header: {alg: HS256}
    │      ├─ Payload: {user_id, email, exp}
    │      └─ Signature: HMAC(header.payload, secret)
    │
    └─ Resposta: {access_token, refresh_token}

─────────────────────────────────────────────

Próximas Requisições:
    │
    └─ Header: Authorization: Bearer {access_token}
        │
        ▼
    ┌──────────────────────────┐
    │ Middleware - Verificação │
    ├──────────────────────────┤
    │ • Token válido?          │
    │ • Não expirou?           │
    │ • Assinatura correta?    │
    └──────────────────────────┘
        │
        ├─ ✓ Autorizado → Continuar
        └─ ✗ Falha → 401 Unauthorized
```

## 7. Estratégia de Scaling

```
Fase 1: MVP (Desenvolvimento)
├─ Single server (Heroku/Render)
├─ PostgreSQL local
├─ Redis local
└─ Max: ~100 usuários

Fase 2: Growth (~1k usuários)
├─ Load Balancer (Nginx)
├─ 2-3 App Servers (Node/Python)
├─ PostgreSQL (replicação read-only)
├─ Redis standalone
├─ CDN para assets estáticos
└─ CloudFront / Cloudflare

Fase 3: Scale (~10k usuários)
├─ Kubernetes cluster
├─ Auto-scaling (horizontal)
├─ PostgreSQL com sharding
├─ Redis Cluster
├─ Separate read/write databases
├─ Message Queue (RabbitMQ/Kafka)
├─ API Gateway
├─ Multi-CDN
└─ Geographic distribution (múltiplas regiões)
```

## 8. Segurança

```
┌─────────────────────────────────────┐
│      CAMADA DE SEGURANÇA            │
├─────────────────────────────────────┤
│                                     │
│ 1. TRANSPORTE                       │
│    └─ HTTPS/TLS 1.3 para tudo      │
│                                     │
│ 2. AUTENTICAÇÃO                     │
│    ├─ JWT compacto                 │
│    ├─ Refresh tokens com curta     │
│    │   validade                     │
│    └─ CORS restritivo              │
│                                     │
│ 3. AUTORIZAÇÃO                      │
│    ├─ Role-Based Access Control     │
│    │  (user, doctor, admin)         │
│    └─ Scope validation              │
│                                     │
│ 4. DADOS SENSÍVEIS                  │
│    ├─ Encryption at rest (AES-256) │
│    ├─ Hashing passwords (bcrypt)   │
│    └─ Masked logs (sem dados médicos
│                                     │
│ 5. REDE                             │
│    ├─ Rate limiting                │
│    ├─ DDoS protection (Cloudflare) │
│    ├─ WAF rules                    │
│    └─ IP whitelisting (admin)      │
│                                     │
│ 6. AUDITORIA                        │
│    ├─ Logging de todas operações   │
│    ├─ Audit trail                  │
│    ├─ GDPR compliance              │
│    └─ Data retention policy        │
│                                     │
└─────────────────────────────────────┘
```

## 9. Plano de Rollout

### Fase 1: Alpha (Semana 1-2)
- Testes com 10 beta testers internos
- ESP32 + MAX30102 hardware testado
- Backend MVP rodando
- Mobile em Flutter com BLE básico

### Fase 2: Beta (Semana 3-4)
- 100 beta testers externos
- Testes de stress em backend
- Refinamento de UI/UX
- Calibração de limiares de fadiga

### Fase 3: Launch (Semana 5+)
- App Store & Google Play release
- Marketing push
- Monitoring contínuo de erros
- Suporte ao usuário

## 10. Monitoramento em Produção

```
Métricas Críticas:
├─ API Response Time (< 200ms em p95)
├─ Error Rate (< 0.5%)
├─ BLE Connection Success Rate (> 95%)
├─ Redis Hit Rate (> 80%)
├─ Database Query Performance
└─ User Engagement (DAU, MAU)

Alertas Automáticos:
├─ Response time > 500ms
├─ Error rate > 5%
├─ Database CPU > 80%
├─ Redis Memory > 90%
├─ WebSocket disconnections > 10%
└─ Payment failures > 1%

Dashboards:
├─ Real-time app health
├─ User activity timeline
├─ Revenue tracking
├─ Performance trends
└─ Error tracking (Sentry)
```

