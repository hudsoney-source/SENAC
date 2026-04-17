# Especificação de Aplicativo Mobile - Sistema de Detecção de Fadiga

## 1. Visão Geral

Aplicativo mobile para iOS e Android que sincroniza dados de biometry do smartwatch ESP32 via Bluetooth, apresenta análise de fadiga em tempo real e fornece alertas personalizados.

## 2. Arquitetura do App

```
┌─────────────────────────────────────────────┐
│         CAMADA DE UI (Flutter/React Native) │
├─────────────────────────────────────────────┤
│ Home | Health | Analytics | Settings |     │
├─────────────────────────────────────────────┤
│      CAMADA DE NEGÓCIO (BLoC/Redux)         │
├─────────────────────────────────────────────┤
│   Gerenciador de Estado & Lógica            │
├─────────────────────────────────────────────┤
│      CAMADA DE DADOS (Repositories)         │
├─────────────────────────────────────────────┤
│  Bluetooth │ Redis │ Local Storage │ API   │
├─────────────────────────────────────────────┤
│       SERVIÇOS EXTERNOS (Backend)           │
└─────────────────────────────────────────────┘
```

## 3. Fluxo de Comunicação Bluetooth

```
        ESP32 SmartWatch           Mobile App
        ──────────────           ──────────────

1. Descoberta:
   Broadcast GATT ────────────→ Scan para "SmartWatch_Fadiga"
                                   ↓
                              Localiza dispositivo

2. Conexão:
                         ← Solicita pareamento
   Confirma pareamento ──→
                                   ↓
                              Conectado

3. Sincronização:
   Stream de dados
   {"bpm":75,...} ────────┐
   {"bpm":74,...} ────────┼──→ Buffer local (SQLite)
   {"bpm":76,...} ────────┘    ↓
                            Processamento IA
                            ↓
                            Atualizar UI

4. Desconexão automática:
   Se inativo > 5min ─→ Desconectar (Economy Mode)
   Reconectar ao movimento detectado
```

## 4. Telas Principais

### 4.1 Tela de Acasalamento (Onboarding)

```
┌─────────────────────────────────┐
│  🔍 Procurando SmartWatch...    │
│                                 │
│  Ativando Bluetooth             │
│  [████████░] 80%                │
│                                 │
│  Dispositivos encontrados:      │
│  ☐ SmartWatch_Fadiga [⚡ RSSI]  │
│    ├─ MacAddress: xx:xx:xx...  │
│    └─ Distância: ~2m            │
│                                 │
│  ☐ Outro dispositivo            │
│                                 │
│  [Selecionar] [Escanear Novamente]
└─────────────────────────────────┘
```

**Fluxo**:
1. Solicitar permissão de Bluetooth
2. Escanear 10 segundos
3. Filtrar por UUID do serviço GATT
4. User seleciona device
5. Conectar e sincronizar profile

### 4.2 Tela Inicial (Home/Dashboard)

```
┌─────────────────────────────────────────────┐
│ ⏰ 14:30:45                          ⚙️ Menu  │
├─────────────────────────────────────────────┤
│                                             │
│  Status de Fadiga                           │
│  ┌─────────────────────────────────────┐   │
│  │  ⊙ VERDE - RISCO BAIXO              │   │
│  │  Fadiga: 15%                        │   │
│  │  ✓ Você está descansado             │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Métricas em Tempo Real                     │
│  ┌────────┬─────────┬────────┬────────┐    │
│  │ ❤️ 72  │ 🫁 98%  │🌡️ 36.8│ 📊 15% │    │
│  │ BPM    │ SpO2    │ TEMP   │FADIGA  │    │
│  │ Normal │ Ótimo   │Normal  │ Baixo  │    │
│  └────────┴─────────┴────────┴────────┘    │
│                                             │
│  [📊 Análise] [📋 Histórico] [⚡ Alertas]   │
│                                             │
│  Status do Dispositivo:                     │
│  ⚫ Conectado (SmartWatch_Fadiga)           │
│  🔋 Bateria: 67%                           │
│  📡 Signal: RSSI -45dBm                    │
│                                             │
└─────────────────────────────────────────────┘
```

