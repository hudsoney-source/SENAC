"""
MODELO DE IA - Sistema de Detecção de Fadiga
Análise de dados biométricos para classificação de fadiga
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==================== CONSTANTES ====================

# Limiares de fadiga para classificação
FATIGUE_THRESHOLDS = {
    'low_risk': (0, 30),        # 0-30: Descansado
    'medium_risk': (31, 65),    # 31-65: Moderadamente cansado
    'high_risk': (66, 100)      # 66-100: Muito cansado
}

# Limiares biométricos normais
NORMAL_RANGES = {
    'bpm': {'min': 50, 'max': 100, 'normal': (60, 90)},
    'spo2': {'min': 92, 'normal': (95, 100)},
    'temperature': {'min': 36.5, 'max': 37.5, 'normal': (36.8, 37.2)}
}

# Pesos para cálculo de fadiga (precisam ser calibrados com dados reais)
FATIGUE_WEIGHTS = {
    'bpm_deviation': 0.25,      # Desviação de frequência cardíaca
    'spo2_reduction': 0.30,     # Redução de oxigenação
    'temperature_elevation': 0.15,  # Elevação de temperatura
    'hrv_reduction': 0.20,      # Redução de variabilidade cardíaca
    'recent_trend': 0.10        # Tendência recente
}

# ==================== CLASSE PRINCIPAL ====================

class FatigueDetectionAI:
    """
    Sistema de IA para detecção de fadiga baseado em sensores biométricos
    """
    
    def __init__(self, window_size: int = 60):
        """
        Inicializar modelo
        
        Args:
            window_size: Número de amostras para análise (padrão: 60 = 1 minuto)
        """
        self.window_size = window_size
        self.data_history = []
        self.fatigue_scores = []
        self.alerts_threshold = 70
        
    def add_reading(self, bpm: int, spo2: int, temperature: float, 
                   timestamp: datetime = None):
        """Adicionar nova leitura de sensor"""
        
        if timestamp is None:
            timestamp = datetime.now()
        
        reading = {
            'timestamp': timestamp,
            'bpm': bpm,
            'spo2': spo2,
            'temperature': temperature
        }
        
        self.data_history.append(reading)
        
        # Manter apenas as últimas N amostras
        if len(self.data_history) > self.window_size * 10:
            self.data_history = self.data_history[-self.window_size * 10:]
    
    def calculate_heart_rate_variability(self, bpm_values: List[int]) -> float:
        """
        Calcular Variabilidade da Frequência Cardíaca (HRV)
        
        HRV é indicador de saúde do sistema nervoso autônomo
        - HRV alta = repouso, relaxado
        - HRV baixa = fadiga, estresse
        
        Args:
            bpm_values: Lista de medições de BPM
        
        Returns:
            Valor de HRV (desvio padrão dos intervalos)
        """
        if len(bpm_values) < 2:
            return 0.0
        
        # Calcular intervalos entre batimentos (em ms)
        intervals = []
        for i in range(len(bpm_values) - 1):
            if bpm_values[i] > 0:
                interval = 60000 / bpm_values[i]
                intervals.append(interval)
        
        if len(intervals) < 2:
            return 0.0
        
        hrv = np.std(intervals)
        return float(hrv)
    
    def calculate_fatigue_score(self) -> Tuple[float, Dict]:
        """
        Calcular pontuação de fadiga (0-100)
        
        Returns:
            Tupla (score, detalhes_componentes)
        """
        
        if len(self.data_history) < 10:
            return 0.0, {'reason': 'insufficient_data'}
        
        # Extrair dados recentes
        recent_data = self.data_history[-self.window_size:]
        df = pd.DataFrame(recent_data)
        
        # Componente 1: Desvio de BPM
        bpm_values = df['bpm'].values[df['bpm'] > 0]
        
        if len(bpm_values) > 0:
            avg_bpm = np.mean(bpm_values)
            normal_bpm = np.mean(NORMAL_RANGES['bpm']['normal'])
            
            # Calcular desvio em relação ao normal
            bpm_deviation = abs(avg_bpm - normal_bpm) / normal_bpm
            bpm_component = min(100, bpm_deviation * 100)
            
            # Taquicardia é mais indicativa de fadiga
            if avg_bpm > NORMAL_RANGES['bpm']['max']:
                bpm_component *= 1.5
        else:
            bpm_component = 0
        
        # Componente 2: Redução de SpO2
        spo2_values = df['spo2'].values[df['spo2'] > 0]
        
        if len(spo2_values) > 0:
            avg_spo2 = np.mean(spo2_values)
            normal_spo2 = np.mean(NORMAL_RANGES['spo2']['normal'])
            
            # Hipoxemia indicativa de fadiga
            spo2_component = (normal_spo2 - avg_spo2) * 5  # Multiplica por 5 para peso
            spo2_component = max(0, min(100, spo2_component))
        else:
            spo2_component = 0
        
        # Componente 3: Temperatura elevada
        temp_values = df['temperature'].values
        avg_temp = np.mean(temp_values)
        
        # Febrícula ou elevação ligeira = fadiga/inflamação
        if avg_temp > 37.0:
            temp_component = (avg_temp - 37.0) * 50  # 1°C acima = 50 pontos
            temp_component = min(100, temp_component)
        else:
            temp_component = 0
        
        # Componente 4: Variabilidade cardíaca reduzida
        if len(bpm_values) > 5:
            hrv = self.calculate_heart_rate_variability(bpm_values)
            # HRV reduzida (< 20ms) indica fadiga
            if hrv < 20:
                hrv_component = (20 - hrv) * 2
            else:
                hrv_component = 0
        else:
            hrv_component = 0
        
        # Componente 5: Tendência recente (piorando?)
        if len(self.fatigue_scores) >= 5:
            recent_scores = self.fatigue_scores[-5:]
            trend = np.polyfit(range(5), recent_scores, 1)[0]
            
            # Se tendência positiva = piorando
            trend_component = max(0, trend * 10) if trend > 0 else 0
        else:
            trend_component = 0
        
        # Calcular score ponderado
        components = {
            'bpm_deviation': float(bpm_component),
            'spo2_reduction': float(spo2_component),
            'temperature_elevation': float(temp_component),
            'hrv_reduction': float(hrv_component),
            'recent_trend': float(trend_component)
        }
        
        weighted_score = (
            components['bpm_deviation'] * FATIGUE_WEIGHTS['bpm_deviation'] +
            components['spo2_reduction'] * FATIGUE_WEIGHTS['spo2_reduction'] +
            components['temperature_elevation'] * FATIGUE_WEIGHTS['temperature_elevation'] +
            components['hrv_reduction'] * FATIGUE_WEIGHTS['hrv_reduction'] +
            components['recent_trend'] * FATIGUE_WEIGHTS['recent_trend']
        )
        
        final_score = float(np.clip(weighted_score, 0, 100))
        
        components['final_score'] = final_score
        components['avg_bpm'] = float(avg_bpm)
        components['avg_spo2'] = float(avg_spo2)
        components['avg_temp'] = float(avg_temp)
        
        self.fatigue_scores.append(final_score)
        
        return final_score, components
    
    def classify_risk_level(self, fatigue_score: float) -> Dict:
        """
        Classificar nível de risco baseado na pontuação
        
        Args:
            fatigue_score: Pontuação de fadiga (0-100)
        
        Returns:
            Dicionário com classificação e recomendações
        """
        
        if fatigue_score < FATIGUE_THRESHOLDS['low_risk'][1]:
            risk_level = 0
            classification = "BAIXO RISCO"
            color = "GREEN"
            recommendation = "✓ Você está bem descansado. Continue monitorando!"
            
        elif fatigue_score < FATIGUE_THRESHOLDS['medium_risk'][1]:
            risk_level = 1
            classification = "RISCO MODERADO"
            color = "YELLOW"
            recommendation = "⚠ Fadiga detectada. Recomenda-se descanso em breve."
            
        else:
            risk_level = 2
            classification = "RISCO ALTO"
            color = "RED"
            recommendation = "🚨 ALERTA: Fadiga severa! Procure descansar IMEDIATAMENTE."
        
        return {
            'risk_level': risk_level,
            'classification': classification,
            'color': color,
            'score': fatigue_score,
            'recommendation': recommendation
        }
    
    def generate_insights(self) -> Dict:
        """Gerar insights automáticos do histórico"""
        
        if len(self.data_history) < 30:
            return {'status': 'insufficient_data'}
        
        df = pd.DataFrame(self.data_history)
        
        # Análise de padrões
        bpm_values = df['bpm'].values[df['bpm'] > 0]
        spo2_values = df['spo2'].values[df['spo2'] > 0]
        
        insights = {
            'total_readings': len(df),
            'duration_minutes': (df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]).total_seconds() / 60,
            
            'heart_rate': {
                'average': float(np.mean(bpm_values)) if len(bpm_values) > 0 else 0,
                'peak': int(np.max(bpm_values)) if len(bpm_values) > 0 else 0,
                'minimum': int(np.min(bpm_values)) if len(bpm_values) > 0 else 0
            },
            
            'oxygenation': {
                'average': float(np.mean(spo2_values)) if len(spo2_values) > 0 else 0,
                'minimum': int(np.min(spo2_values)) if len(spo2_values) > 0 else 0
            },
            
            'temperature': {
                'average': float(np.mean(df['temperature'].values)),
                'maximum': float(np.max(df['temperature'].values))
            },
            
            'fatigue_trend': self._calculate_trend(),
            'recommendations': self._generate_recommendations()
        }
        
        return insights
    
    def _calculate_trend(self) -> str:
        """Calcular tendência de fadiga"""
        
        if len(self.fatigue_scores) < 5:
            return "insufficient_data"
        
        recent = np.array(self.fatigue_scores[-5:])
        older = np.array(self.fatigue_scores[-10:-5])
        
        avg_recent = np.mean(recent)
        avg_older = np.mean(older)
        
        change = ((avg_recent - avg_older) / avg_older * 100) if avg_older > 0 else 0
        
        if change > 10:
            return "deteriorating"  # Piorando
        elif change < -10:
            return "improving"  # Melhorando
        else:
            return "stable"  # Estável
    
    def _generate_recommendations(self) -> List[str]:
        """Gerar recomendações baseadas nos dados"""
        
        recommendations = []
        
        if len(self.data_history) == 0:
            return ["Sem dados para análise"]
        
        df = pd.DataFrame(self.data_history)
        bpm_values = df['bpm'].values[df['bpm'] > 0]
        spo2_values = df['spo2'].values[df['spo2'] > 0]
        
        # Análise de BPM
        if len(bpm_values) > 0:
            avg_bpm = np.mean(bpm_values)
            
            if avg_bpm > 110:
                recommendations.append("❌ Frequência cardíaca elevada detectada. Reduza estresse/atividade.")
            elif avg_bpm < 50:
                recommendations.append("⚠️ Frequência cardíaca muito baixa. Verifique dispositivo.")
        
        # Análise de SpO2
        if len(spo2_values) > 0:
            avg_spo2 = np.mean(spo2_values)
            
            if avg_spo2 < 93:
                recommendations.append("🫁 Oxigenação baixa. Procure melhor ventilação/altitude.")
        
        # Análise de fadiga
        if len(self.fatigue_scores) > 0:
            latest_fatigue = self.fatigue_scores[-1]
            
            if latest_fatigue > 70:
                recommendations.append("😴 Fadiga alta detectada. Recomenda-se descanso urgente!")
                recommendations.append("💤 Procure dormir 7-8 horas regularmente.")
                recommendations.append("🧘 Considere técnicas de relaxamento (meditação, yoga).")
            elif latest_fatigue > 50:
                recommendations.append("⏰ Considere uma pausa de 15-20 minutos.")
                recommendations.append("💧 Mantenha-se hidratado.")
        
        # Padrões detectados
        if len(self.fatigue_scores) > 10:
            trend = self._calculate_trend()
            
            if trend == "deteriorating":
                recommendations.append("📊 Fadiga está aumentando. Procure descanso antecipado.")
            elif trend == "improving":
                recommendations.append("✅ Fadiga está diminuindo. Continue com estratégia atual.")
        
        return recommendations if recommendations else ["Status normal - continue monitorando"]
    
    def get_all_metrics(self) -> Dict:
        """Retornar todos os indicadores calculados"""
        
        fatigue_score, components = self.calculate_fatigue_score()
        risk_info = self.classify_risk_level(fatigue_score)
        insights = self.generate_insights()
        
        return {
            'fatigue_score': fatigue_score,
            'components': components,
            'risk_info': risk_info,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        }


# ==================== FUNÇÕES AUXILIARES ====================

def simulate_fatigue_progression():
    """
    Simular progressão de fadiga para testes
    Retorna dados realistas de sensores ao longo de um período
    """
    
    ai = FatigueDetectionAI(window_size=60)
    
    # Simular 180 minutos (3 horas) de dados
    for minute in range(180):
        # Simular aumento gradual de fadiga
        base_time = minute / 180  # 0 a 1
        
        # BPM: começa em 70, vai para 90+ com fadiga
        bpm = int(70 + base_time * 30 + np.random.normal(0, 5))
        
        # SpO2: começa em 98%, reduz ligeiramente com fadiga
        spo2 = int(98 - base_time * 5 + np.random.normal(0, 1))
        
        # Temperatura: começa em 37.0, sobe ligeiramente
        temperature = 37.0 + base_time * 0.5 + np.random.normal(0, 0.2)
        
        timestamp = datetime.now() - timedelta(minutes=180-minute)
        
        ai.add_reading(bpm, spo2, temperature, timestamp)
    
    return ai

    
# ==================== TESTE E DEMONSTRAÇÃO ====================

if __name__ == "__main__":
    print("=" * 60)
    print("SISTEMA DE DETECÇÃO DE FADIGA - IA")
    print("=" * 60)
    
    # Simular dados
    print("\n📊 Gerando dados de teste...")
    ai_system = simulate_fatigue_progression()
    
    # Obter métricas
    metrics = ai_system.get_all_metrics()
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE FADIGA")
    print("=" * 60)
    
    print(f"\n📈 Pontuação de Fadiga: {metrics['fatigue_score']:.1f}/100")
    
    print(f"\n🎯 Classificação: {metrics['risk_info']['classification']}")
    print(f"   Recomendação: {metrics['risk_info']['recommendation']}")
    
    print(f"\n❤️  Frequência Cardíaca Média: {metrics['components']['avg_bpm']:.0f} BPM")
    print(f"   Desvio: {metrics['components']['bpm_deviation']:.1f} pts")
    
    print(f"\n🫁 Oxigenação Média: {metrics['components']['avg_spo2']:.0f}%")
    print(f"   Redução: {metrics['components']['spo2_reduction']:.1f} pts")
    
    print(f"\n🌡️  Temperatura Média: {metrics['components']['avg_temp']:.1f}°C")
    print(f"   Elevação: {metrics['components']['temperature_elevation']:.1f} pts")
    
    print(f"\n📊 Insights:")
    insights = metrics['insights']
    print(f"   • Total de leituras: {insights['total_readings']}")
    print(f"   • Duração: {insights['duration_minutes']:.0f} minutos")
    print(f"   • HR Mín/Máx: {insights['heart_rate']['minimum']}/{insights['heart_rate']['peak']} BPM")
    print(f"   • SpO2 Mín: {insights['oxygenation']['minimum']}%")
    print(f"   • Tendência: {insights['fatigue_trend'].upper()}")
    
    print(f"\n💡 Recomendações:")
    for i, rec in enumerate(insights['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    print("\n" + "=" * 60)
