# Guia de Implementação - Sistema de Detecção de Fadiga

## 1. Setup Inicial do Projeto

### 1.1 Estrutura de Diretórios

```
smartwatch-fadiga-project/
├── firmware/
│   ├── smartwatch_fadiga.ino          # Código principal ESP32
│   ├── lib/
│   │   ├── MAX30102/
│   │   ├── BluetoothSerial/
│   │   └── WebServer/
│   └── platformio.ini
│
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.js
│   │   │   ├── readings.js
│   │   │   ├── analytics.js
│   │   │   └── alerts.js
│   │   ├── services/
│   │   │   ├── redisService.js
│   │   │   ├── aiService.js
│   │   │   └── notificationService.js
│   │   ├── models/
│   │   │   ├── User.js
│   │   │   └── Reading.js
│   │   ├── middleware/
│   │   │   ├── auth.js
│   │   │   └── rateLimit.js
│   │   └── app.js
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt (Python)
│   └── package.json (Node)
│
├── mobile/
│   ├── lib/
│   │   ├── screens/
│   │   ├── widgets/
│   │   ├── services/
│   │   │   ├── bluetooth_service.dart
│   │   │   ├── api_service.dart
│   │   │   └── notification_service.dart
│   │   ├── models/
│   │   ├── bloc/
│   │   └── main.dart
│   └── pubspec.yaml
│
├── web-dashboard/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/
│   └── package.json
│
├── ai-model/
│   ├── fatigue_ai.py               # Seu arquivo já criado
│   ├── requirements.txt
│   ├── tests/
│   └── data/
│
├── docs/
│   ├── HARDWARE_CONNECTIONS.md      # Já criado
│   ├── REDIS_ARCHITECTURE.md         # Já criado
│   ├── DASHBOARD_SPECIFICATION.md    # Já criado
│   ├── MOBILE_APP_SPECIFICATION.md   # Já criado
│   ├── SYSTEM_ARCHITECTURE.md        # Já criado
│   └── API_DOCUMENTATION.md
│
└── README.md
```

## 2. Backend - Implementação Node.js

### 2.1 Estrutura de Pastas

```bash
cd backend
npm init -y
npm install express redis pg dotenv cors jsonwebtoken bcrypt
npm install --save-dev nodemon
```

### 2.2 Arquivo: src/app.js

```javascript
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const redisClient = require('./services/redisService');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Rotas
app.use('/api/auth', require('./api/auth'));
app.use('/api/readings', require('./api/readings'));
app.use('/api/analytics', require('./api/analytics'));
app.use('/api/alerts', require('./api/alerts'));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date() });
});

// Erro handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

module.exports = app;
```

### 2.3 Arquivo: src/index.js

```javascript
const app = require('./app');
const http = require('http');
const socketIO = require('socket.io');
const redisService = require('./services/redisService');

const PORT = process.env.PORT || 3000;

const server = http.createServer(app);
const io = socketIO(server, {
  cors: {
    origin: process.env.CORS_ORIGIN || '*'
  }
});

// WebSocket para real-time
io.on('connection', (socket) => {
  console.log('New WebSocket connection:', socket.id);
  
  socket.on('subscribe-user', (userId) => {
    socket.join(`user:${userId}`);
  });
  
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Health check para Redis
setInterval(async () => {
  try {
    await redisService.ping();
  } catch (err) {
    console.error('Redis connection lost:', err);
  }
}, 30000);
```

### 2.4 Arquivo: services/redisService.js

```javascript
const redis = require('redis');
const dotenv = require('dotenv');

dotenv.config();

const client = redis.createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

client.on('error', (err) => console.log('Redis Client Error', err));
client.connect();

const redisService = {
  // Stream operations
  addReading: async (userId, data) => {
    const key = `biometric_data:${userId}`;
    return await client.xAdd(key, '*', {
      bpm: data.bpm.toString(),
      spo2: data.spo2.toString(),
      temperature: data.temperature.toString(),
      fatigue_level: data.fatigue_level.toString(),
      risk_level: data.risk_level.toString()
    });
  },

  getRecentReadings: async (userId, minutes = 60) => {
    const key = `biometric_data:${userId}`;
    const now = Date.now();
    const startTime = now - (minutes * 60 * 1000);
    
    return await client.xRange(key, `${startTime}`, `${now}`);
  },

  // Hash operations
  updateUserMetrics: async (userId, metrics) => {
    const key = `${userId}:metrics:recent`;
    return await client.hSet(key, metrics);
  },

  getUserMetrics: async (userId) => {
    const key = `${userId}:metrics:recent`;
    return await client.hGetAll(key);
  },

  // Health check
  ping: async () => {
    return await client.ping();
  }
};

module.exports = redisService;
```

