import streamlit as st

def inicializar_session_state():
    defaults = {
        'fase': 'FASE_0_INTRO',
        'cv_texto': None,
        'perfil': {},
        'mensagens': [],
        'analise_inicial': None,
        'openai_client': None,
        'modulo_ativo': None,
        'etapa_modulo': None,
        'force_scroll_top': False,
        # Novas variáveis para o fluxo de otimização
        'score_ats_inicial': None,
        'score_ats_final': None,
        'gaps_alvo': [],
        'cv_otimizado': "",
        'linkedin_data': {},
        'linkedin_headline': "",
        'linkedin_skills': [],
        'linkedin_about': "",
        'dados_coletados': {},
        'reality_check_resultado': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value