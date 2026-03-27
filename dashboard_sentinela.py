# -*- coding: utf-8 -*-
import streamlit as st
import serial
import time
import pywhatkit as kit

#Para rodar digite: streamlit run dashboard_sentinela.py

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Sentinela Tech", page_icon="🛡️", layout="wide")

st.title("🛡️ Sentinela Tech: Sistema de Proteção Inteligente")
st.markdown(f"**Professor Responsável:** Renato Santos | **Projeto:** Maria da Penha | **Status:** Monitoramento Ativo")
st.markdown("---")

# --- CONEXÃO COM O ARDUINO (PORTA COM8) ---
if 'arduino' not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM8', 9600, timeout=0.1)
        st.success("✅ Hardware Conectado: Botão e Sensor de Som operacionais.")
    except Exception as e:
        st.error("⚠️ Erro de Conexão: Verifique se o Monitor Serial da IDE do Arduino está FECHADO.")

# --- CONFIGURAÇÕES DE ENVIO ---
ID_GRUPO = "Dl9OmdFOj9KAQKSMkZJ3h7"

painel_alerta = st.empty()
painel_alerta.info("🟢 Sistema em vigília. Aguardando sinais dos sensores...")

# --- LOOP DE MONITORAMENTO ---
if 'arduino' in st.session_state:
    while True:
        try:
            # Lemos a linha e garantimos que o Python entenda como UTF-8
            comando = st.session_state.arduino.readline().decode('utf-8', errors='ignore').strip()

            if comando:
                hora_evento = time.strftime('%H:%M:%S')

                if comando == "ALERTA_BOTAO":
                    painel_alerta.error(f"🚨 EMERGÊNCIA: Botão de Pânico acionado às {hora_evento}!")

                    # Usamos strings simples e garantimos que o pywhatkit as receba bem
                    msg = f"ALERTA SENTINELA: O botao fisico de emergencia foi acionado! Horario: {hora_evento}."

                    # O segredo: wait_time um pouco maior ajuda o navegador a processar os caracteres
                    kit.sendwhatmsg_to_group_instantly(ID_GRUPO, msg, wait_time=20, tab_close=True)
                    st.toast("Mensagem de socorro enviada!")
                    time.sleep(2)

                elif comando == "ALERTA_SOM":
                    painel_alerta.warning(f"🔊 ALERTA ACÚSTICO: Ruído crítico detectado às {hora_evento}!")

                    msg = f"AVISO SENTINELA: O sensor detectou um ruido de alta intensidade. Verifique o local! Horario: {hora_evento}."

                    kit.sendwhatmsg_to_group_instantly(ID_GRUPO, msg, wait_time=20, tab_close=True)
                    st.toast("Alerta sonoro enviado!")
                    time.sleep(2)

        except Exception as e:
            st.sidebar.error(f"Conexão perdida: {e}")
            break

        time.sleep(0.1)