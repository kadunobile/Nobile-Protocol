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
        'gaps_identificados': [],
        'cv_otimizado': "",
        'linkedin_data': {},
        'linkedin_headline': "",
        'linkedin_skills': [],
        'linkedin_about': "",
        'dados_coletados': {},
        'reality_check_resultado': None,
        'reality_ats_resultado': None,
        # Autenticação
        'authenticated': False,
        'user': None,
        # Variáveis para o novo fluxo do otimizador
        'gaps_respostas': {},
        'cv_estruturado': None,
        'dados_coleta_historico': [],
        'dados_coleta_count': 0,
        'analise_cv_completa': None,
        'gap_atual_index': 0,
        'experiencia_atual': 1,
        'total_experiencias': 3,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value