**Funcionalidades**:
- Auto-atualiza a cada 2 segundos via Bluetooth
- Indicador de conexão com ícone
- Botões de ação rápida
- Notificações em tempo real

### 4.3 Tela de Análise Detalhada

```
┌─────────────────────────────────────────────┐
│ < Home              📊 Análise Detalhada    │
├─────────────────────────────────────────────┤
│                                             │
│ Períodos de Visualização:                   │
│ [1h] [4h] [24h] [7d] [30d]                 │
│        ▼                                    │
│                                             │
│ Gráfico: Frequência Cardíaca               │
│ ┌─────────────────────────────────────┐    │
│ │ BPM │                      ╱╲       │    │
│ │     │   ╱╲    ╱╲   ╱╲ ╱╲ ╱  ╲     │    │
│ │ 80  │──╱  ╲──╱  ╲─╱  ╲╱    ╲__   │    │
│ │ 60  │╱                            │    │
│ │     │────────────────────────────│    │
│ │     0h    6h   12h   18h   24h  │    │
│ └─────────────────────────────────────┘    │
│ 📊 Estatísticas:                           │
│ • Mínimo: 50 BPM (03:15)                   │
│ • Máximo: 102 BPM (16:45)                  │
│ • Média: 74 BPM                            │
│ • Desvio: ±18 BPM                          │
│                                             │
│ [SpO2] [Temperatura] [Fadiga]               │
│                                             │
└─────────────────────────────────────────────┘
```

**Recursos**:
- Múltiplos gráficos deslizáveis
- Zoom in/out por pinch
- Toque no gráfico → ver valor exato
- Exportar dados em CSV
- Compartilhar com médico (PDF)

### 4.4 Tela de Alertas

```
┌─────────────────────────────────────────────┐
│ < Home                    🔔 Alertas        │
├─────────────────────────────────────────────┤
│                                             │
│ Filtros: [Todos] [Ativo] [Hoje] [Semana]  │
│                                             │
│ ┌─────────────────────────────────────┐    │
│ │ 🟢 14/04 - 14:30                    │    │
│ │ Saída do Modo de Risco Alto        │    │
│ │ Parabéns! Fadiga normalizou.        │    │
│ └─────────────────────────────────────┘    │
│                                             │
│ ┌─────────────────────────────────────┐    │
│ │ 🟡 14/04 - 11:15                    │    │
│ │ Alerta: Fadiga Moderada             │    │
│ │ Sua fadiga está em nível médio.     │    │
│ │ Recomenda-se descanso em breve.     │    │
│ └─────────────────────────────────────┘    │
│                                             │
│ ┌─────────────────────────────────────┐    │
│ │ 🔴 14/04 - 09:45                    │    │
│ │ ALERTA: Fadiga Severa!              │    │
│ │ BPM: 118 | SpO2: 91% | Temp: 37.2  │    │
│ │ [Ver Contexto] [Descartar]          │    │
│ └─────────────────────────────────────┘    │
│                                             │
│ Histórico de Alertas (30 dias)              │
│ ├─ Sem alertas: 18 dias                    │
│ ├─ Alertas baixos: 8 dias                  │
│ └─ Alertas altos: 4 dias                   │
│                                             │
└─────────────────────────────────────────────┘
```

### 4.5 Tela de Histórico

```
┌─────────────────────────────────────────────┐
│ < Home               📋 Histórico           │
├─────────────────────────────────────────────┤
│                                             │
│ 📅 Data: [14 Abril ▼] [Últimos 7 dias ▼]  │
│                                             │
│ 14 de Abril, 2024                           │
│ ┌─────────────────────────────────────┐    │
│ │ Horámos │ HR  │ SpO2│Temp│Fadiga│     │ │
│ ├─────────────────────────────────────┤    │
│ │ 00:00   │ 62  │ 97% │36.8│ 12%  │     │ │
│ │ 01:00   │ 58  │ 98% │36.9│ 8%   │     │ │
│ │ 02:00   │ 55  │ 98% │37.0│ 5%   │ ✓ │ │
│ │ ...     │ ... │ ... │... │ ...  │     │ │
│ │ 23:00   │ 68  │ 97% │36.7│ 18%  │     │ │
│ └─────────────────────────────────────┘    │
│                                             │
│ Resumo do Dia:                              │
│ • Média HR: 72 BPM                         │
│ • Pico HR: 102 BPM às 16:45                │
│ • Duração monitorada: 18h 32m              │
│ • Alertas: 2 (1 médio, 1 baixo)            │
│                                             │
│ [⬇️ Exportar] [📤 Compartilhar]             │
│                                             │
└─────────────────────────────────────────────┘
```

