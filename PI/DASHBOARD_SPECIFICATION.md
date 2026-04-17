# Dashboard de Detecção de Fadiga - Especificação de Design

## 1. Visão Geral da Interface

O dashboard deve apresentar informações em tempo real com visualizações claras e intuitivas, permitindo o usuário monitorar sua saúde no computador/tablet enquanto sincroniza dados do smartwatch.

```
┌─────────────────────────────────────────────────────────────────┐
│  💤 SmartWatch Fadiga - Dashboard v1.0                    [Menu] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ Status em Tempo  │  │ Métricas Atuais  │  │  Alertas de  │ │
│  │  Real (Cores)    │  │  (Números/Gauge) │  │  Risco       │ │
│  │                  │  │                  │  │              │ │
│  │  ⚪ RISCO: BAIXO  │  │ ❤️ 72 BPM        │  │ Nenhum ⚫    │ │
│  │                  │  │ 🫁 98 %          │  │  alertas     │ │
│  │  Fadiga: 15%     │  │ 🌡️ 36.8°C        │  │  ativos      │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Gráfico de Frequência Cardíaca (Últimas 2h)             │  │
│  │                                                          │  │
│  │   BPM │                          ╱╲                     │  │
│  │   100 │                         ╱  ╲      ╱╲            │  │
│  │    80 │  ╱╲    ╱╲    ╱╲    ╱╲  ╱    ╲────╱  ╲          │  │
│  │    60 │ ╱  ╲──╱  ╲──╱  ╲╱╲╱    ╱─────       ╲         │  │
│  │       │                      │                │        │  │
│  │       └──────────────────────────────────────────       │  │
│  │       00:00  06:00  12:00  18:00  22:00  |AGORA|       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────┐ │
│  │ Oxigenação (SpO2)  │  │  Temperatura Corp. │  │ Fadiga   │ │
│  │                    │  │                    │  │ Diária   │ │
│  │ 🫁 98%             │  │ 🌡️ 36.8°C           │  │ 📊       │ │
│  │ █████████░ Normal  │  │ ████░░░░░ Normal   │  │ ▆▇█▆▅    │ │
│  │ Tendência: Estável │  │ Tendência: Estável │  │ 7d média │ │
│  └────────────────────┘  └────────────────────┘  └──────────┘ │
│                                                                 │
│ [📱 Abrir no Mobile] [⚙️ Configurações] [📊 Relatórios] [⚡ Mais] │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Componentes Principais

### 2.1 Card de Status Geral

**Objetivo**: Exibir classificação de risco em grande destaque

**Elementos**:
- Indicador circular com cores:
  - 🟢 Verde: Risco Baixo (Fadiga < 30%)
  - 🟡 Amarelo: Risco Médio (Fadiga 30-65%)
  - 🔴 Vermelho: Risco Alto (Fadiga > 65%)
- Percentual de fadiga (0-100)
- Timestamp da última leitura
- Ícone de conexão BLE

**Layout**:
```
┌─────────────────────────────┐
│   ⊙ RISCO: BAIXO           │
│    15% de Fadiga            │
│                             │
│   ✓ Conectado • 2min atrás  │
│   ⚠️ Próxima sincronização  │
│      em 45s                 │
└─────────────────────────────┘
```

### 2.2 Painel de Métricas Atuais

**Objetivo**: Mostrar últimas 4 leituras em formato visual

**Cards Individuais** (cada um com miniatura):

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  ❤️ BPM     │    │  🫁 SpO2    │    │  🌡️ TEMP    │    │  📊 FADIGA  │
├─────────────┤    ├─────────────┤    ├─────────────┤    ├─────────────┤
│   72        │    │   98        │    │   36.8      │    │   15        │
│             │    │             │    │             │    │             │
│ Normal      │    │ Ótimo       │    │ Normal      │    │ Baixo       │
│ ↓ 3 bpm     │    │ ↑ 1%        │    │ ↓ 0.1°C     │    │ ↑ 2 pts     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Cores de Status**:
- Verde: Normal/Ótimo
- Amarelo: Atenção requerida
- Vermelho: Crítico

### 2.3 Gráfico de Séries Temporais

**Tipos de Dados**:
1. **Frequência Cardíaca** (linha contínua azul)
   - Eixo Y: 40-160 BPM
   - Eixo X: 24 horas (selecionável)
   - Zona sombreada: Normal (60-100)

2. **Oxigenação** (linha contínua verde)
   - Eixo Y: 85-100%
   - Zona sombreada: Normal (>95%)

3. **Temperatura** (linha contínua laranja)
   - Eixo Y: 35-40°C
   - Zona sombreada: Normal (36.5-37.5)

4. **Fadiga** (curva vermelha)
   - Eixo Y: 0-100%
   - Zonas: Verde (0-30), Amarelo (30-65), Vermelho (65-100)

**Interatividade**:
- Hover → Exibir valor exato + timestamp
- Zoom in/out com scroll
- Seletor de período: 1h, 4h, 24h, 7d, 30d
- Exportar como PNG/CSV

### 2.4 Indicadores Gauge

Para resumir múltiplos dados em um visual único:

```
Exemplo: Gauge de BPM
         60 bpm
            ↓
    ┌──────●──────┐
    │              │
