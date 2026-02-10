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
        # ATS e Reality Check
        'score_ats_inicial': None,
        'score_ats_final': None,
        'reality_check_resultado': None,
        'reality_ats_resultado': None,
        # Gaps (gaps_alvo e gaps_identificados são mantidos separados por compatibilidade com diferentes fases)
        'gaps_alvo': [],
        'gaps_identificados': [],
        'gaps_respostas': {},
        # CV Otimizado e LinkedIn
        'cv_otimizado': "",
        'cv_estruturado': None,
        'linkedin_data': {},
        'linkedin_headline': "",
        'linkedin_skills': [],
        'linkedin_about': "",
        # Coleta de dados do otimizador
        'dados_coletados': {},
        'dados_coleta_historico': [],
        'dados_coleta_count': 0,
        'analise_cv_completa': None,
        # Controle de fluxo do otimizador
        'gap_atual_index': 0,
        'experiencia_atual': 1,
        'total_experiencias': 3,
        # Trigger flags para auto-triggers do chat
        'etapa_0_diagnostico_triggered': False,
        'etapa_0_gap_triggered': False,
        'etapa_0_resumo_triggered': False,
        'etapa_1_triggered': False,
        'etapa_1_coleta_focada_triggered': False,
        'etapa_6_linkedin_triggered': False,
        'checkpoint_1_triggered': False,
        'etapa_2_reescrita_triggered': False,
        'etapa_2_final_triggered': False,
        # Autenticação
        'authenticated': False,
        'user': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value