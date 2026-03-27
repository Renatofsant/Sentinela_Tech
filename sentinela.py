import streamlit as st
import serial
import time
import pywhatkit as kit
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Sentinela Tech", page_icon="🛡️", layout="wide")

st.title("🛡️ Sentinela Tech: Monitoramento Inteligente")
st.markdown(f"**Professor:** Renato Santos | **Turma:** 3002 | **Projeto:** Proteção Maria da Penha")

# --- CONEXÃO COM ARDUINO ---
if 'arduino' not in st.session_state:
    try:
        # Lembre-se de verificar se a porta é COM3 ou outra no seu PC
        st.session_state.arduino = serial.Serial('COM8', 9600, timeout=0.1)
        st.success("✅ Sistema de Sensores (Botão + Som) Conectado!")
    except:
        st.error("⚠️ Sensores não detectados. Verifique o cabo USB.")

# --- INTERFACE ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📍 Mapa de Risco em Tempo Real")
    # Simulação de pontos de atenção na região
    mapa_data = pd.DataFrame({
        'lat': [-22.9068, -22.9035, -22.9080],
        'lon': [-43.1729, -43.1750, -43.1780]
    })
    st.map(mapa_data)

with col2:
    st.subheader("🚨 Painel de Controle")
    alerta_placeholder = st.empty()
    alerta_placeholder.info("🟢 Ambiente Monitorado. Aguardando sinais...")

    # Lógica de Monitoramento e Automação
    if 'arduino' in st.session_state:
        try:
            # Lê o dado serial vindo do Arduino
            comando = st.session_state.arduino.readline().decode('utf-8').strip()

            if comando:
                timestamp = time.strftime('%H:%M:%S')
                numero_emergencia = "+5521900000000"  # Ajuste para o número de teste

                if comando == "ALERTA_BOTAO":
                    alerta_placeholder.error(f"🚨 EMERGÊNCIA: Botão acionado às {timestamp}!")
                    msg = "ALERTA CRÍTICO: O botão de pânico foi acionado manualmente! Verifique a segurança imediatamente."
                    kit.sendwhatmsg_instantly(numero_emergencia, msg, wait_time=15, tab_close=True)

                elif comando == "ALERTA_SOM":
                    alerta_placeholder.warning(f"🔊 ALERTA SONORO: Grito ou impacto detectado às {timestamp}!")
                    msg = "AVISO DE SEGURANÇA: O sensor detectou um ruído de alta intensidade (possível grito ou briga). Verifique o local."
                    kit.sendwhatmsg_instantly(numero_emergencia, msg, wait_time=15, tab_close=True)

        except Exception as e:
            st.write("Erro na sincronização dos sensores.")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Configurações do Sistema")
st.sidebar.write("**Sensores Ativos:**")
st.sidebar.write("- Botão Físico (Pino 2)")
st.sidebar.write("- Sensor de Som Digital (Pino 3)")