60  │              │  100  ← Escala
    │ △ 72 bpm    │
    └──────────────┘
    Normal se 60-100

Cores:
- Verde: Normal
- Amarelo: Alerta
- Vermelho: Crítico
```

### 2.5 Alert Box

**Exibição de Alertas Críticos**:

```
┌────────────────────────────────────────┐
│ 🚨 ALERTA: Fadiga Alta Detectada       │
│ ─────────────────────────────────────  │
│ Seu nível de fadiga está muito alto.   │
│ Recomendação: Procure descansar!       │
│ ────────────────────────────────────── │
│ [Dismiss] [Ver Detalhes] [Chamar Doc]  │
└────────────────────────────────────────┘
```

**Estados**:
- **Info** (azul): Informações gerais
- **Warning** (amarelo): Atenção necessária
- **Error** (vermelho): Ação urgente requerida
- **Success** (verde): Status positivo

### 2.6 Timeline de Eventos

```
Timeline de últimas 24 horas:
────────────────────────────────────►

14:30 - Fadiga Elevada
11:15 - Oxigenação Normal
08:45 - Início da Monitoração
```

## 3. Features Secundárias

### 3.1 Painel de Recomendações

```
┌────────────────────────────────────┐
│ 💡 Recomendações Personalizadas    │
├────────────────────────────────────┤
│ 1. ✓ Continue com atividade normal │
│ 2. ⏰ Próximo descanso recomendado │
│    em 2 horas                      │
│ 3. 💤 Padrao de sono adequado      │
│    detectado (↑7% comparado à      │
│    semana anterior)                │
│ 4. 🧘 Tente meditação antes de     │
│    dormir (-15% na fadiga noturna) │
└────────────────────────────────────┘
```

### 3.2 Histórico Semanal/Mensal

```
┌─────────────────────────────────┐
│ 📊 Resumo Semanal              │
├─────────────────────────────────┤
│ Fadiga Média:   35%  (↓5% vs.)  │
│ BPM Médio:      74   (↑2bpm)    │
│ SpO2 Média:     97% (Normal)    │
│ Horas Repouso:  45h  (7h/dia)   │
│ Noites com Risco Alto: 1        │
│ Melhoria: +12% comparado a mês  │
│ anterior                         │
└─────────────────────────────────┘
```

### 3.3 Settings/Configurações

```
⚙️ CONFIGURAÇÕES
├─ Dispositivo
│  ├─ Nome do SmartWatch: [ESP32_001        ]
│  ├─ Status de Conexão: Conectado ✓
│  └─ Última Sincronização: Há 2 minutos
│
├─ Limiares de Alerta
│  ├─ BPM Máximo: [120   ]
│  ├─ BPM Mínimo: [50    ]
│  ├─ SpO2 Mínimo: [92   ]
│  └─ Fadiga crítica em: [70%  ]
│
├─ Notificações
│  ├─ ☑️ Ativar notificações
│  ├─ ☑️ Sons de alerta
│  └─ Horário silencioso: [00:00 - 08:00]
│
└─ Dados
   ├─ Exportar Histórico
   └─ Limpar Cache Local
