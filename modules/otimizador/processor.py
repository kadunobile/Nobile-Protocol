# Novas etapas do fluxo otimizado
from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico, prompt_etapa0_diagnostico_gap_individual
from modules.otimizador.etapa1_coleta_focada import prompt_etapa1_coleta_focada
from modules.otimizador.checkpoint_validacao import prompt_checkpoint_validacao
from modules.otimizador.etapa2_reescrita_progressiva import prompt_etapa2_reescrita_progressiva, prompt_etapa2_reescrita_final
from modules.otimizador.etapa6_otimizacao_linkedin import prompt_etapa6_otimizacao_linkedin

# HEADHUNTER ELITE: Módulos dinâmicos com geração contextual de perguntas
from modules.otimizador.etapa0_diagnostico_dinamico import (
    gerar_pergunta_dinamica_gap,
    verificar_resposta_negativa_gap,
    deve_aprofundar_gap
)
from modules.otimizador.etapa1_coleta_dinamica import (
    prompt_etapa1_coleta_dinamica_inicial,
    gerar_proxima_pergunta_coleta,
    verificar_pronto_para_avancar_coleta,
    gerar_mensagem_transicao_coleta
)
from modules.otimizador.etapa1_5_seo_mapping import (
    prompt_etapa1_5_seo_intro,
    prompt_etapa1_5_seo_keyword,
    processar_resposta_keyword,
    gerar_resumo_seo_mapping,
    obter_keywords_a_perguntar
)

# HEADHUNTER ELITE: Novos módulos de inteligência
from modules.otimizador.market_knowledge import detectar_area_por_cargo, obter_conhecimento_mercado
from modules.otimizador.classificador_perfil import classificar_senioridade_e_estrategia
from modules.otimizador.analisador_bullets import analisar_bullets_fracos
from modules.otimizador.engenheiro_texto import gerar_bullet_star, aplicar_star_method_completo

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
ENABLE_DYNAMIC_QUESTIONS = True  # Enable dynamic question generation (set to False to use static prompts)

# HEADHUNTER ELITE: Etapas com pause obrigatória
ETAPAS_COM_PAUSE_OBRIGATORIA = [
    'ETAPA_0_DIAGNOSTICO_RESUMO',     # Pausa após resumo de diagnóstico
    'AGUARDANDO_OK_DIAGNOSTICO',      # Pausa para usuário confirmar diagnóstico
    'ETAPA_1_5_SEO_RESUMO',           # Pausa após resumo de SEO Mapping
    'AGUARDANDO_OK_SEO',              # Pausa para usuário confirmar SEO
    'CHECKPOINT_1_VALIDACAO',         # Pausa após validação de mapeamento
    'AGUARDANDO_APROVACAO_VALIDACAO', # Pausa para usuário aprovar validação
    'AGUARDANDO_CONTINUAR_CHECKPOINT2', # Pausa antes de LinkedIn
]

