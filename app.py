import streamlit as st
from core.config import setup_environment
from core.state import inicializar_session_state
from ui.sidebar import renderizar_sidebar
from ui.screens.fase0_intro import fase_0_intro
from ui.screens.fase0_upload import fase_0_upload
from ui.screens.fase1_diagnostico import fase_1_diagnostico
from ui.screens.fase1_briefing import fase_1_briefing
from ui.screens.fase15_reality import fase_15_reality_check
from ui.chat import fase_chat

setup_environment()

st.set_page_config(
    page_title="Protocolo Nóbile",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown('''<style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    .stApp {background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%); color: #e0e0e0;} 
    .block-container {max-width: 800px !important; margin: 0 auto !important; padding: 2rem;} 
    h1 {color: #ffffff; text-align: center; font-size: 2rem;} 
    h2 {color: #ffffff; font-size: 1.5rem;} 
    h3 {color: #e0e0e0; font-size: 1.2rem;} 
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #16213e 0%, #0f3460 100%); border-right: 2px solid #e94560;} 
    .stButton > button {width: 100%; background: linear-gradient(90deg, #e94560 0%, #d32f4f 100%); color: white; border: none; padding: 0.75rem; font-weight: 600; border-radius: 8px; transition: all 0.3s;} 
    .stButton > button:hover {background: linear-gradient(90deg, #d32f4f 0%, #b71c3c 100%); transform: translateY(-2px);} 
    .stButton > button:disabled {background: #555555; color: #888888; transform: none;}
    </style>''', unsafe_allow_html=True)

def main():
    inject_custom_css()
    inicializar_session_state()

    if st.session_state.fase not in ['FASE_0_INTRO', 'FASE_0_UPLOAD']:
        renderizar_sidebar()

    fases = {
        'FASE_0_INTRO': fase_0_intro,
        'FASE_0_UPLOAD': fase_0_upload,
        'FASE_1_DIAGNOSTICO': fase_1_diagnostico,
        'FASE_1_BRIEFING': fase_1_briefing,
        'FASE_15_REALITY': fase_15_reality_check,
        'CHAT': fase_chat
    }

    fases[st.session_state.fase]()

if __name__ == "__main__":
    main()
