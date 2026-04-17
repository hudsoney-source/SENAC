# 🗂️ ÍNDICE MASTER - Sistema de Detecção de Fadiga

## 📑 Navegação Completa

### 🚀 Para Começar (Comece Aqui!)

| Documento | Descrição | Tempo |
|-----------|-----------|-------|
| [QUICK_START.md](QUICK_START.md) | 5 passos para ter tudo funcionando | **15 min** |
| [README.md](README.md) | Visão geral do projeto | 5 min |
| [DELIVERABLES_SUMMARY.md](DELIVERABLES_SUMMARY.md) | O que foi entregue | 10 min |

---

### 🔧 Hardware & Firmware

| Aspecto | Documento | Detalhes |
|--------|-----------|---------|
| **Código ESP32** | [smartwatch_fadiga.ino](smartwatch_fadiga.ino) | ~400 linhas C++ |
| **Pinagem** | [HARDWARE_CONNECTIONS.md](HARDWARE_CONNECTIONS.md#2-conexão-i2c-detalhada-max30102) | I2C, GPIO, SPI |
| **Diagramas** | [HARDWARE_CONNECTIONS.md](HARDWARE_CONNECTIONS.md#1-diagrama-de-pinos-esp32-s3-devkit) | ASCII art circuits |
| **Consumo Energia** | [HARDWARE_CONNECTIONS.md](HARDWARE_CONNECTIONS.md#12-consumo-de-energia) | Tabela watts/mA |
| **Troubleshooting** | [HARDWARE_CONNECTIONS.md](HARDWARE_CONNECTIONS.md#14-troubleshooting) | Problemas comuns |

---

### 🗄️ Backend & Banco de Dados

| Componente | Documento | Conteúdo |
|-----------|-----------|---------|
| **Redis Schemas** | [REDIS_ARCHITECTURE.md](REDIS_ARCHITECTURE.md#1-schemas-e-estruturas-de-dados) | Streams, Hashes, Sets |
| **Operações Redis** | [REDIS_ARCHITECTURE.md](REDIS_ARCHITECTURE.md#3-operações-redis-principais) | Python code examples |
| **Data Retention** | [REDIS_ARCHITECTURE.md](REDIS_ARCHITECTURE.md#4-política-de-retenção-de-dados) | TTL policies |
| **API Design** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#7-fluxo-de-dados-end-to-end) | Endpoints REST |
| **Implementation** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#26-backend---implementação-nodejs) | Code examples |
| **Docker Setup** | [docker-compose.yml](docker-compose.yml) | 7 serviços |

---

### 🤖 Inteligência Artificial

| Tópico | Arquivo | Descrição |
|--------|---------|-----------|
| **Código Python** | [fatigue_ai.py](fatigue_ai.py) | Classe `FatigueDetectionAI` |
| **Versão Executável** | [fatigue_ai.py](fatigue_ai.py#teste-e-demonstração) | `if __name__ == "__main__"` |
| **Componentes** | [fatigue_ai.py](fatigue_ai.py#componente-1-desvio-de-bpm) | BPM, SpO2, HRV, Trend |
| **Classificação** | [fatigue_ai.py](fatigue_ai.py#classify_risk_level) | Risco baixo/médio/alto |
| **Insights** | [fatigue_ai.py](fatigue_ai.py#generate_insights) | Recomendações personalizadas |
| **Arquitetura** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#5-pipeline-de-processamento-de-ia) | 7 estágios |

---

### 📱 Aplicativo Mobile

| Aspecto | Documento | Detalhes |
|--------|-----------|---------|
| **Telas** | [MOBILE_APP_SPECIFICATION.md](MOBILE_APP_SPECIFICATION.md#4-telas-principais) | 6 telas principais |
| **Bluetooth** | [MOBILE_APP_SPECIFICATION.md](MOBILE_APP_SPECIFICATION.md#6-comunicação-bluetooth---protocolo) | UUID, JSON format |
| **Storage** | [MOBILE_APP_SPECIFICATION.md](MOBILE_APP_SPECIFICATION.md#51-sqlite-schema) | SQLite tabelas |
| **Permissões** | [MOBILE_APP_SPECIFICATION.md](MOBILE_APP_SPECIFICATION.md#7-permissões-necessárias) | iOS/Android |
| **Flutter Code** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#31-arquivo-libservicesbluetoothservicedart) | BleService class |
| **Conectividade** | [MOBILE_APP_SPECIFICATION.md](MOBILE_APP_SPECIFICATION.md#8-tratamento-de-conectividade) | Estados e transições |

---

### 📊 Dashboard Web

| Componente | Documento | Descrição |
|-----------|-----------|-----------|
| **Overview** | [DASHBOARD_SPECIFICATION.md](DASHBOARD_SPECIFICATION.md#1-visão-geral-da-interface) | Layout completo |
| **Cards** | [DASHBOARD_SPECIFICATION.md](DASHBOARD_SPECIFICATION.md#21-card-de-status-geral) | Métricas e status |
| **Gráficos** | [DASHBOARD_SPECIFICATION.md](DASHBOARD_SPECIFICATION.md#23-gráfico-de-séries-temporais) | Chart.js tipos |
| **Responsividade** | [DASHBOARD_SPECIFICATION.md](DASHBOARD_SPECIFICATION.md#5-responsividade) | Desktop/Tablet/Mobile |
| **Tech Stack** | [DASHBOARD_SPECIFICATION.md](DASHBOARD_SPECIFICATION.md#6-tecnologias-recomendadas) | React, Chart.js, WebSocket |
| **HTML/React** | [DASHBOARD_SPECIFICATION.md](DASHBOARD_SPECIFICATION.md#8-exemplo-de-estrutura-htmlreact) | Código exemplo |

---

### 🏗️ Arquitetura Geral

| Seção | Arquivo | Tema |
|-------|---------|------|
| **Diagrama Completo** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#1-diagrama-de-arquitetura-geral) | 3 camadas + 4 subsistemas |
| **Fluxo de Dados** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#2-fluxo-de-dados-end-to-end) | Sensor → UI |
| **Stack Tech** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#3-stack-tecnológico-completo) | Frameworks e libs |
| **Modelo de Dados** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#4-modelo-de-dados) | ER diagram |
| **Segurança** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#8-segurança) | Encryption, Auth, etc |
| **Scaling** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#7-estratégia-de-scaling) | 3 fases de crescimento |
| **Monitoramento** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md#10-monitoramento-em-produção) | Métricas e alertas |

---

### 💻 Implementação Prática

| Tópico | Arquivo | Cobertura |
|--------|---------|-----------|
| **Project Setup** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#1-setup-inicial-do-projeto) | Pastas e estrutura |
| **Backend Code** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#2-backend---implementação-nodejs) | 5 arquivos exemplo |
| **Mobile Code** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#3-mobile---implementação-flutter) | 2 arquivos exemplo |
| **Testes** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#4-teste-de-integração) | Passos de validação |
| **Deploy Docker** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#5-deploy-em-produção) | Dockerfile |
| **Logs & Monitoring** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#6-monitoramento-e-logs) | Comandos úteis |
| **Checklist** | [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md#8-checklist-de-verificação) | 10 itens |

---

### 📦 Arquivos de Configuração

| Arquivo | Uso | Linhas |
|---------|-----|----|
| [requirements.txt](requirements.txt) | Dependências Python | 33 packages |
| [docker-compose.yml](docker-compose.yml) | Orquestração containers | 200+ |

---

## 🎯 Guia por Perfil

### 👨‍💻 Desenvolvedor Embarcado
```
1. QUICK_START.md → Passo 1 (Hardware)
2. smartwatch_fadiga.ino → Entender firmware
3. HARDWARE_CONNECTIONS.md → Conexões físicas
4. Serial Monitor → Validação
```

### 🔗 Desenvolvedor Backend
```
1. QUICK_START.md → Passo 2 (Backend)
2. REDIS_ARCHITECTURE.md → Schemas de dados
3. IMPLEMENTATION_GUIDE.md → Seção 2 (Backend)
4. docker-compose.yml → Setup completo
```

### 📱 Desenvolvedor Mobile
```
1. QUICK_START.md → Passo 6 (Mobile)
2. MOBILE_APP_SPECIFICATION.md → Visão completa
3. IMPLEMENTATION_GUIDE.md → Seção 3 (Mobile)
4. Flutter pubspec.yaml → Dependências
```

### 📊 Desenvolvedor Frontend
```
1. DASHBOARD_SPECIFICATION.md → Design completo
2. SYSTEM_ARCHITECTURE.md → API contracts
3. IMPLEMENTATION_GUIDE.md → Exemplo React
4. Chart.js docs → Visualizações
```

### 🤖 Data Scientist / IA
```
1. fatigue_ai.py → Modelo completo
2. SYSTEM_ARCHITECTURE.md → Seção 5 (Pipeline IA)
3. REDIS_ARCHITECTURE.md → Operações Redis
4. requirements.txt → Dependências ML
```

### 🏗️ Arquiteto de Sistemas
```
1. SYSTEM_ARCHITECTURE.md → Arquitetura completa
2. Diagrama Mermaid → Visão visual
3. IMPLEMENTATION_GUIDE.md → Stack tech
4. DELIVERABLES_SUMMARY.md → Visão geral
```

---

## 📈 Sequência de Aprendizado

### Nível 1: Conceitos (1-2 horas)
- [ ] Ler README.md
- [ ] Entender QUICK_START.md
- [ ] Ver diagrama Mermaid

### Nível 2: Implementação Hardware (2-3 horas)
- [ ] HARDWARE_CONNECTIONS.md (completo)
- [ ] smartwatch_fadiga.ino (comentários)
- [ ] Testes com Serial Monitor

### Nível 3: Backend e Dados (3-4 horas)
- [ ] REDIS_ARCHITECTURE.md (completo)
- [ ] SYSTEM_ARCHITECTURE.md (seções 2-5)
- [ ] IMPLEMENTATION_GUIDE.md (seção 2)

### Nível 4: IA e Analytics (2-3 horas)
- [ ] fatigue_ai.py (executar e entender)
- [ ] Componentes de análise
- [ ] Calibração de limiares

### Nível 5: Frontend (2-3 horas)
- [ ] DASHBOARD_SPECIFICATION.md (completo)
- [ ] MOBILE_APP_SPECIFICATION.md (completo)
- [ ] IMPLEMENTATION_GUIDE.md (seções 3-4)

### Nível 6: Deploy (1-2 horas)
- [ ] docker-compose.yml
- [ ] IMPLEMENTATION_GUIDE.md (seção 5-6)
- [ ] SYSTEM_ARCHITECTURE.md (seções 8-10)

**Total**: ~13-17 horas para domínio completo

---

## 🔍 Buscar por Tópico

### Como...

**...conectar MAX30102 ao ESP32?**
→ [HARDWARE_CONNECTIONS.md#2-conexão-i2c-detalhada](HARDWARE_CONNECTIONS.md#2-conexão-i2c-detalhada-max30102)

**...armazenar dados em Redis?**
→ [REDIS_ARCHITECTURE.md#31-registrar-nova-leitura](REDIS_ARCHITECTURE.md#31-registrar-nova-leitura)

**...calcular fadiga com IA?**
→ [fatigue_ai.py#get_all_metrics](fatigue_ai.py#get_all_metrics)

**...sincronizar Bluetooth?**
→ [MOBILE_APP_SPECIFICATION.md#6-comunicação-bluetooth---protocolo](MOBILE_APP_SPECIFICATION.md#6-comunicação-bluetooth---protocolo)

**...desenhar gráfico em tempo real?**
→ [DASHBOARD_SPECIFICATION.md#23-gráfico-de-séries-temporais](DASHBOARD_SPECIFICATION.md#23-gráfico-de-séries-temporais)

**...fazer deploy com Docker?**
→ [IMPLEMENTATION_GUIDE.md#5-deploy-em-produção](IMPLEMENTATION_GUIDE.md#5-deploy-em-produção)

**...otimizar bateria?**
→ [HARDWARE_CONNECTIONS.md#12-consumo-de-energia](HARDWARE_CONNECTIONS.md#12-consumo-de-energia)

**...tratar erros de Bluetooth?**
→ [MOBILE_APP_SPECIFICATION.md#10-tratamento-de-erros](MOBILE_APP_SPECIFICATION.md#10-tratamento-de-erros)

---

## 📥 Imports Rápidos

Se você encontrou este projeto e quer integrar:

### Para Projeto Python
```python
from fatigue_ai import FatigueDetectionAI

ai = FatigueDetectionAI(window_size=60)
ai.add_reading(bpm=75, spo2=97, temperature=36.5)
score, components = ai.calculate_fatigue_score()
```

### Para Projeto Node.js
```javascript
const redisService = require('./services/redisService');

await redisService.addReading(userId, {bpm, spo2, temperature});
const metrics = await redisService.getUserMetrics(userId);
```

### Para Flutter
```dart
import 'services/bluetooth_service.dart';

final ble = BluetoothService();
await ble.connectToDevice(device);
```

---

## 🎓 Referências Externas

### Hardware/IoT
- ESP32 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf
- MAX30102 Sparkfun: https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library

### Backend/Web
- Express.js: https://expressjs.com
- Redis Documentation: https://redis.io/documentation
- WebSocket: https://socket.io

### Mobile
- Flutter: https://flutter.dev
- React Native: https://reactnative.dev
- Flutter Blue Plus: https://pub.dev/packages/flutter_blue_plus

### Web
- React: https://react.dev
- Chart.js: https://www.chartjs.org
- Tailwind CSS: https://tailwindcss.com

---

## 📞 Dúvidas Frequentes

**P: Quanto tempo para implementar tudo?**
R: 2-4 semanas dependendo da experiência. Veja QUICK_START.md para versão acelerada.

**P: Posso usar diferentes sensores?**
R: Sim, adapte smartwatch_fadiga.ino para seu sensor (I2C, SPI, etc).

**P: Qual o custo total?**
R: ~$50-100 (ESP32 $10, MAX30102 $15-20, bateria $10, resto eletrônicos).

**P: Funciona offline?**
R: Sim, mobile sincroniza com backend quando conectado à internet.

**P: Qual a acurácia?**
R: Depende de calibração. Esperamos >85% com dados clínicos reais.

---

**Última atualização**: 16 de Abril de 2024
**Versão**: 1.0.0
**Arquivos**: 10+ documentos + código pronto