### 2.5 Arquivo: api/readings.js

```javascript
const express = require('express');
const router = express.Router();
const redisService = require('../services/redisService');
const aiService = require('../services/aiService');
const auth = require('../middleware/auth');

// POST /api/readings
router.post('/', auth, async (req, res) => {
  try {
    const { bpm, spo2, temperature, device_id } = req.body;
    const userId = req.user.id;

    // Validar dados
    if (!bpm || !spo2 || !temperature) {
      return res.status(400).json({ error: 'Missing fields' });
    }

    // Armazenar em Redis
    const readingId = await redisService.addReading(userId, {
      bpm, spo2, temperature,
      fatigue_level: 0,  // Será calculado
      risk_level: 0
    });

    // Análise IA
    const analysis = await aiService.analyzeFatigue(userId, {
      bpm, spo2, temperature
    });

    // Atualizar métricas recentes
    await redisService.updateUserMetrics(userId, {
      last_bpm: bpm.toString(),
      last_spo2: spo2.toString(),
      last_temperature: temperature.toString(),
      fatigue_level: analysis.fatigue_level.toString(),
      risk_level: analysis.risk_level.toString(),
      last_update: Date.now().toString()
    });

    // Gerar alertas se necessário
    if (analysis.risk_level > 0) {
      // TODO: Enviar notificação ao usuário
    }

    res.json({
      success: true,
      reading_id: readingId,
      analysis
    });

  } catch (error) {
    console.error('Error creating reading:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/readings/history
router.get('/history', auth, async (req, res) => {
  try {
    const userId = req.user.id;
    const { hours = 24 } = req.query;

    const readings = await redisService.getRecentReadings(userId, hours * 60);

    res.json({
      success: true,
      count: readings.length,
      data: readings
    });

  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
```

## 3. Mobile - Implementação Flutter

### 3.1 Arquivo: lib/services/bluetooth_service.dart

```dart
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BluetoothService {
  static final BluetoothService _instance = BluetoothService._internal();
  
  factory BluetoothService() {
    return _instance;
  }
  
  BluetoothService._internal();

  final FlutterBluePlus _flutterBlue = FlutterBluePlus.instance;
  BluetoothDevice? _connectedDevice;
  BluetoothCharacteristic? _bioCharacteristic;

  // Stream para leituras biométricas
  late Stream<List<BluetoothDevice>> _scanResults;

  Future<void> startScan() async {
    _scanResults = _flutterBlue.scan(timeout: const Duration(seconds: 10));
  }

  Future<void> connectToDevice(BluetoothDevice device) async {
    try {
      await device.connect();
      _connectedDevice = device;
      
      // Descobrir serviços
      List<BluetoothService> services = await device.discoverServices();
      
      for (var service in services) {
        for (var characteristic in service.characteristics) {
          if (characteristic.uuid.toString() == 'YOUR-BIO-CHAR-UUID') {
            _bioCharacteristic = characteristic;
            
            // Habilitar notificações
            await characteristic.setNotifyValue(true);
            
            // Ouvir valores
            characteristic.value.listen((value) {
              _processBioData(value);
            });
          }
        }
      }
    } catch (e) {
      print('Error connecting: $e');
    }
  }

  void _processBioData(List<int> value) {
    // Parse JSON do ESP32
    String jsonString = String.fromCharCodes(value);
    // Processar dados...
  }

  Future<void> disconnect() async {
    await _connectedDevice?.disconnect();
    _connectedDevice = null;
  }
}
```

### 3.2 Arquivo: lib/screens/home_screen.dart