**Funcionalidades**:
- Scroll por data
- Modo detalhado/resumido
- Seleção de múltiplos dias
- Comparação entre períodos

### 4.6 Tela de Configurações

```
┌─────────────────────────────────────────────┐
│ < Home                ⚙️ Configurações      │
├─────────────────────────────────────────────┤
│                                             │
│ 👤 Perfil                                   │
│ ├─ Nome: João Silva                        │
│ ├─ Idade: 35 anos                          │
│ ├─ Sexo: Masculino                         │
│ └─ [Editar Perfil]                         │
│                                             │
│ 📱 Dispositivo                              │
│ ├─ Nome: SmartWatch_Fadiga                 │
│ ├─ MAC: AA:BB:CC:DD:EE:FF                  │
│ ├─ Versão Firmware: 1.2.3                  │
│ ├─ Última Sincronização: 2 min atrás       │
│ └─ [Reacoplar Dispositivo]                 │
│                                             │
│ 🚨 Notificações                             │
│ ├─ ☑️ Ativar Notificações                   │
│ ├─ ☑️ Som de Alerta                        │
│ ├─ ☑️ Vibração                             │
│ ├─ ☑️ Teste de Conexão a cada 5min        │
│ └─ Horário Silencioso: [21:00 - 08:00]    │
│                                             │
│ ⚠️ Limiares de Alerta                      │
│ ├─ BPM Alto: [120 bpm] ▹                   │
│ ├─ BPM Baixo: [50 bpm] ▹                   │
│ ├─ SpO2 Mínimo: [92%] ▹                    │
│ ├─ Fadiga Crítica: [75%] ▹                 │
│ └─ Temperatura Máx: [38.0°C] ▹             │
│                                             │
│ 📊 Dados                                    │
│ ├─ Armazenamento Local: 245 MB             │
│ ├─ [Cloud: Sincronizar Agora]              │
│ ├─ [Exportar Histórico]                    │
│ └─ [Limpar Cache]                          │
│                                             │
│ ℹ️ Sobre                                    │
│ ├─ Versão: 1.0.0                           │
│ ├─ Build: 2024.04                          │
│ └─ [Termos de Uso] [Privacidade]           │
│                                             │
└─────────────────────────────────────────────┘
```

## 5. Estrutura de Dados (Local Storage)

### 5.1 SQLite Schema

```sql
-- Tabela de leituras biométricas
CREATE TABLE readings (
    id INTEGER PRIMARY KEY,
    device_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    bpm INTEGER,
    spo2 INTEGER,
    temperature REAL,
    fatigue_level INTEGER,
    risk_level INTEGER,
    synced BOOLEAN DEFAULT FALSE
);

-- Índice para queries rápidas
CREATE INDEX idx_timestamp ON readings(timestamp);
CREATE INDEX idx_synced ON readings(synced);

-- Tabela de alertas
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    device_id TEXT NOT NULL,
    alert_type TEXT,  -- 'HIGH_BPM', 'LOW_SPO2', 'FADIGA_ALTA', etc
    timestamp DATETIME,
    value_bpm INTEGER,
    value_spo2 INTEGER,
    value_fatigue INTEGER,
    user_acknowledged BOOLEAN DEFAULT FALSE
);

-- Tabela de configurações
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de pareamento
CREATE TABLE paired_devices (
    id INTEGER PRIMARY KEY,
    device_name TEXT,
    device_address TEXT UNIQUE,
    paired_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_connected DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);
```

