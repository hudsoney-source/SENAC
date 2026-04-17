/*
 * SISTEMA DE DETECÇÃO DE FADIGA COM ESP32 S3 + MAX30102
 * 
 * Funcionalidades:
 * - Leitura de batimento cardíaco (BPM) via MAX30102
 * - Leitura de oxigenação (SpO2) 
 * - Leitura de temperatura
 * - Comunicação Bluetooth para smartphone
 * - Vibrador para alertas
 * - Otimização de consumo de energia
 * - Sincronização com Redis backend
 */

#include <Wire.h>
#include <BluetoothSerial.h>
#include "MAX30102.h"
#include <EEPROM.h>
#include <esp_sleep.h>

// ==================== CONFIGURAÇÕES ====================
#define MAX30102_ADDR 0x57
#define VIBRADOR_PIN 15
#define LED_STATUS_PIN 13
#define BUTTON_WAKE_PIN 14

// Constantes de retenção de dados
#define EEPROM_SIZE 512
#define SAMPLES_PER_MINUTE 60
#define BUFFER_SIZE 600  // 10 minutos de dados

// Estruturas de dados
struct BiometricData {
  uint16_t bpm;           // Batimento cardíaco
  uint8_t spo2;           // Oxigenação
  float temperature;      // Temperatura
  uint32_t timestamp;     // Timestamp
  uint8_t fatigue_level;  // 0-100, 0=descansado, 100=muito cansado
};

struct FAtigueAnalysis {
  uint8_t risk_level;     // 0=baixo, 1=médio, 2=alto
  float trend;            // -1 a 1 (piorando a melhorando)
  char recommendation[128];
};

// Variáveis globais
BluetoothSerial SerialBT;
MAX30102 sensor;
BiometricData sensor_data;
BiometricData data_buffer[BUFFER_SIZE];
uint16_t buffer_index = 0;

FAtigueAnalysis current_analysis;
uint32_t last_sync = 0;
uint32_t last_vibration = 0;
bool ble_connected = false;

// ==================== CALIBRAÇÃO MAX30102 ====================
void init_MAX30102() {
  Serial.println("[INIT] Inicializando MAX30102...");
  
  if (!sensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("[ERROR] MAX30102 não respondeu!");
    while (1);
  }
  
  // Configuração para detecção de dedo
  sensor.setup(0x1F, 0x02, 100, 0x00, 3, 100);
  
  // LED Bright configuration
  sensor.setPulseAmplitudeRed(0x0A);
  sensor.setPulseAmplitudeGreen(0x00);
  sensor.setPulseAmplitudeIR(0x33);
  
  Serial.println("[OK] MAX30102 calibrado!");
}

// ==================== LEITURA DE SENSORES ====================
void read_biometric_data() {
  sensor_data.timestamp = millis();
  
  // Verificar disponibilidade de dados
  int32_t bufferLength = sensor.available();
  
  if (bufferLength > 0) {
    // Limpar buffer antigo
    while (sensor.available() > 100) {
      sensor.nextSample();
    }
    
    // Ler múltiplas amostras para análise
    uint32_t red_sum = 0, ir_sum = 0;
    int samples_count = 0;
    
    while (sensor.available()) {
      red_sum += sensor.getFIFORed();
      ir_sum += sensor.getFIFOIR();
      sensor.nextSample();
      samples_count++;
    }
    
    // Calcular média
    uint32_t red_avg = red_sum / max(1, samples_count);
    uint32_t ir_avg = ir_sum / max(1, samples_count);
    
    // Estimação de BPM (algoritmo simplificado)
    sensor_data.bpm = estimate_bpm(red_avg, ir_avg);
    
    // Estimação de SpO2
    sensor_data.spo2 = estimate_spo2(red_avg, ir_avg);
    
    // Leitura de temperatura (simulada via resistor de temperatura)
    sensor_data.temperature = read_temperature();
    
  } else {
    // Valores padrão se nenhum dedo detectado
    sensor_data.bpm = 0;
    sensor_data.spo2 = 0;
  }
}

// ==================== ESTIMATIVA DE BPM ====================
uint16_t estimate_bpm(uint32_t red, uint32_t ir) {
  // Algoritmo simplificado de correlação para detecção de pico
  static uint32_t prev_ir = 0;
  static uint8_t peak_count = 0;
  static uint32_t peak_timer = 0;
  
  // Detectar pico quando IR desce após subir
  if (ir < prev_ir && prev_ir > 100000) {
    peak_count++;
    
    if (peak_timer == 0) {
      peak_timer = millis();
    }
  }
  
  prev_ir = ir;
  
  // Calcular BPM a cada 60 segundos
  uint32_t elapsed = millis() - peak_timer;
  if (elapsed >= 60000 && peak_count > 0) {
    uint16_t bpm = (peak_count * 60000) / elapsed;
    peak_count = 0;
    peak_timer = 0;
    return constrain(bpm, 30, 200);  // BPM realista
  }
  
  return 0;  // Esperando amostras
}