```dart
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _bpm = 0;
  int _spo2 = 0;
  double _temperature = 0;
  int _fatigueLevel = 0;

  @override
  void initState() {
    super.initState();
    _setupBluetooth();
  }

  void _setupBluetooth() {
    // Inicializar conexão Bluetooth
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('💤 SmartWatch Fadiga'),
      ),
      body: Column(
        children: [
          // Status Card
          _buildStatusCard(),
          
          // Métricas Grid
          _buildMetricsGrid(),
          
          // Gráfico
          _buildChart(),
        ],
      ),
    );
  }

  Widget _buildStatusCard() {
    Color statusColor = _fatigueLevel < 30 
        ? Colors.green 
        : _fatigueLevel < 65 
            ? Colors.yellow 
            : Colors.red;

    return Container(
      margin: EdgeInsets.all(16),
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: statusColor.withOpacity(0.2),
        border: Border.all(color: statusColor),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Text('Fadiga: $_fatigueLevel%', style: TextStyle(fontSize: 24)),
          SizedBox(height: 8),
          Text(_getFatigueStatus()),
        ],
      ),
    );
  }

  String _getFatigueStatus() {
    if (_fatigueLevel < 30) return '✓ Você está descansado';
    if (_fatigueLevel < 65) return '⚠ Fadiga moderada';
    return '🚨 Fadiga severa!';
  }

  Widget _buildMetricsGrid() {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      children: [
        _buildMetricCard('❤️ BPM', '$_bpm', 'bpm'),
        _buildMetricCard('🫁 SpO2', '$_spo2%', 'spo2'),
        _buildMetricCard('🌡️ TEMP', '$_temperature°C', 'temp'),
        _buildMetricCard('📊 FADIGA', '$_fatigueLevel%', 'fatigue'),
      ],
    );
  }

  Widget _buildMetricCard(String label, String value, String type) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(label, style: TextStyle(fontSize: 12)),
            SizedBox(height: 8),
            Text(value, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  Widget _buildChart() {
    return Container(
      margin: EdgeInsets.all(16),
      height: 200,
      child: Card(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Center(child: Text('Gráfico com Chart.js')),
        ),
      ),
    );
  }
}
```

## 4. Teste de Integração

### 4.1 Teste de Ponta a Ponta

```bash
# 1. Iniciar Backend
cd backend
docker-compose up -d
npm start

# 2. Upload ESP32
# (Usar Arduino IDE)

# 3. Iniciar Mobile
cd mobile
flutter run -d android

# 4. Teste Manual
# - Colocar smartwatch no pulso
# - App detecta BLE?
# - Dados fluem para Redis?
# - Dashboard mostra em tempo real?
```

## 5. Deploy em Produção

### 5.1 Docker

```dockerfile
# Dockerfile Backend
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "src/index.js"]
```

### 5.2 Deployment com Docker Compose

```bash
docker-compose down
docker-compose pull
docker-compose up -d

# Verificar saúde
docker ps
curl http://localhost:3000/health
```

## 6. Monitoramento e Logs

### 6.1 Visualizar Logs

```bash
# Backend
docker logs -f smartwatch-backend

# Redis
docker exec -it smartwatch-redis redis-cli monitor

# Database
docker logs -f smartwatch-postgres
```

## 7. Performance

### Otimizações Importantes

```
ESP32:
- Clock reduzido para 80MHz em modo economia
- Light Sleep quando inativo
- Compressão de dados antes envio

Backend:
- Redis cache para métricas recentes
- Connection pooling de BD
- Rate limiting (100 req/min por usuário)

Mobile:
- Local cache com SQLite
- Lazy loading de histórico
- Batch sync a cada 15s

Dashboard:
- Virtual scrolling para histórico longo
- Agregação de dados no backend
- CDN para assets estáticos
```

## 8. Checklist de Verificação

- [ ] ESP32 detecta MAX30102 via I2C
- [ ] Leituras de BPM/SpO2/Temp realistas
- [ ] Bluetooth broadcasting funciona
- [ ] App mobile conecta via BLE
- [ ] Dados sincronizam ao Redis sem erros
- [ ] IA calcula fadiga corretamente
- [ ] Alertas disparam quando threshold atingido
- [ ] Dashboard atualiza em real-time via WebSocket
- [ ] Bateria ESP32 dura > 24 horas
- [ ] Sem memória leaks em app mobile

---

**Próximos passos**: Integração com ferramentas de CI/CD, testes automatizados, e otimizações de performance baseadas em telemetria real.

