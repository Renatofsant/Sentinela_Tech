# 🛡️ Sentinela Tech: Sistema de Proteção Inteligente

Projeto desenvolvido para a Feira de Ciências, focado na aplicação de tecnologia para a segurança feminina e apoio à Lei Maria da Penha.

## 🚀 Sobre o Projeto
O **Sentinela Tech** é um sistema híbrido que combina hardware (Arduino) e software (Python/Selenium) para oferecer uma rede de socorro imediata. O sistema monitora o ambiente e, em caso de emergência, dispara alertas automáticos para grupos de apoio no WhatsApp.

## 🛠️ Tecnologias Utilizadas
* **Hardware:** Arduino Uno, Sensor de Som, Botão de Pânico.
* **Linguagem:** Python 3.x
* **Bibliotecas:** * `Streamlit`: Interface visual do Dashboard.
  * `Selenium`: Automação do navegador para envio de mensagens.
  * `PySerial`: Comunicação entre o PC e o Arduino.

## 📋 Como Funciona
1. O **Arduino** monitora picos de ruído ou acionamento manual.
2. O **Python** recebe o sinal via porta Serial.
3. O **Selenium** assume o controle do navegador já autenticado.
4. Mensagens de alerta são enviadas sequencialmente para múltiplos grupos cadastrados.

---
**Professor Responsável:** Renato Santos
**Turmas:** 1º e 3º Ano do Ensino Médio