// ==================== ESTIMATIVA DE SpO2 ====================
uint8_t estimate_spo2(uint32_t red, uint32_t ir) {
  // Razão de absorção de luz vermelha vs infravermelha
  if (ir == 0) return 0;
  
  float ratio = (float)red / (float)ir;
  
  // Calibração empírica (requer calibração em produção)
  float spo2 = 110.0 - 25.0 * ratio;
  
  return constrain((uint8_t)spo2, 70, 100);
}

// ==================== LEITURA DE TEMPERATURA ====================
float read_temperature() {
  // Usar sensor NTC via GPIO35 (ADC1)
  uint16_t raw = analogRead(35);
  
  // Conversão ADC para resistência
  float resistance = 4095.0 / raw - 1.0;
  resistance = 10000.0 / resistance;  // Divisor de tensão
  
  // Conversão Steinhart-Hart (coeficientes típicos)
  float t1 = log(resistance / 10000.0);
  float B = 3950.0;
  float T0 = 298.15;  // 25°C em Kelvin
  
  float temperature = 1.0 / ((t1 / B) + (1.0 / T0)) - 273.15;
  
  return constrain(temperature, 30.0, 40.0);
}

// ==================== ANÁLISE DE FADIGA ====================
void analyze_fatigue() {
  if (buffer_index < 30) return;  // Necessário mínimo 30 amostras
  
  // Análise de padrões
  float avg_bpm = 0, avg_spo2 = 0, avg_temp = 0;
  float bpm_variance = 0, spo2_variance = 0;
  
  // Calcular médias
  uint16_t valid_samples = 0;
  for (int i = 0; i < buffer_index; i++) {
    if (data_buffer[i].bpm > 0 && data_buffer[i].spo2 > 0) {
      avg_bpm += data_buffer[i].bpm;
      avg_spo2 += data_buffer[i].spo2;
      avg_temp += data_buffer[i].temperature;
      valid_samples++;
    }
  }
  
  if (valid_samples == 0) return;
  
  avg_bpm /= valid_samples;
  avg_spo2 /= valid_samples;
  avg_temp /= valid_samples;
  
  // Calcular variância
  for (int i = 0; i < buffer_index; i++) {
    float bpm_diff = data_buffer[i].bpm - avg_bpm;
    float spo2_diff = data_buffer[i].spo2 - avg_spo2;
    bpm_variance += bpm_diff * bpm_diff;
    spo2_variance += spo2_diff * spo2_diff;
  }
  
  bpm_variance = sqrt(bpm_variance / valid_samples);
  spo2_variance = sqrt(spo2_variance / valid_samples);
  
  // Regras de classificação
  sensor_data.fatigue_level = calculate_fatigue_level(
    avg_bpm, avg_spo2, avg_temp, bpm_variance, spo2_variance
  );
  
  // Determinar nível de risco e recomendações
  determine_risk_level(avg_bpm, avg_spo2, sensor_data.fatigue_level);
  
  // Calcular tendência
  if (buffer_index > 60) {
    float recent_avg = 0, old_avg = 0;
    for (int i = 30; i < 60; i++) {
      if (data_buffer[i].bpm > 0) recent_avg += data_buffer[i].bpm;
    }
    for (int i = 0; i < 30; i++) {
      if (data_buffer[i].bpm > 0) old_avg += data_buffer[i].bpm;
    }
    recent_avg /= 30;
    old_avg /= 30;
    current_analysis.trend = (recent_avg - old_avg) / old_avg;
  }
}

// ==================== CÁLCULO DE NÍVEL DE FADIGA ====================
uint8_t calculate_fatigue_level(float bpm, float spo2, float temp, 
                                float bpm_var, float spo2_var) {
  uint8_t fatigue = 0;
  
  // Critério 1: Frequência cardíaca elevada (repouso deve ser 60-100 BPM)
  if (bpm > 100) {
    fatigue += 20;  // Taquicardia pode indicar fadiga
  } else if (bpm < 50) {
    fatigue += 10;  // Bradicardia anormal
  }
  
  // Critério 2: Redução de SpO2 (normal > 95%)
  if (spo2 < 92) {
    fatigue += 30;  // Hipoxemia significativa
  } else if (spo2 < 95) {
    fatigue += 10;  // Ligeira redução
  }
  
  // Critério 3: Variabilidade da FC (alta variabilidade = fadiga)
  if (bpm_var > 20) {
    fatigue += 15;
  } else if (bpm_var > 15) {
    fatigue += 8;
  }
  
  // Critério 4: Estabilidade de SpO2
  if (spo2_var > 3) {
    fatigue += 10;
  }
  
  // Critério 5: Temperatura elevada
  if (temp > 37.5) {
    fatigue += 5;
  }
  
  return constrain(fatigue, 0, 100);
}

