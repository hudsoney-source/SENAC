# Mapa da Pinagem da ESP32

## Pinagem da ESP32

| GPIO  | Função Principal                  | Funções Alternativas                  |
|-------|-----------------------------------|---------------------------------------|
| GPIO0 | Boot (modo de inicialização)     | GPIO                                 |
| GPIO1 | UART TX                          | Comunicação Serial                   |
| GPIO2 | GPIO                             | PWM, I2C SDA                         |
| GPIO3 | UART RX                          | Comunicação Serial                   |
| GPIO4 | GPIO                             | PWM, ADC, I2C SDA                    |
| GPIO5 | GPIO                             | PWM, ADC, I2C SCL                    |
| GPIO6 | Reservado para Flash             | Não utilizar                         |
| GPIO7 | Reservado para Flash             | Não utilizar                         |
| GPIO8 | Reservado para Flash             | Não utilizar                         |
| GPIO9 | Reservado para Flash             | Não utilizar                         |
| GPIO10| Reservado para Flash             | Não utilizar                         |
| GPIO11| Reservado para Flash             | Não utilizar                         |
| GPIO12| GPIO                             | PWM, ADC                             |
| GPIO13| GPIO                             | PWM, ADC                             |
| GPIO14| GPIO                             | PWM, ADC                             |
| GPIO15| GPIO                             | PWM, ADC                             |
| GPIO16| GPIO                             | PWM                                  |
| GPIO17| GPIO                             | PWM                                  |
| GPIO18| GPIO                             | PWM, SPI SCK                         |
| GPIO19| GPIO                             | PWM, SPI MISO                        |
| GPIO21| I2C SDA                          | GPIO                                 |
| GPIO22| I2C SCL                          | GPIO                                 |
| GPIO23| GPIO                             | PWM, SPI MOSI                        |
| GPIO25| DAC1                             | PWM, ADC                             |
| GPIO26| DAC2                             | PWM, ADC                             |
| GPIO27| GPIO                             | PWM, ADC                             |
| GPIO32| ADC1 CH4                         | PWM                                  |
| GPIO33| ADC1 CH5                         | PWM                                  |
| GPIO34| ADC1 CH6                         | Somente entrada                      |
| GPIO35| ADC1 CH7                         | Somente entrada                      |
| GPIO36| ADC1 CH0                         | Somente entrada                      |
| GPIO39| ADC1 CH3                         | Somente entrada                      |

## Notas Importantes
- **GPIO6 a GPIO11**: Reservados para o Flash interno, não devem ser utilizados.
- **DAC**: GPIO25 e GPIO26 podem ser usados como conversores digital-analógico.
- **ADC**: GPIO32 a GPIO39 são canais ADC, usados para leitura de sinais analógicos.
- **PWM**: Todas as portas GPIO (exceto as reservadas) podem ser usadas para PWM.
- **I2C**: GPIO21 (SDA) e GPIO22 (SCL) são os pinos padrão para comunicação I2C.
- **SPI**: GPIO18 (SCK), GPIO19 (MISO), GPIO23 (MOSI) e GPIO5 (CS) são usados para SPI.
- **UART**: GPIO1 (TX) e GPIO3 (RX) são os pinos padrão para comunicação serial.