```

## 4. Design Visual

### 4.1 Paleta de Cores

```
Primárias:
- Azul (BPM): #3498DB
- Verde (SpO2/Normal): #27AE60
- Laranja (Temperatura): #E67E22
- Vermelho (Alerta): #E74C3C
- Amarelo (Atenção): #F39C12

Secundárias:
- Fundo: #1A1A1A (Dark mode) ou #F5F5F5 (Light)
- Texto: #FFFFFF (Dark) ou #222222 (Light)
- Bordas: #404040 (Dark) ou #CCCCCC (Light)

Gradientes:
- Risco Baixo: Verde → Verde claro
- Risco Médio: Amarelo → Laranja
- Risco Alto: Vermelho → Vermelho escuro
```

### 4.2 Tipografia

```
Títulos: Roboto Bold, 24-32px
Subtítulos: Roboto, 16-20px
Corpo: Roboto, 12-14px
Números: Courier New (monospace) para consistência
```

## 5. Responsividade

### 5.1 Desktop (≥1200px)
- Layout em 4 colunas
- Gráficos lado a lado
- Menu horizontalMenu superior

### 5.2 Tablet (768px-1200px)
- Layout em 2 colunas
- Gráficos empilhados
- Menu colapsável

### 5.3 Mobile (320px-768px)
- Layout em 1 coluna
- Cards empilhados verticalmente
- Menu drawer/hamburger
- Gráficos adaptáveis

## 6. Tecnologias Recomendadas

- **Frontend**: React.js / Vue.js / Angular
- **Gráficos**: Chart.js, D3.js, ou Recharts
- **Styling**: Tailwind CSS ou Material-UI
- **Backend**: Node.js/Express ou Python/Flask
- **WebSocket**: Para atualização em tempo real

## 7. API Endpoints Necessários

```
GET  /api/user/metrics/current     → Últimas métricas
GET  /api/user/metrics/history     → Histórico (query: period)
GET  /api/user/alerts              → Lista de alertas ativos
POST /api/user/settings            → Atualizar configurações
GET  /api/user/insights            → Análises e recomendações
GET  /api/device/status            → Status do smartwatch
POST /api/device/sync              → Iniciar sincronização
```

## 8. Exemplo de Estrutura HTML/React

```jsx
<Dashboard>
  <Header>
    <Logo /> <UserProfile /> <Menu />
  </Header>
  
  <MainContent>
    <StatusCard risk={risk} fatigue={fatigue} />
    
    <MetricsGrid>
      <MetricCard label="BPM" value={72} unit="bpm" status="normal" />
      <MetricCard label="SpO2" value={98} unit="%" status="normal" />
      <MetricCard label="Temp" value={36.8} unit="°C" status="normal" />
      <MetricCard label="Fadiga" value={15} unit="%" status="low" />
    </MetricsGrid>
    
    <ChartsSection>
      <TimeSeriesChart type="bpm" timeRange="24h" />
      <TimeSeriesChart type="spo2" timeRange="24h" />
      <TimeSeriesChart type="fatigue" timeRange="24h" />
    </ChartsSection>
    
    <RecommendationsPanel />
    <AlertsPanel />
  </MainContent>
  
  <Sidebar>
    <Navigation />
    <QuickStats />
  </Sidebar>
  
  <Footer>
    <SyncStatus /> <DeviceStatus />
  </Footer>
</Dashboard>
```

## 9. Performance

- Carregar dados de forma progressiva
- Cache local para últimas 24h
- Atualizar em real-time via WebSocket
- Degradar gracefully se offline
- Limite de 1000 pontos de dados por gráfico

