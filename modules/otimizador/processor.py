from modules.otimizador.etapa1_seo import prompt_etapa1
from modules.otimizador.etapa1_5_analise_cv import prompt_etapa1_5
from modules.otimizador.etapa2_interrogatorio import prompt_etapa2
from modules.otimizador.etapa3_curadoria import prompt_etapa3
from modules.otimizador.etapa4_engenharia import prompt_etapa4
from modules.otimizador.etapa5_validacao import prompt_etapa5
from modules.otimizador.etapa6_arquivo import prompt_etapa6
from modules.otimizador.etapa7_exportacao import prompt_etapa7
# Novas etapas do fluxo otimizado
from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico
from modules.otimizador.etapa1_coleta_focada import prompt_etapa1_coleta_focada
from modules.otimizador.checkpoint_validacao import prompt_checkpoint_validacao
from modules.otimizador.etapa2_reescrita_progressiva import prompt_etapa2_reescrita_progressiva, prompt_etapa2_reescrita_final
from modules.otimizador.etapa6_otimizacao_linkedin import prompt_etapa6_otimizacao_linkedin
import streamlit as st

# Configuration constants
DEFAULT_MAX_EXPERIENCES = 3  # Default number of experiences to optimize


def processar_modulo_otimizador(prompt):
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    etapa = st.session_state.get('etapa_modulo')
    
    # ========== NOVO FLUXO OTIMIZADO ==========
    
    # ETAPA 0: DIAGNÓSTICO
    if etapa == 'ETAPA_0_DIAGNOSTICO':
        return prompt_etapa0_diagnostico()
    
    if etapa == 'AGUARDANDO_OK_DIAGNOSTICO':
        if any(word in prompt.lower() for word in ['ok', 'continuar', 'sim', 'perfeito', 'aprovar', 'vamos']):
            st.session_state.etapa_modulo = 'ETAPA_1_COLETA_FOCADA'
            return prompt_etapa1_coleta_focada()
        return None
    
    # ETAPA 1: COLETA FOCADA
    if etapa == 'ETAPA_1_COLETA_FOCADA':
        return prompt_etapa1_coleta_focada()
    
    if etapa == 'AGUARDANDO_DADOS_COLETA':
        if any(word in prompt.lower() for word in ['continuar', 'pronto', 'concluído', 'concluido', 'finalizado']):
            # Salvar dados coletados
            st.session_state.dados_coletados = {'raw_response': prompt}
            st.session_state.etapa_modulo = 'CHECKPOINT_1_VALIDACAO'
            return prompt_checkpoint_validacao()
        return None
    
    # CHECKPOINT 1: VALIDAÇÃO
    if etapa == 'CHECKPOINT_1_VALIDACAO':
        return prompt_checkpoint_validacao()
    
    if etapa == 'AGUARDANDO_APROVACAO_VALIDACAO':
        if any(word in prompt.lower() for word in ['aprovar', 'aprovado', 'ok', 'correto', 'sim', 'perfeito']):
            # Iniciar reescrita progressiva
            st.session_state.etapa_modulo = 'ETAPA_2_REESCRITA_EXP_1'
            st.session_state.experiencia_atual = 1
            return prompt_etapa2_reescrita_progressiva(1)
        return None
    
    # ETAPA 2: REESCRITA PROGRESSIVA (múltiplas experiências)
    if etapa and etapa.startswith('ETAPA_2_REESCRITA_EXP_'):
        exp_num = int(etapa.split('_')[-1])
        return prompt_etapa2_reescrita_progressiva(exp_num)
    
    if etapa and etapa.startswith('AGUARDANDO_APROVACAO_EXP_'):
        exp_num = int(etapa.split('_')[-1])
        if any(word in prompt.lower() for word in ['próxima', 'proxima', 'próximo', 'proximo', 'continuar', 'aprovar', 'ok']):
            # Verificar se há mais experiências
            max_exp = st.session_state.get('total_experiencias', DEFAULT_MAX_EXPERIENCES)
            if exp_num < max_exp:
                st.session_state.etapa_modulo = f'ETAPA_2_REESCRITA_EXP_{exp_num + 1}'
                return prompt_etapa2_reescrita_progressiva(exp_num + 1)
            else:
                # Finalizar reescritas
                st.session_state.etapa_modulo = 'ETAPA_2_REESCRITA_FINAL'
                return prompt_etapa2_reescrita_final()
        return None
    
    if etapa == 'ETAPA_2_REESCRITA_FINAL':
        return prompt_etapa2_reescrita_final()
    
    if etapa == 'AGUARDANDO_CONTINUAR_CHECKPOINT2':
        if any(word in prompt.lower() for word in ['continuar', 'ok', 'aprovar', 'sim']):
            # TODO: Salvar CV otimizado das mensagens reescritas
            # Por enquanto, marcar para gerar na fase de validação
            if not st.session_state.get('cv_otimizado'):
                # Placeholder - o CV otimizado deveria ser construído das reescritas
                st.session_state.cv_otimizado = st.session_state.get('cv_texto', '')
            st.session_state.fase = 'FASE_VALIDACAO_SCORE_ATS'
            return None  # Vai para tela de validação
        return None
    
    # ETAPA 6: OTIMIZAÇÃO LINKEDIN (novo fluxo)
    if etapa == 'ETAPA_6_LINKEDIN':
        return prompt_etapa6_otimizacao_linkedin()
    
    if etapa == 'AGUARDANDO_ESCOLHA_HEADLINE':
        # Usuário escolhe headline A, B ou C
        if any(letra in prompt.upper() for letra in ['A', 'B', 'C']):
            # Salvar escolha (simplificado)
            st.session_state.linkedin_headline_escolhida = prompt.upper().strip()[0]
            st.session_state.etapa_modulo = 'AGUARDANDO_OK_SKILLS'
            return None  # Continua no mesmo prompt
        return None
    
    if etapa == 'AGUARDANDO_OK_SKILLS':
        if any(word in prompt.lower() for word in ['ok', 'sim', 'continuar', 'correto']):
            st.session_state.etapa_modulo = 'AGUARDANDO_APROVACAO_ABOUT'
            return None
        return None
    
    if etapa == 'AGUARDANDO_APROVACAO_ABOUT':
        if any(word in prompt.lower() for word in ['aprovar', 'aprovado', 'ok', 'sim', 'perfeito']):
            # Salvar dados de LinkedIn e ir para exports
            st.session_state.fase = 'FASE_EXPORTS_COMPLETO'
            return None
        return None

    # ========== FLUXO ORIGINAL (LEGACY) ==========

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