# Keywords que indicam que o usuário não tem experiência com um gap
NEGATIVE_RESPONSE_KEYWORDS = [
    # Absolute lack of possession
    'não tenho', 'nao tenho', 
    'não possuo', 'nao possuo',
    'nunca tive',
    # Lack of knowledge
    'não sei', 'nao sei',
    'não conheço', 'nao conheço',
    'desconheço', 'desconheco',
    # No experience/usage
    'nunca usei', 'nunca trabalhei', 'nunca utilizei',
    'não tive contato', 'nao tive contato',
    'sem experiência', 'sem experiencia',
    # Absolute negation
    'jamais',
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
            
            # Get gap early for error handling
            gap = gaps[gap_index] if gap_index < len(gaps) else 'unknown'
            
            if gap_index < len(gaps):
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
                    # Reset trigger flag so next gap can be shown
                    st.session_state.etapa_0_gap_triggered = False
                    return prompt_etapa0_diagnostico_gap_individual(st.session_state.gap_atual_index)
                else:
                    # Todos os gaps foram processados - ir para resumo
                    st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO_RESUMO'
                    st.session_state.etapa_0_resumo_triggered = False  # Reset trigger for resumo
                    return gerar_resumo_diagnostico()
        except Exception as e:
            gap_info = f"índice {gap_index}, gap: {gap}" if 'gap' in locals() and 'gap_index' in locals() else "índice desconhecido"
            logger.error(f"Erro ao processar resposta de gap [{gap_info}]: {e}", exc_info=True)
            # Tentar recuperar indo para resumo
            st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO_RESUMO'
            st.session_state.etapa_0_resumo_triggered = False  # Reset trigger for resumo
            return gerar_resumo_diagnostico()
        
        return None
    
    if etapa == 'ETAPA_0_DIAGNOSTICO_RESUMO':
        return gerar_resumo_diagnostico()
    
    if etapa == 'AGUARDANDO_OK_DIAGNOSTICO':
        # Usuário confirmou o resumo - avançar para coleta
        st.session_state.etapa_modulo = 'ETAPA_1_COLETA_FOCADA'
        st.session_state.etapa_1_coleta_focada_triggered = False  # Reset trigger for coleta
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
        
        # Usar prompt dinâmico ou estático baseado na configuração
        if ENABLE_DYNAMIC_QUESTIONS:
            return prompt_etapa1_coleta_dinamica_inicial()
        else:
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
                # Usuário quer avançar - salvar dados e ir para SEO MAPPING
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
                
                # Verificar se há keywords para perguntar na etapa de SEO
                keywords_a_perguntar = obter_keywords_a_perguntar()
                if keywords_a_perguntar:
                    # Há keywords para perguntar - ir para SEO MAPPING
                    st.session_state.etapa_modulo = 'ETAPA_1_5_SEO_INTRO'
                    st.session_state.etapa_1_5_seo_intro_triggered = False  # Reset trigger
                    return prompt_etapa1_5_seo_intro()
                else:
                    # Não há keywords para perguntar - pular para CHECKPOINT_1
                    logger.info("Nenhuma keyword para perguntar - pulando SEO Mapping")
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
                
                # === MODO DINÂMICO: Gerar próxima pergunta com GPT ===
                if ENABLE_DYNAMIC_QUESTIONS:
                    # Verificar se já coletou dados suficientes (stop condition)
                    if verificar_pronto_para_avancar_coleta():
                        logger.info("Stop condition atingida - mostrando mensagem de transição")
                        return gerar_mensagem_transicao_coleta()
                    
                    # Gerar próxima pergunta dinâmica
                    client = st.session_state.get('openai_client')
                    if client:
                        try:
                            proxima_pergunta = gerar_proxima_pergunta_coleta(client, prompt)
                            if proxima_pergunta:
                                return proxima_pergunta
                            else:
                                # Stop condition atingida pela função
                                return gerar_mensagem_transicao_coleta()
                        except Exception as e:
                            logger.error(f"Erro ao gerar próxima pergunta dinâmica: {e}", exc_info=True)
                            # Fallback: continuar com fluxo normal (retornar None)
                    else:
                        logger.warning("Cliente OpenAI não disponível para geração dinâmica")
                
                # Se já coletou 3+ respostas, permitir avançar mas NÃO forçar
                # O usuário ainda pode continuar respondendo ou digitar "continuar"
                # Retornar None para que a LLM continue a conversação naturalmente
        except Exception as e:
            current_count = st.session_state.get('dados_coleta_count', 0)
            logger.error(f"Erro ao processar coleta de dados (respostas coletadas: {current_count}): {e}", exc_info=True)
            # Tentar recuperar mantendo o fluxo
            return None
        
        return None
    
    # ETAPA 1.5: SEO MAPPING (TARGET) - Perguntas sobre keywords essenciais
    if etapa == 'ETAPA_1_5_SEO_INTRO':
        return prompt_etapa1_5_seo_intro()
    
    if etapa == 'AGUARDANDO_INICIO_SEO':
        # Usuário leu a introdução, vamos começar com a primeira keyword
        st.session_state.seo_keyword_index = 0
        st.session_state.etapa_modulo = 'ETAPA_1_5_SEO_KEYWORD'
        return prompt_etapa1_5_seo_keyword(0)
    
    if etapa == 'ETAPA_1_5_SEO_KEYWORD':
        # Perguntar sobre a keyword atual
        keyword_index = st.session_state.get('seo_keyword_index', 0)
        return prompt_etapa1_5_seo_keyword(keyword_index)
    
    if etapa == 'AGUARDANDO_RESPOSTA_SEO_KEYWORD':
        # Processar resposta do usuário sobre a keyword atual
        try:
            keyword_index = st.session_state.get('seo_keyword_index', 0)
            keywords_a_perguntar = obter_keywords_a_perguntar()
            
            if keyword_index < len(keywords_a_perguntar):
                keyword = keywords_a_perguntar[keyword_index]
                
                # Processar resposta
                processar_resposta_keyword(prompt, keyword)
                
                # Avançar para a próxima keyword
                st.session_state.seo_keyword_index = keyword_index + 1
                
                # Verificar se há mais keywords
                if st.session_state.seo_keyword_index < len(keywords_a_perguntar):
                    # Continuar com a próxima keyword
                    st.session_state.etapa_modulo = 'ETAPA_1_5_SEO_KEYWORD'
                    st.session_state.etapa_1_5_seo_keyword_triggered = False  # Reset trigger
                    return prompt_etapa1_5_seo_keyword(st.session_state.seo_keyword_index)
                else:
                    # Todas as keywords foram processadas - ir para resumo
                    st.session_state.etapa_modulo = 'ETAPA_1_5_SEO_RESUMO'
                    st.session_state.etapa_1_5_seo_resumo_triggered = False  # Reset trigger
                    return gerar_resumo_seo_mapping()
        except Exception as e:
            logger.error(f"Erro ao processar resposta de keyword SEO: {e}", exc_info=True)
            # Tentar recuperar indo para resumo ou checkpoint
            st.session_state.etapa_modulo = 'CHECKPOINT_1_VALIDACAO'
            return prompt_checkpoint_validacao()
        
        return None
    
    if etapa == 'ETAPA_1_5_SEO_RESUMO':
        return gerar_resumo_seo_mapping()
    
    if etapa == 'AGUARDANDO_OK_SEO':
        # Usuário confirmou o resumo de SEO - avançar para checkpoint
        st.session_state.etapa_modulo = 'CHECKPOINT_1_VALIDACAO'
        st.session_state.checkpoint_1_triggered = False  # Reset trigger
        return prompt_checkpoint_validacao()
    
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
            if not st.session_state.get('cv_otimizado'):
                st.session_state.cv_otimizado = st.session_state.get('cv_texto', '')
            # Go to LinkedIn optimization FIRST, then exports
            st.session_state.etapa_modulo = 'ETAPA_6_LINKEDIN'
            st.session_state.etapa_6_linkedin_triggered = False  # Reset flag
            return None
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
            st.session_state.fase = 'FASE_VALIDACAO_SCORE_ATS'
            return None
        return None

    return None
