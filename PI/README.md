# Projeto Integrador - Sistema de Deteccao de Fadiga

Projeto voltado ao monitoramento de sinais fisiologicos com ESP32, analise de fadiga e documentacao da arquitetura da solucao.

## Principais arquivos

- `smartwatch_fadiga.ino`: firmware do dispositivo
- `fatigue_ai.py`: prototipo de processamento e inferencia
- `docker-compose.yml`: infraestrutura de apoio para servicos locais
- `QUICK_START.md`: passos iniciais para subir o projeto
- `INDEX.md`: indice mestre da documentacao
- `SYSTEM_ARCHITECTURE.md`: visao de arquitetura
- `REDIS_ARCHITECTURE.md`: organizacao dos dados no Redis

## Objetivo

O sistema busca identificar sinais de fadiga a partir de sensores embarcados, gerar alertas e organizar os dados para analise posterior.

## Como comecar

1. Leia `QUICK_START.md`.
2. Verifique as conexoes em `HARDWARE_CONNECTIONS.md`.
3. Faca o upload do firmware em `smartwatch_fadiga.ino`.
4. Consulte a arquitetura e os fluxos antes de integrar backend ou dashboard.

## Conteudo do diretorio

- Documentacao tecnica
- Especificacoes de dashboard e app mobile
- Guia de implementacao
- Resumo de entregaveis
- Observacoes finais do projeto
