# Diagrama de Conexão - ESP32 S3 SmartWatch Detecção de Fadiga

## 1. Diagrama de Pinos ESP32 S3 DevKit

```
              ┌─────────────────────┐
              │   ESP32 S3 DevKit   │
       ┌──────┤                     ├──────┐
       │      │  PINO 3V3  ← VCC    │      │
       │      │  PINO GND  ← GND    │      │
       │      │                     │      │
       │      │  PINO 8   (SDA)     │      │
       │      │  PINO 9   (SCL)     │      │
       │      │  PINO 15  (VIBR)    │      │
       │      │  PINO 13  (LED)     │      │
       │      │  PINO 14  (WAKE)    │      │
       │      │  PINO 35  (TEMP)    │      │
       │      │  PINO 5   (TX BLE)  │      │
       │      │  PINO 6   (RX BLE)  │      │
       │      └─────────────────────┘      │
       │                                    │
       │    ┌──────────────────────────┐    │
       │    │   MAX30102 Sensor        │    │
       │    │  (Batimento + SpO2)      │    │
       │    │                          │    │
       │    │  VCC  ──────────────────┼────┤ 3V3
       │    │  GND  ──────────────────┼────┤ GND
       │    │  SDA  ──────┬───────────┘    │
       │    │  SCL  ──────┼────────────────┘
       │    │  INT  ──────┐ (Opc.)
       │    └──────────────┼────────────────┘
       │           (fios de I2C)
       │
       │    ┌──────────────────────────┐
       │    │   VIBRADOR (Motor)       │
       │    │                          │
       │    │  Pino +  ─────────────┐  │
       │    │  Pino -  ─────────────┼─┼──┤ GND
       │    │         (via transistor)
       │    └──────────────────────┼──┘
       │         (para Pino 15)     │
       │                            │
       └────────────────────────────┘
```

## 2. Conexão I2C Detalhada (MAX30102)

```
ESP32 S3          MAX30102
─────────         ────────
Pino 8  (SDA) ──→ SDA
Pino 9  (SCL) ──→ SCL
3V3 ────────────→ VCC (3.3V)
GND ────────────→ GND

Resistores de Pull-up (opcional, MAX30102 já possui):
4.7kΩ entre SDA e 3V3
4.7kΩ entre SCL e 3V3
```

## 3. Circuito do Vibrador

```
         ESP32 S3 Pino 15
              │
              ├─────────────┐
              │             │
            1kΩ            ↓ (Base)
            Resistor    ┌─────┐
              │         │ 2N2222 (NPN BJT)
              ├────────→│  
              │         │Coletor
         GND──┤         │  
                        ├──────┐
                        │      │
                        │    Motor Vibrador
                        │       +
                        │
                        ├───────┐
                        │       │
                       ↓        ↓
                    Diodo 1N4007
                     (proteção)
                        │
                       GND
```

## 4. Sensor NTC (Temperatura)

```
3V3 ──────┬────────────────────┐
          │                    │
        10kΩ                   │
      (Resistor)               │
          │                  NTC
          │                (10kΩ@25°C)
          ├─── ADC Pino 35 ──→│
          │                    │
         GND←──────────────────┘
```

## 5. LED Status

```
3V3 ────→ [LED(2V,20mA)]──→ 330Ω ──→ ESP32 Pino 13 ──→ GND
```

## 6. Botão de Despertar

```
3V3 ────→ [Botão] ──→ ESP32 Pino 14 (INPUT_PULLUP) ──→ GND
```

## 7. Bateria e Alimentação

```
┌─────────────────────────────────┐
│     Bateria (3000mAh @ 3.7V)    │
│     Li-Po ou Li-Ion             │
│                                 │
│  + ──────────────┬──────────────┤ 3V3 (ESP32)
│                  │              │
│          ┌───────┴────────┐     │
│          │                │     │
│     Regulador DC-DC       │     │
│     (300mA @ 3.3V)        │     │
│                           │     │
│  - ─────────────┬────────GND────┘ GND (ESP32)
│                 │
│          ┴ (Capacitor 100uF)
└─────────────────┴──────────────────┘
```

## 8. Sequência de Inicialização do I2C

```c
// Configure no setup():
Wire.begin(8, 9);           // SDA=8, SCL=9
Wire.setClock(400000);      // 400kHz
Wire.setTimeOut(1000);      // Timeout de 1s
```

## 9. Protocolo de Comunicação Bluetooth

```
ESP32 S3 UART para Bluetooth (integrado)
Velocidade: 115200 bps
Formato: JSON de linha única

Dados enviados ("tx"):
{"bpm":75,"spo2":97,"temp":36.5,"fatigue":25,"risk":0,"ts":12345}

Comandos recebidos ("rx"):
"ping"           → {"response":"pong"}
"status"         → {"status":"active","bpm":75,...}
"reset_buffer"   → {"status":"buffer_reset"}
```

## 10. Mapeamento de Sinais Detalhado

| ESP32 Pino | Função         | Tipo    | Tensão | Periférico          |
|-----------|---------------|---------|--------|-------------------|
| 8         | I2C SDA       | I/O     | 3.3V   | MAX30102          |
| 9         | I2C SCL       | I/O     | 3.3V   | MAX30102          |
| 13        | LED Status    | Output  | 3.3V   | LED + Resistor    |
| 14        | Botão Despertar| Input   | 3.3V   | Botão com Pullup  |
| 15        | Vibrador Ctrl | Output  | 3.3V   | Transistor NPN    |
| 35        | Sensor Temp   | ADC1_7  | 3.3V   | Divisor NTC       |
| 3V3       | Alimentação   | Power   | 3.3V   | Regulador LDO     |
| GND       | Terra         | Power   | 0V     | Comum             |

## 11. Verificação de Conexão

```python
# Script para verificar I2C (Arduino IDE)
void check_i2c() {
  byte error, address;
  byte nDevices = 0;
  
  Serial.println("Scanning I2C...");
  
  for(address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("Device found at 0x");
      Serial.println(address, HEX);
      nDevices++;
    }
  }
  
  if (nDevices == 0) {
    Serial.println("No I2C devices found!");
  }
}
```

## 12. Consumo de Energia

| Componente      | Estado      | Corrente |
|----------------|-----------|----------|
| ESP32 S3       | Ativo     | 80 mA    |
| ESP32 S3       | Light Sleep| 10 mA    |
| MAX30102       | Lendo     | 15 mA    |
| MAX30102       | Standby   | 2 mA     |
| Vibrador       | Desligado | 0 mA     |
| Vibrador       | Ligado    | 100 mA   |
| LED Status     | Ligado    | 20 mA    |
| **Total (Normal)** | **Ativo** | **~115 mA** |
| **Total (Otimizado)** | **Sleep Mode** | **~15 mA** |

## 13. Duração da Bateria

Considerando bateria de 3000 mAh:

- **Modo Normal (115 mA médio)**: ~26 horas
- **Modo Otimizado (50 mA médio)**: ~60 horas
- **Modo Sleep (15 mA médio)**: ~200 horas

## 14. Troubleshooting

| Problema              | Causa Provável          | Solução                |
|--------------------|------------------------|----------------------|
| MAX30102 não detectado| Fios soltos             | Verificar conexão I2C |
| BPM inconsistente    | Dedo mal posicionado    | Calibrar sensor       |
| ConexãoBT fraca      | Interferência          | Afastar de Wi-Fi      |
| Bateria esgota rápido| Clock muito alto        | Usar Light Sleep      |
| Vibrador não responde| Transistor queimado     | Substituir transistor |

