import streamlit as st
from core.config import setup_environment
from core.state import inicializar_session_state
from ui.sidebar import renderizar_sidebar
from ui.screens.fase0_intro import fase_0_intro
from ui.screens.fase0_upload import fase_0_upload
from ui.screens.fase1_diagnostico import fase_1_diagnostico
from ui.screens.fase1_briefing import fase_1_briefing
from ui.screens.fase15_reality import fase_15_reality_check
from ui.screens.fase_analise_loading import fase_analise_loading
from ui.screens.fase_gaps_interativos import fase_gaps_interativos
from ui.screens.fase_ats_score import fase_ats_score
from ui.screens.fase_carta import fase_carta_apresentacao
from ui.screens.fase_interview import fase_prep_entrevista
from ui.screens.fase_comparador import fase_comparador_cv
from ui.chat import fase_chat

setup_environment()

st.set_page_config(
    page_title="Protocolo Nóbile",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"  # Auto-collapse on mobile
)

def inject_custom_css():
    st.markdown('''<style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    .stApp {background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%); color: #e0e0e0;} 
    .block-container {max-width: 800px !important; margin: 0 auto !important; padding: 2rem; width: 100%;} 
    h1 {color: #ffffff; text-align: center; font-size: 2rem;} 
    h2 {color: #ffffff; font-size: 1.5rem;} 
    h3 {color: #e0e0e0; font-size: 1.2rem;} 
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #16213e 0%, #0f3460 100%); border-right: 2px solid #e94560;} 
    .stButton > button {width: 100%; background: linear-gradient(90deg, #e94560 0%, #d32f4f 100%); color: white; border: none; padding: 0.75rem; font-weight: 600; border-radius: 8px; transition: all 0.3s; min-height: 48px;} 
    .stButton > button:hover {background: linear-gradient(90deg, #d32f4f 0%, #b71c3c 100%); transform: translateY(-2px);} 
    .stButton > button:disabled {background: #555555; color: #888888; transform: none;}
    
    /* Mobile-specific styles */
    @media screen and (max-width: 768px) {
        .block-container {
            padding-top: 5rem !important; /* Adicionar espaço para header do browser */
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 1rem !important;
            max-width: 100% !important;
            margin-top: 0 !important;
        }
        
        /* Ensure first element has extra spacing */
        .block-container > div:first-child {
            margin-top: 1rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.25rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        .stButton > button {
            padding: 0.875rem !important;
            font-size: 0.95rem !important;
            min-height: 52px !important;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        /* Stack columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Improve form inputs on mobile */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 0.75rem !important;
        }
        
        /* Better chat input on mobile */
        .stChatInput > div > div > textarea {
            font-size: 16px !important;
            min-height: 56px !important;
        }
        
        /* Improve info/warning boxes on mobile */
        .stInfo, .stWarning, .stSuccess, .stError {
            padding: 0.75rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Better chat messages on mobile */
        [data-testid="stChatMessage"] {
            padding: 0.75rem !important;
        }
        
        /* Better markdown rendering on mobile */
        .stMarkdown {
            font-size: 0.95rem !important;
        }
    }
    
    /* Small mobile devices */
    @media screen and (max-width: 480px) {
        .block-container {
            padding: 0.75rem !important;
        }
        
        h1 {
            font-size: 1.3rem !important;
        }
        
        h2 {
            font-size: 1.1rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
        
        .stButton > button {
            padding: 1rem !important;
            min-height: 56px !important;
        }
        
        .stMarkdown {
            font-size: 0.9rem !important;
        }
    }
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
        'FASE_ANALISE_LOADING': fase_analise_loading,
        'FASE_GAPS_INTERATIVOS': fase_gaps_interativos,
        'FASE_ATS_SCORE': fase_ats_score,
        'FASE_CARTA': fase_carta_apresentacao,
        'FASE_INTERVIEW': fase_prep_entrevista,
        'FASE_COMPARADOR': fase_comparador_cv,
        'CHAT': fase_chat
    }

    fases[st.session_state.fase]()

if __name__ == "__main__":
    main()