// ==================== DETERMINAR NÍVEL DE RISCO ====================
void determine_risk_level(float bpm, float spo2, uint8_t fatigue_level) {
  // Classificação de risco
  if (fatigue_level < 30 && spo2 > 95 && bpm < 100) {
    current_analysis.risk_level = 0;  // Baixo risco
    strcpy(current_analysis.recommendation, 
           "Status normal. Continue monitorando regularmente.");
  } 
  else if (fatigue_level < 60 && spo2 > 92) {
    current_analysis.risk_level = 1;  // Médio risco
    strcpy(current_analysis.recommendation, 
           "Fadiga moderada detectada. Recomenda-se descanso em breve.");
  } 
  else {
    current_analysis.risk_level = 2;  // Alto risco
    strcpy(current_analysis.recommendation, 
           "ALERTA: Fadiga severa! Procure descanso IMEDIATAMENTE.");
  }
}

// ==================== COMUNICAÇÃO BLUETOOTH ====================
void send_ble_data() {
  if (!ble_connected) return;
  
  // Formato JSON para envio
  char json_buffer[256];
  snprintf(json_buffer, sizeof(json_buffer),
    "{\"bpm\":%d,\"spo2\":%d,\"temp\":%.1f,\"fatigue\":%d,\"risk\":%d,\"ts\":%lu}",
    sensor_data.bpm, sensor_data.spo2, sensor_data.temperature,
    sensor_data.fatigue_level, current_analysis.risk_level, sensor_data.timestamp
  );
  
  SerialBT.print(json_buffer);
  SerialBT.print("\n");
  
  Serial.print("[BLE TX] ");
  Serial.println(json_buffer);
}

// ==================== CONTROLE DE VIBRADOR ====================
void trigger_vibration_alert(uint8_t pattern) {
  uint32_t now = millis();
  
  // Debounce: não ativar vibrações com menos de 5 segundos de intervalo
  if (now - last_vibration < 5000) return;
  
  last_vibration = now;
  
  switch (pattern) {
    case 0:  // Alerta suave (fadiga moderada)
      for (int i = 0; i < 3; i++) {
        digitalWrite(VIBRADOR_PIN, HIGH);
        delay(100);
        digitalWrite(VIBRADOR_PIN, LOW);
        delay(100);
      }
      break;
      
    case 1:  // Alerta urgente (fadiga severa)
      for (int i = 0; i < 5; i++) {
        digitalWrite(VIBRADOR_PIN, HIGH);
        delay(150);
        digitalWrite(VIBRADOR_PIN, LOW);
        delay(75);
      }
      break;
      
    case 2:  // Padrão contínuo (crítico)
      digitalWrite(VIBRADOR_PIN, HIGH);
      delay(500);
      digitalWrite(VIBRADOR_PIN, LOW);
      delay(200);
      digitalWrite(VIBRADOR_PIN, HIGH);
      delay(500);
      digitalWrite(VIBRADOR_PIN, LOW);
      break;
  }
}

// ==================== GERENCIAMENTO DE BUFFER ====================
void add_to_buffer() {
  if (buffer_index >= BUFFER_SIZE) {
    // Deslocar dados antigos
    memmove(data_buffer, data_buffer + 1, 
            (BUFFER_SIZE - 1) * sizeof(BiometricData));
    buffer_index = BUFFER_SIZE - 1;
  }
  
  data_buffer[buffer_index++] = sensor_data;
}

// ==================== SINCRONIZAÇÃO COM REDIS ====================
void sync_with_redis() {
  uint32_t now = millis();
  
  // Sincronizar a cada 60 segundos ou quando nível de risco muda
  if (now - last_sync > 60000) {
    last_sync = now;
    
    if (ble_connected) {
      // Enviar comando de sincronização
      char sync_cmd[256];
      snprintf(sync_cmd, sizeof(sync_cmd),
        "{\"cmd\":\"sync\",\"data\":[");
      
      SerialBT.print(sync_cmd);
      
      // Enviar últimos 10 minutos de dados
      for (int i = 0; i < min(600, (int)buffer_index); i++) {
        if (data_buffer[i].bpm > 0) {
          snprintf(sync_cmd, sizeof(sync_cmd),
            "{\"bpm\":%d,\"spo2\":%d,\"temp\":%.1f,\"ts\":%lu}%s",
            data_buffer[i].bpm, data_buffer[i].spo2,
            data_buffer[i].temperature, data_buffer[i].timestamp,
            (i < buffer_index - 1) ? "," : "");
          SerialBT.print(sync_cmd);
        }
      }
      
      SerialBT.println("]}");
    }
  }
}