## 6. Comunicação Bluetooth - Protocolo

### 6.1 UUID do Serviço GATT

```
Primary Service:
UUID: 12345678-1234-1234-1234-123456789012

Characteristics:
1. Biometric Data (Read+Notify)
   UUID: 11111111-2222-3333-4444-555555555555
   Props: Read, Notify
   Format: JSON
   Example: {"bpm":75,"spo2":97,"temp":36.5,...}

2. Control Command (Write)
   UUID: 22222222-2222-3333-4444-555555555555
   Props: Write
   Format: JSON Command
   Example: {"cmd":"start_logging","interval":1000}

3. Sync Status (Read)
   UUID: 33333333-2222-3333-4444-555555555555
   Props: Read
   Format: JSON
   Example: {"battery":67,"rssi":-45,"status":"ready"}
```

### 6.2 Mensagens Bidirecionais

**Smartphone → ESP32**:
```json
{
  "cmd": "start_sync",
  "timestamp": 1713279600,
  "request_id": "req_12345"
}

{
  "cmd": "set_thresholds",
  "bpm_max": 120,
  "spo2_min": 92
}

{
  "cmd": "ping"
}
```

**ESP32 → Smartphone**:
```json
{
  "type": "reading",
  "bpm": 75,
  "spo2": 97,
  "temperature": 36.5,
  "fatigue_level": 25,
  "risk_level": 0,
  "timestamp": 1713279600
}

{
  "type": "alert",
  "alert_type": "HIGH_FATIGUE",
  "severity": "high",
  "message": "Fadiga severa detectada"
}

{
  "type": "pong",
  "battery": 67,
  "rssi": -45
}
```

## 7. Permissões Necessárias

### Para iOS
```xml
<key>NSBluetoothPeripheralUsageDescription</key>
<string>Necessitamos acessar Bluetooth para conectar ao seu SmartWatch</string>
<key>NSBluetoothCentralUsageDescription</key>
<string>Necessitamos acessar Bluetooth para ler dados de saúde</string>
<key>NSHealthShareUsageDescription</key>
<string>Compartilhação opcional com app Saúde</string>
```

### Para Android
```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.INTERNET" />
```

## 8. Tratamento de Conectividade

```
Estados do App:
┌─────────────────────────┐
│   INICIALIZANDO         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  AGUARDANDO CONEXÃO     │
│ (Buscar device)         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  CONECTANDO             │
│ (GATT connect)          │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  SINCRONIZANDO          │
│ (Set notificações)      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  LIGADO ✓               │
│ (Recebendo dados)       │
└────────────┬────────────┘
             │
    ┌────────┴─────────┐
    ▼                  ▼
┌───────────┐   ┌─────────────┐
│ RECEBENDO │   │ DESCONECTADO│
│ DADOS     │   │ (Reconectar)│
└───────────┘   └─────────────┘
```

## 9. Estratégia de Sincronização

```
A cada 15 segundos:
1. Verificar conexão Bluetooth
2. Se desconectado: Tentar reconectar
3. Se conectado: Sincronizar buffer local
4. Salvar localmente se desconexão ocorrer
5. Atualizar UI com nova informação

Modo Economy (quando inativo > 2min):
- Pausar notificações
- Reduzir atualização para 1min
- Manter Bluetooth ativo (mas passive)

Modo Full (quando app está em foreground):
- Atualizar a cada 1-2s
- Som e vibração de alertas ativo
- Histórico completo sincronizado
```

## 10. Tratamento de Erros

```
Cenários de Erro:

1. Não consigo conectar ao device
   └─ Mostrar: "Não encontrado. Certifique-se que..."
   └─ Sugestões: "Abra Bluetooth, aproxime-se"

2. Conexão perdida mid-sync
   └─ Retentar automaticamente 3x
   └─ Se falhar: Usar dados locais

3. Dados corrompidos
   └─ Validar JSON
   └─ Se inválido: Descartar e continuar

4. Bateria do device baixa
   └─ Notificar user
   └─ Modo de economia de bateria
```

