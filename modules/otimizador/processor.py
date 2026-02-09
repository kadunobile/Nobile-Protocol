from modules.otimizador.etapa1_seo import prompt_etapa1
from modules.otimizador.etapa1_5_analise_cv import prompt_etapa1_5
from modules.otimizador.etapa2_interrogatorio import prompt_etapa2
from modules.otimizador.etapa3_curadoria import prompt_etapa3
from modules.otimizador.etapa4_engenharia import prompt_etapa4
from modules.otimizador.etapa5_validacao import prompt_etapa5
from modules.otimizador.etapa6_arquivo import prompt_etapa6
from modules.otimizador.etapa7_exportacao import prompt_etapa7
# Novas etapas do fluxo otimizado
from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico, prompt_etapa0_diagnostico_gap_individual
from modules.otimizador.etapa1_coleta_focada import prompt_etapa1_coleta_focada
from modules.otimizador.checkpoint_validacao import prompt_checkpoint_validacao
from modules.otimizador.etapa2_reescrita_progressiva import prompt_etapa2_reescrita_progressiva, prompt_etapa2_reescrita_final
from modules.otimizador.etapa6_otimizacao_linkedin import prompt_etapa6_otimizacao_linkedin
import streamlit as st
import logging

logger = logging.getLogger(__name__)

# Defensive import for cv_estruturado - provide fallbacks if module has issues
try:
    from core.cv_estruturado import (
        inicializar_cv_estruturado, 
        salvar_dados_coleta, 
        atualizar_posicionamento,
        atualizar_gaps
    )
except ImportError:
    # Fallback functions if cv_estruturado not available
    def inicializar_cv_estruturado():
        return {}
    def salvar_dados_coleta(dados):
        pass
    def atualizar_posicionamento(**kwargs):
        pass
    def atualizar_gaps(**kwargs):
        pass

# Configuration constants
DEFAULT_MAX_EXPERIENCES = 3  # Default number of experiences to optimize
MIN_RESPONSE_LENGTH = 10  # Minimum response length to be considered substantive

# Keywords que indicam que o usuário não tem experiência com um gap
NEGATIVE_RESPONSE_KEYWORDS = [
    'não tenho', 'nao tenho', 'não', 'nao', 
    'não sei', 'nao sei', 'nunca', 'jamais'
]


def gerar_resumo_diagnostico():
    """
    Gera resumo do diagnóstico após coletar respostas de todos os gaps.
    
    Returns:
        str: Resumo formatado do diagnóstico
    """
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    perfil = st.session_state.get('perfil', {})
    cargo = perfil.get('cargo_alvo', 'cargo desejado')
    
    gaps_com_experiencia = {gap: info for gap, info in gaps_respostas.items() if info.get('tem_experiencia')}
    gaps_sem_experiencia = {gap: info for gap, info in gaps_respostas.items() if not info.get('tem_experiencia')}
    
    resumo = f"""### 📋 RESUMO DO DIAGNÓSTICO

**CARGO-ALVO:** {cargo}

---

"""
    
    if gaps_com_experiencia:
        resumo += """#### ✅ Gaps que você TEM experiência:

"""
        for gap, info in gaps_com_experiencia.items():
            resumo += f"""**{gap}**
📝 Sua resposta: _{info['resposta']}_

"""
    
    if gaps_sem_experiencia:
        resumo += """
#### ❌ Gaps que você NÃO tem experiência:

"""
        for gap in gaps_sem_experiencia.keys():
            resumo += f"- {gap}\n"
    
    resumo += """
---

### 🎯 Próximos Passos

Agora vamos coletar dados adicionais sobre suas experiências profissionais para otimizar seu CV e destacar as competências que você JÁ TEM!

"""
    
    # Salvar contagem de gaps resolvidos para uso posterior
    st.session_state.gaps_resolviveis_count = len(gaps_com_experiencia)
    st.session_state.gaps_nao_resolviveis_count = len(gaps_sem_experiencia)
    
    return resumo