// ==================== OTIMIZAÇÃO DE ENERGIA ====================
void optimize_power_consumption() {
  // Reduzir brilho de LED quando inativo
  if (ble_connected) {
    digitalWrite(LED_STATUS_PIN, HIGH);
  } else {
    digitalWrite(LED_STATUS_PIN, LOW);
  }
  
  // Light Sleep se nenhum alerta urgente
  if (current_analysis.risk_level < 2) {
    // Manter operação normal mas com reduções de clock
    setCpuFrequencyMhz(80);  // Reduzir de 240MHz para 80MHz
  } else {
    setCpuFrequencyMhz(240);  // Clock máximo para alertas
  }
}

// ==================== MANIPULADOR DE EVENTOS BLUETOOTH ====================
void handle_ble_events() {
  while (SerialBT.available()) {
    String command = SerialBT.readStringUntil('\n');
    command.trim();
    
    if (command == "ping") {
      SerialBT.println("{\"response\":\"pong\"}");
    } 
    else if (command == "status") {
      char status[200];
      snprintf(status, sizeof(status),
        "{\"status\":\"active\",\"bpm\":%d,\"spo2\":%d,\"fatigue\":%d}",
        sensor_data.bpm, sensor_data.spo2, sensor_data.fatigue_level);
      SerialBT.println(status);
    }
    else if (command == "reset_buffer") {
      buffer_index = 0;
      SerialBT.println("{\"status\":\"buffer_reset\"}");
    }
  }
}

// ==================== SETUP ====================
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n=== SMARTWATCH FADIGA v1.0 ===");
  
  // Configurar pinos
  pinMode(VIBRADOR_PIN, OUTPUT);
  pinMode(LED_STATUS_PIN, OUTPUT);
  pinMode(BUTTON_WAKE_PIN, INPUT_PULLUP);
  
  digitalWrite(VIBRADOR_PIN, LOW);
  digitalWrite(LED_STATUS_PIN, LOW);
  
  // Inicializar I2C
  Wire.begin(8, 9);  // SDA=8, SCL=9 (ESP32 S3)
  
  // Inicializar MAX30102
  init_MAX30102();
  
  // Inicializar Bluetooth
  if (!SerialBT.begin("SmartWatch_Fadiga")) {
    Serial.println("[ERROR] Falha ao inicializar Bluetooth!");
  } else {
    Serial.println("[OK] Bluetooth iniciado!");
  }
  
  // Inicializar EEPROM
  EEPROM.begin(EEPROM_SIZE);
  
  Serial.println("[OK] Sistema pronto!");
  digitalWrite(LED_STATUS_PIN, HIGH);
  delay(500);
  digitalWrite(LED_STATUS_PIN, LOW);
}

// ==================== LOOP PRINCIPAL ====================
void loop() {
  // Verificar conexão Bluetooth
  ble_connected = SerialBT.hasClient();
  
  // Ler dados biométricos
  read_biometric_data();
  
  // Armazenar em buffer
  add_to_buffer();
  
  // Debug serial
  Serial.print("[DATA] BPM:");
  Serial.print(sensor_data.bpm);
  Serial.print(" SpO2:");
  Serial.print(sensor_data.spo2);
  Serial.print("% Temp:");
  Serial.print(sensor_data.temperature, 1);
  Serial.println("°C");
  
  // Análise de fadiga a cada 10 segundos
  static uint32_t last_analysis = 0;
  if (millis() - last_analysis > 10000) {
    last_analysis = millis();
    analyze_fatigue();
    
    Serial.print("[FADIGA] Nível: ");
    Serial.print(sensor_data.fatigue_level);
    Serial.print("/100 | Risco: ");
    Serial.println(current_analysis.risk_level);
  }
  
  // Enviar dados via Bluetooth
  send_ble_data();
  
  // Sincronizar com Redis
  sync_with_redis();
  
  // Lidar com eventos Bluetooth
  handle_ble_events();
  
  // Alertas de vibração
  if (current_analysis.risk_level == 1) {
    trigger_vibration_alert(0);
  } else if (current_analysis.risk_level == 2) {
    trigger_vibration_alert(1);
  }
  
  // Otimizar consumo de energia
  optimize_power_consumption();
  
  delay(1000);  // Leitura a cada 1 segundo
}
