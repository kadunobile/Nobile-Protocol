import logging
import streamlit as st
from core.utils import forcar_topo
from core.gpt_telemetry import chamar_gpt_com_telemetria, renderizar_badge_gpt_calls, CONTEXTO_DIAGNOSTICO, CONTEXTO_COLETA, CONTEXTO_REESCRITA, CONTEXTO_LINKEDIN, CONTEXTO_VALIDACAO
from core.cv_cache import obter_resumo_cv_cached, inicializar_cache_cv_async
from modules.otimizador.processor import processar_modulo_otimizador

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def fase_chat():
    """Interface de chat do Protocolo Nóbile com logging integrado."""
    logger.info("Iniciando fase de chat")
    
    # ===== FORÇAR SCROLL ANTES DE QUALQUER RENDERIZAÇÃO =====
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    
    if st.session_state.get('force_scroll_top', False):
        # Use forcar_topo() which is more reliable with Streamlit's rendering
        forcar_topo()
        st.session_state.force_scroll_top = False
    
    st.markdown("# 💬 [5] Headhunter Elite — Otimização Ativa")
    st.markdown("---")
    
    # ===== RENDERIZAR BADGE DE CHAMADAS GPT =====
    renderizar_badge_gpt_calls()
    
    # Inicializar cache do CV em background se ainda não foi feito
    if (st.session_state.get('cv_texto') and 
        not st.session_state.get('cv_resumo_cache') and
        st.session_state.get('openai_client')):
        try:
            inicializar_cache_cv_async(st.session_state.openai_client)
        except Exception as e:
            logger.warning(f"Erro ao inicializar cache do CV: {e}")
    
    # Show brief instructions ONCE before auto-trigger (only if chat is starting)
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_0_DIAGNOSTICO' and
        not st.session_state.get('etapa_0_diagnostico_triggered') and
        not st.session_state.get('chat_instructions_shown', False)):
        
        # Mark instructions as shown to avoid re-rendering on every rerun
        st.session_state.chat_instructions_shown = True
        
        st.info("""
        **🎯 Como funciona o Headhunter Elite:**
        
        O robô vai te fazer perguntas estratégicas sobre suas experiências e competências. 
        
        **Como responder:**
        - Seja específico e concreto
        - Compartilhe números, resultados e contexto
        - Se não souber ou não tiver experiência com algo, diga "não tenho"
        
        **O que vai acontecer:**
        1. Diagnóstico de gaps no seu CV
        2. Coleta de dados das suas experiências
        3. Reescrita otimizada do CV
        4. Otimização do perfil LinkedIn
        
        ⏱️ **Tempo estimado:** 15-20 minutos
        
        Vamos começar! 🚀
        """)
    
    # Render messages
    for msg in st.session_state.mensagens:
        # Skip internal messages (prompts do sistema não devem aparecer para o usuário)
        if msg.get("internal") == True:
            continue
        
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
        elif msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])


    # Auto-trigger ETAPA_0_DIAGNOSTICO (novo fluxo)
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_0_DIAGNOSTICO' and
        not st.session_state.get('etapa_0_diagnostico_triggered')):
        
        st.session_state.etapa_0_diagnostico_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_0_DIAGNOSTICO): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("🔍 Diagnosticando gaps no seu CV..."):
                    resp = chamar_gpt_com_telemetria(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        contexto=CONTEXTO_DIAGNOSTICO,
                        temperature=0.3,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait to start asking gaps
                        st.session_state.etapa_modulo = 'AGUARDANDO_INICIO_GAPS'
            st.rerun()
    
    # Auto-trigger primeiro gap individual
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_0_GAP_INDIVIDUAL' and
        not st.session_state.get('etapa_0_gap_triggered')):
        
        st.session_state.etapa_0_gap_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_0_GAP_INDIVIDUAL): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            with st.chat_message("assistant"):
                st.markdown(prompt_otimizador)
                st.session_state.mensagens.append({"role": "assistant", "content": prompt_otimizador})
                # Move to next state - wait for gap response
                st.session_state.etapa_modulo = 'AGUARDANDO_RESPOSTA_GAP'
                # Reset trigger for next gap
                st.session_state.etapa_0_gap_triggered = False
            st.rerun()
    
    # Auto-trigger resumo do diagnóstico
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_0_DIAGNOSTICO_RESUMO' and
        not st.session_state.get('etapa_0_resumo_triggered')):
        
        st.session_state.etapa_0_resumo_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_0_DIAGNOSTICO_RESUMO): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            with st.chat_message("assistant"):
                st.markdown(prompt_otimizador)
                st.session_state.mensagens.append({"role": "assistant", "content": prompt_otimizador})
                # Move to next state - wait for OK to continue
                st.session_state.etapa_modulo = 'AGUARDANDO_OK_DIAGNOSTICO'
            st.rerun()
    
    # Auto-trigger ETAPA_1_COLETA_FOCADA
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_1_COLETA_FOCADA' and
        not st.session_state.get('etapa_1_coleta_focada_triggered')):
        
        st.session_state.etapa_1_coleta_focada_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_1_COLETA_FOCADA): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("📝 Preparando coleta de dados..."):
                    resp = chamar_gpt_com_telemetria(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        contexto=CONTEXTO_COLETA,
                        temperature=0.3,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait for data
                        st.session_state.etapa_modulo = 'AGUARDANDO_DADOS_COLETA'
            st.rerun()
    
    # Auto-trigger ETAPA_1_5_SEO_INTRO
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_1_5_SEO_INTRO' and
        not st.session_state.get('etapa_1_5_seo_intro_triggered')):
        
        st.session_state.etapa_1_5_seo_intro_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_1_5_SEO_INTRO): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            with st.chat_message("assistant"):
                st.markdown(prompt_otimizador)
                st.session_state.mensagens.append({"role": "assistant", "content": prompt_otimizador})
                # Move to next state - wait to start asking keywords
                st.session_state.etapa_modulo = 'AGUARDANDO_INICIO_SEO'
            st.rerun()
    
    # Auto-trigger SEO keyword individual
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_1_5_SEO_KEYWORD' and
        not st.session_state.get('etapa_1_5_seo_keyword_triggered')):
        
        st.session_state.etapa_1_5_seo_keyword_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_1_5_SEO_KEYWORD): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            with st.chat_message("assistant"):
                st.markdown(prompt_otimizador)
                st.session_state.mensagens.append({"role": "assistant", "content": prompt_otimizador})
                # Move to next state - wait for keyword response
                st.session_state.etapa_modulo = 'AGUARDANDO_RESPOSTA_SEO_KEYWORD'
                # Reset trigger for next keyword
                st.session_state.etapa_1_5_seo_keyword_triggered = False
            st.rerun()
    
    # Auto-trigger resumo do SEO Mapping
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_1_5_SEO_RESUMO' and
        not st.session_state.get('etapa_1_5_seo_resumo_triggered')):
        
        st.session_state.etapa_1_5_seo_resumo_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_1_5_SEO_RESUMO): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            with st.chat_message("assistant"):
                st.markdown(prompt_otimizador)
                st.session_state.mensagens.append({"role": "assistant", "content": prompt_otimizador})
                # Move to next state - wait for OK to continue
                st.session_state.etapa_modulo = 'AGUARDANDO_OK_SEO'
            st.rerun()
    
    # Auto-trigger ETAPA_6_LINKEDIN
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_6_LINKEDIN' and
        not st.session_state.get('etapa_6_linkedin_triggered')):
        
        st.session_state.etapa_6_linkedin_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_6_LINKEDIN): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("🔵 Otimizando seu perfil LinkedIn..."):
                    resp = chamar_gpt_com_telemetria(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        contexto=CONTEXTO_LINKEDIN,
                        temperature=0.5,  # Mais criatividade para headlines
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait for headline choice
                        st.session_state.etapa_modulo = 'AGUARDANDO_ESCOLHA_HEADLINE'
            st.rerun()

    # Auto-trigger CHECKPOINT_1_VALIDACAO
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'CHECKPOINT_1_VALIDACAO' and
        not st.session_state.get('checkpoint_1_triggered')):
        
        st.session_state.checkpoint_1_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (CHECKPOINT_1_VALIDACAO): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("✅ Validando dados coletados..."):
                    resp = chamar_gpt_com_telemetria(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        contexto=CONTEXTO_VALIDACAO,
                        temperature=0.3,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait for approval
                        st.session_state.etapa_modulo = 'AGUARDANDO_APROVACAO_VALIDACAO'
            st.rerun()
    
    # Auto-trigger ETAPA_2_REESCRITA_EXP_* (dynamic states)
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo', '').startswith('ETAPA_2_REESCRITA_EXP_') and
        not st.session_state.get('etapa_2_reescrita_triggered')):
        
        st.session_state.etapa_2_reescrita_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_2_REESCRITA_EXP): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("✍️ Reescrevendo experiência profissional..."):
                    resp = chamar_gpt_com_telemetria(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        contexto=CONTEXTO_REESCRITA,
                        temperature=0.4,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Extract experience number from etapa
                        etapa = st.session_state.get('etapa_modulo', '')
                        try:
                            exp_num = int(etapa.split('_')[-1])
                        except (ValueError, IndexError) as e:
                            logger.error(f"Erro ao extrair número da experiência de etapa '{etapa}': {e}")
                            exp_num = 1  # Fallback to first experience
                        # Move to approval state for this experience
                        st.session_state.etapa_modulo = f'AGUARDANDO_APROVACAO_EXP_{exp_num}'
            st.rerun()
    
    # Auto-trigger ETAPA_2_REESCRITA_FINAL
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_2_REESCRITA_FINAL' and
        not st.session_state.get('etapa_2_final_triggered')):
        
        st.session_state.etapa_2_final_triggered = True
        try:
            prompt_otimizador = processar_modulo_otimizador("")
        except Exception as e:
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_2_REESCRITA_FINAL): {e}", exc_info=True)
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("🎯 Finalizando reescrita do CV..."):
                    resp = chamar_gpt_com_telemetria(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        contexto=CONTEXTO_REESCRITA,
                        temperature=0.3,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait to continue
                        st.session_state.etapa_modulo = 'AGUARDANDO_CONTINUAR_CHECKPOINT2'
            st.rerun()

    # ===== RENDERIZAR BOTÕES DE CONTINUAÇÃO =====
    # Mapa completo de botões contextuais para todos os estados AGUARDANDO_*
    if st.session_state.get('modulo_ativo') == 'OTIMIZADOR':
        etapa = st.session_state.get('etapa_modulo', '')
        
        # Definir botões para cada estado
        botoes = {
            'AGUARDANDO_INICIO_GAPS': ('▶️ Começar Diagnóstico', 'ok'),
            'AGUARDANDO_OK_DIAGNOSTICO': ('✅ Continuar para Coleta', 'continuar'),
            'AGUARDANDO_DADOS_COLETA': ('⏭️ Avançar para Próxima Etapa', 'continuar'),
            'AGUARDANDO_APROVACAO_VALIDACAO': ('✅ Aprovar e Continuar', 'aprovar'),
            'AGUARDANDO_CONTINUAR_CHECKPOINT2': ('🚀 Ir para Validação ATS', 'continuar'),
            'AGUARDANDO_OK_SKILLS': ('✅ Aprovar Skills', 'ok'),
            'AGUARDANDO_APROVACAO_ABOUT': ('✅ Aprovar e Exportar', 'aprovar'),
        }
        
        # Tratar estados dinâmicos AGUARDANDO_APROVACAO_EXP_N
        if etapa and etapa.startswith('AGUARDANDO_APROVACAO_EXP_'):
            botoes[etapa] = ('⏭️ Próxima Experiência', 'próxima')
        
        # Renderizar botão se estado atual está no mapa
        if etapa in botoes:
            texto_botao, comando = botoes[etapa]
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Usar key único baseado no etapa para evitar duplicatas
                if st.button(texto_botao, use_container_width=True, type="primary", key=f"btn_{etapa}"):
                    # Processar comando através do otimizador
                    resultado = processar_modulo_otimizador(comando)
                    if resultado:
                        st.session_state.mensagens.append({"role": "assistant", "content": resultado})
                    st.rerun()

    prompt = st.chat_input("Digite sua pergunta ou resposta...")

    if prompt:
        logger.debug(f"Prompt recebido: {prompt[:100]}...")  # Log apenas primeiros 100 chars
        st.session_state.mensagens.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.get('modulo_ativo') == 'OTIMIZADOR':
            try:
                prompt_otimizador = processar_modulo_otimizador(prompt)
            except Exception as e:
                logger.error(f"Erro ao processar módulo otimizador: {e}", exc_info=True)
                prompt_otimizador = None
                st.error("⚠️ Erro ao processar. Tente novamente ou clique no botão abaixo.")

            if prompt_otimizador:
                st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Processando etapa..."):
                        resp = chamar_gpt_com_telemetria(
                            st.session_state.openai_client, 
                            st.session_state.mensagens,
                            contexto=CONTEXTO_COLETA,
                            temperature=0.3,
                            seed=42
                        )
                        if resp:
                            st.markdown(resp)
                            st.session_state.mensagens.append({"role": "assistant", "content": resp})
            # Rerun whether processor succeeded or returned None
            # - If succeeded: rerun to display result
            # - If None: rerun to show the button instead
            st.rerun()
            return

        if hasattr(st.session_state, 'aguardando_vaga') and st.session_state.aguardando_vaga:
            cargo = st.session_state.perfil.get('cargo_alvo', 'N/A')
            pretensao = st.session_state.perfil.get('pretensao_salarial', 'N/A')
            prompt_fit = f"""[/fit_perfil]

**VAGA:**
{prompt}

**CARGO-ALVO:** {cargo}

Etapa 1: Estimativa Salarial da Vaga vs {pretensao}
Etapa 2: Score de Match (0-100%), Pontos de Atenção, Edições no CV
Etapa 3: Veredito Final (APLICAR / NÃO APLICAR)

Use o CV do contexto."""
            st.session_state.mensagens[-1]["content"] = prompt_fit
            st.session_state.aguardando_vaga = False

        with st.chat_message("assistant"):
            with st.spinner("🤔 Analisando..."):
                resp = chamar_gpt_com_telemetria(
                    st.session_state.openai_client, 
                    st.session_state.mensagens,
                    contexto=CONTEXTO_OUTROS
                )
                if resp:
                    st.markdown(resp)
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})