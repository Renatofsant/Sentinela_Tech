# -*- coding: utf-8 -*-
import streamlit as st
import serial
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Para rodar digite: streamlit run dashboard_sentinela_grupos.py


# --- CONFIGURAÇÃO DO NAVEGADOR (SELENIUM) ---
def iniciar_driver():
    chrome_options = Options()

    # Criamos um caminho seguro na pasta de usuário para salvar o login (Session)
    perfil_path = os.path.join(os.environ['USERPROFILE'], 'Sentinela_WhatsApp_Session')
    if not os.path.exists(perfil_path):
        os.makedirs(perfil_path)

    # Configura o Chrome para usar essa pasta e não parecer um robô básico
    chrome_options.add_argument(f"--user-data-dir={perfil_path}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Instala o driver automaticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Sentinela Tech", page_icon="🛡️", layout="wide")
st.title("🛡️ Sentinela Tech: Monitoramento Profissional")
st.markdown(f"**Professor Responsável:** Renato Santos | **Projeto:** Maria da Penha")
st.markdown("---")

# 1. Conexão com o Hardware (Arduino)
if 'arduino' not in st.session_state:
    try:
        # Ajuste para a sua porta COM8
        st.session_state.arduino = serial.Serial('COM8', 9600, timeout=0.1)
        st.success("✅ Hardware Conectado: Botão e Sensor prontos.")
    except:
        st.error("⚠️ Erro: Arduino não encontrado na COM8. Verifique o cabo ou feche a IDE do Arduino.")

# 2. Controle da Sessão do WhatsApp
if 'driver' not in st.session_state:
    st.info("👋 Olá, Renato! Antes de começar, precisamos preparar a rede de apoio.")
    if st.button("🚀 PASSO 1: Abrir e Logar no WhatsApp"):
        with st.spinner("Iniciando motor de navegação..."):
            st.session_state.driver = iniciar_driver()
            st.session_state.driver.get("https://web.whatsapp.com")
            st.warning("⚠️ Escaneie o QR Code apenas uma vez. Depois, o login ficará salvo!")
else:
    st.success("✅ SISTEMA EM VIGÍLIA: O WhatsApp já está autenticado.")
    if st.button("🔄 Reiniciar Navegador (Use se o Chrome fechar)"):
        try:
            st.session_state.driver.quit()
        except:
            pass
        del st.session_state['driver']
        st.rerun()

# --- CONFIGURAÇÕES DE DESTINO ---
# Insira os IDs dos seus grupos aqui
LISTA_GRUPOS = ["Dl9OmdFOj9KAQKSMkZJ3h7", "HzgSBu1chDU2xCz5vszs17"]

painel_alerta = st.empty()
painel_alerta.info("🔍 Monitorando sinais de emergência do Arduino...")

# --- LOOP PRINCIPAL DE DISPARO ---
if 'arduino' in st.session_state and 'driver' in st.session_state:
    driver = st.session_state.driver

    while True:
        try:
            # Lê o comando enviado pelo Arduino via Serial
            comando = st.session_state.arduino.readline().decode('utf-8', errors='ignore').strip()

            if comando == "ALERTA_BOTAO" or comando == "ALERTA_SOM":
                origem = "Botão Físico" if comando == "ALERTA_BOTAO" else "Sensor de Som"
                hora_evento = time.strftime('%H:%M:%S')

                painel_alerta.error(f"🚨 EMERGÊNCIA DETECTADA: Acionamento via {origem} às {hora_evento}!")

                # Mensagem sem acentos para garantir 100% de compatibilidade no envio
                msg = (
                    f"*ALERTA SENTINELA: EMERGÊNCIA!*"
                    f"\n\n*Origem:* {origem}"
                    f"\n*Vítima:* Maria da Silva"
                    f"\n*Local:* Colégio Estadual Maria Nazareth Cavalcanti Silva"
                    f"\n*Endereço:* Rua Barbosa, N 229 - Cascadura, Rio de Janeiro - RJ"
                    f"\n*Horário:* {hora_evento}"
                    f"\n\n_Verifique o local imediatamente ou acione a viatura mais próxima!_"
                )

                # Dispara para cada grupo da lista usando o Selenium
                for id_grupo in LISTA_GRUPOS:
                    st.toast(f"Disparando alerta para o grupo: {id_grupo}")

                    # Navega diretamente para o grupo
                    url = f"https://web.whatsapp.com/accept?code={id_grupo}"
                    driver.get(url)

                    # Espera a caixa de texto carregar por até 40 segundos (Segurança extra)
                    wait = WebDriverWait(driver, 40)
                    xpath_caixa = '//div[@contenteditable="true"][@data-tab="10"]'
                    caixa_texto = wait.until(EC.presence_of_element_located((By.XPATH, xpath_caixa)))

                    # Digita e envia com a tecla ENTER
                    caixa_texto.send_keys(msg + Keys.ENTER)
                    time.sleep(5)  # Pausa para garantir que a mensagem saiu antes de trocar de URL

                st.session_state.arduino.flushInput()
                st.toast("✅ Rede de apoio notificada com sucesso!")
                time.sleep(2)
                painel_alerta.info("🔍 Sistema rearmado. Continuando monitoramento...")

        except Exception as e:
            # Caso o navegador seja fechado manualmente, avisa no Dashboard
            st.sidebar.warning(f"Atenção: Navegador ou conexão instável.")
            break

        time.sleep(0.1)