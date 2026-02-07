from modules.otimizador.etapa1_seo import prompt_etapa1
from modules.otimizador.etapa1_5_analise_cv import prompt_etapa1_5
from modules.otimizador.etapa2_interrogatorio import prompt_etapa2
from modules.otimizador.etapa3_curadoria import prompt_etapa3
from modules.otimizador.etapa4_engenharia import prompt_etapa4
from modules.otimizador.etapa5_validacao import prompt_etapa5
from modules.otimizador.etapa6_arquivo import prompt_etapa6
from modules.otimizador.etapa7_exportacao import prompt_etapa7
import streamlit as st

def processar_modulo_otimizador(prompt):
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    etapa = st.session_state.get('etapa_modulo')

    if etapa == 'AGUARDANDO_INICIAR':
        if prompt.lower().strip() in ['iniciar', 'começar', 'comecar', 'ok', 'sim', 'vamos', 'start']:
            st.session_state.etapa_modulo = 'ETAPA_1_SEO'
            return prompt_etapa1(cargo)
        return None

    if etapa == 'AGUARDANDO_OK':
        if prompt.lower().strip() in ['ok', 'começar', 'comecar', 'iniciar', 'sim', 'vamos', 'start']:
            st.session_state.etapa_modulo = 'ETAPA_1_SEO'
            return prompt_etapa1(cargo)
        return None

    if etapa == 'AGUARDANDO_OK_KEYWORDS':
        # After showing keywords, user says OK to continue
        if any(word in prompt.lower() for word in ['ok', 'continuar', 'sim', 'perfeito', 'ótimo', 'otimo', 'vamos']):
            st.session_state.etapa_modulo = 'ETAPA_2'
            return prompt_etapa2()
        return None

    if etapa == 'ETAPA_1_SEO':
        # Automatically generate ETAPA 1 prompt on first entry
        return prompt_etapa1(cargo)

    if etapa == 'ETAPA_1':
        # Check if keywords were collected (from gaps interactive or other source)
        keywords_preenchidas = st.session_state.get('keywords_preenchidas', {})
        keywords_selecionadas = st.session_state.get('keywords_selecionadas', [])
        
        # If we have keywords, move to ETAPA_1.5 for CV analysis
        if keywords_preenchidas or keywords_selecionadas:
            # Prepare list of keywords from either source
            if keywords_preenchidas:
                keywords_list = list(keywords_preenchidas.keys())
            else:
                keywords_list = keywords_selecionadas
            
            st.session_state.etapa_modulo = 'ETAPA_1_5'
            return prompt_etapa1_5(cargo, keywords_list)
        elif len(prompt) > 10:
            # Original behavior: move to ETAPA_2 if no keywords flow
            st.session_state.etapa_modulo = 'ETAPA_2'
            return prompt_etapa2()
        return None

    if etapa == 'ETAPA_1_5':
        # User reviewed CV analysis, move to ETAPA_2 if they say continue
        if "continuar" in prompt.lower():
            st.session_state.etapa_modulo = 'ETAPA_2'
            return prompt_etapa2()
        return None  # Wait for user to say continue

    if etapa == 'ETAPA_2':
        if len(prompt) > 30:
            st.session_state.etapa_modulo = 'ETAPA_3'
            return prompt_etapa3()
        return None

    if etapa == 'ETAPA_3':
        if len(prompt) > 20:
            st.session_state.etapa_modulo = 'ETAPA_4'
            return prompt_etapa4()
        return None

    if etapa == 'ETAPA_4':
        st.session_state.etapa_modulo = 'ETAPA_5'
        return prompt_etapa5()

    if etapa == 'ETAPA_5':
        if any(word in prompt.lower() for word in ['arquivo', 'ok', 'aprovado', 'aprovei', 'sim', 'perfeito', 'ótimo', 'otimo', 'exportar']):
            st.session_state.etapa_modulo = 'ETAPA_6'
            return prompt_etapa6(cargo)
        return None

    if etapa == 'ETAPA_6':
        st.session_state.etapa_modulo = 'ETAPA_7'
        st.session_state.modulo_ativo = None
        return prompt_etapa7()

    return None