def processar_modulo_otimizador(prompt):
    perfil = st.session_state.get('perfil', {})
    cargo = perfil.get('cargo_alvo', 'cargo desejado')
    etapa = st.session_state.get('etapa_modulo')
    
    # ========== NOVO FLUXO OTIMIZADO ==========
    
    # ETAPA 0: DIAGNÓSTICO (introdução)
    if etapa == 'ETAPA_0_DIAGNOSTICO':
        return prompt_etapa0_diagnostico()
    
    # ETAPA 0: PERGUNTAR SOBRE CADA GAP INDIVIDUALMENTE
    if etapa == 'AGUARDANDO_INICIO_GAPS':
        # Usuário leu a introdução, vamos começar com o primeiro gap
        st.session_state.gap_atual_index = 0
        st.session_state.etapa_modulo = 'ETAPA_0_GAP_INDIVIDUAL'
        return prompt_etapa0_diagnostico_gap_individual(0)
    
    if etapa == 'ETAPA_0_GAP_INDIVIDUAL':
        # Perguntar sobre o gap atual
        gap_index = st.session_state.get('gap_atual_index', 0)
        return prompt_etapa0_diagnostico_gap_individual(gap_index)
    
    if etapa == 'AGUARDANDO_RESPOSTA_GAP':
        # Processar resposta do usuário sobre o gap atual
        try:
            gap_index = st.session_state.get('gap_atual_index', 0)
            gaps = st.session_state.get('gaps_alvo', [])
            
            if gap_index < len(gaps):
                gap = gaps[gap_index]
                
                # Inicializar dicionário de respostas se não existir
                if 'gaps_respostas' not in st.session_state:
                    st.session_state.gaps_respostas = {}
                
                # Verificar se usuário disse que não tem experiência
                if any(word in prompt.lower() for word in NEGATIVE_RESPONSE_KEYWORDS):
                    # Usuário não tem experiência com este gap
                    st.session_state.gaps_respostas[gap] = {
                        'tem_experiencia': False,
                        'resposta': None
                    }
                else:
                    # Usuário tem experiência - salvar resposta
                    st.session_state.gaps_respostas[gap] = {
                        'tem_experiencia': True,
                        'resposta': prompt
                    }
                
                # Avançar para o próximo gap
                st.session_state.gap_atual_index = gap_index + 1
                
                # Verificar se há mais gaps
                if st.session_state.gap_atual_index < len(gaps):
                    # Continuar com o próximo gap
                    st.session_state.etapa_modulo = 'ETAPA_0_GAP_INDIVIDUAL'
                    return prompt_etapa0_diagnostico_gap_individual(st.session_state.gap_atual_index)
                else:
                    # Todos os gaps foram processados - ir para resumo
                    st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO_RESUMO'
                    return gerar_resumo_diagnostico()
        except Exception as e:
            logger.error(f"Erro ao processar resposta de gap [índice {gap_index}, gap: {gap}]: {e}", exc_info=True)
            # Tentar recuperar indo para resumo
            st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO_RESUMO'
            return gerar_resumo_diagnostico()
        
        return None
    
    if etapa == 'ETAPA_0_DIAGNOSTICO_RESUMO':
        return gerar_resumo_diagnostico()
    
    if etapa == 'AGUARDANDO_OK_DIAGNOSTICO':
        # Usuário confirmou o resumo - avançar para coleta
        st.session_state.etapa_modulo = 'ETAPA_1_COLETA_FOCADA'
        return prompt_etapa1_coleta_focada()
    
    # ETAPA 1: COLETA FOCADA
    if etapa == 'ETAPA_1_COLETA_FOCADA':
        # Inicializar estrutura de CV e contador de respostas se não existir
        if 'cv_estruturado' not in st.session_state:
            st.session_state.cv_estruturado = inicializar_cv_estruturado()
            # Atualizar posicionamento com cargo alvo
            perfil = st.session_state.get('perfil', {})
            cargo = perfil.get('cargo_alvo', '')
            if cargo:
                atualizar_posicionamento(cargo_alvo=cargo)
            # Atualizar gaps identificados
            gaps_respostas = st.session_state.get('gaps_respostas', {})
            if gaps_respostas:
                resolvidos = [gap for gap, info in gaps_respostas.items() if info.get('tem_experiencia')]
                nao_resolvidos = [gap for gap, info in gaps_respostas.items() if not info.get('tem_experiencia')]
                atualizar_gaps(
                    identificados=list(gaps_respostas.keys()),
                    resolvidos=resolvidos,
                    nao_resolvidos=nao_resolvidos
                )
        
        if 'dados_coleta_count' not in st.session_state:
            st.session_state.dados_coleta_count = 0
        if 'dados_coleta_historico' not in st.session_state:
            st.session_state.dados_coleta_historico = []
        
        return prompt_etapa1_coleta_focada()
    
    if etapa == 'AGUARDANDO_DADOS_COLETA':
        # CRITICAL FIX: Aceitar QUALQUER resposta do usuário como dados coletados
        # não apenas keywords específicas
        
        try:
            # Inicializar histórico se não existir
            if 'dados_coleta_historico' not in st.session_state:
                st.session_state.dados_coleta_historico = []
            if 'dados_coleta_count' not in st.session_state:
                st.session_state.dados_coleta_count = 0
            
            # Verificar se usuário quer avançar explicitamente
            palavras_avanco = ['continuar', 'pronto', 'concluído', 'concluido', 'finalizado',
                              'próxima', 'proxima', 'próximo', 'proximo', 'avançar', 'avancar']
            
            if any(word in prompt.lower() for word in palavras_avanco):
                # Usuário quer avançar - salvar dados e ir para validação
                st.session_state.dados_coletados = {
                    'raw_response': prompt,
                    'historico': st.session_state.dados_coleta_historico,
                    'total_respostas': st.session_state.dados_coleta_count
                }
                # Salvar na estrutura de CV
                try:
                    salvar_dados_coleta(st.session_state.dados_coletados)
                except Exception as e:
                    logger.warning(f"Erro ao salvar dados coletados: {e}")
                st.session_state.etapa_modulo = 'CHECKPOINT_1_VALIDACAO'
                return prompt_checkpoint_validacao()
            
            # Se não for comando de avançar, SALVAR a resposta como dado coletado
            # e permitir que o chat continue normalmente para mais perguntas
            if len(prompt.strip()) > MIN_RESPONSE_LENGTH:  # Resposta com conteúdo substantivo
                st.session_state.dados_coleta_historico.append(prompt)
                st.session_state.dados_coleta_count += 1
                
                # Salvar incrementalmente na estrutura
                try:
                    salvar_dados_coleta({'raw_response': prompt})
                except Exception as e:
                    logger.warning(f"Erro ao salvar dados incrementais: {e}")
                
                # Se já coletou 3+ respostas, permitir avançar mas NÃO forçar
                # O usuário ainda pode continuar respondendo ou digitar "continuar"
                # Retornar None para que a LLM continue a conversação naturalmente
        except Exception as e:
            current_count = st.session_state.get('dados_coleta_count', 0)
            logger.error(f"Erro ao processar coleta de dados (respostas coletadas: {current_count}): {e}", exc_info=True)
            # Tentar recuperar mantendo o fluxo
            return None
        
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
