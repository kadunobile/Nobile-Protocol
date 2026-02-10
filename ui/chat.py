import logging
import streamlit as st
from core.utils import chamar_gpt, forcar_topo
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
    
    st.markdown("# 💬 Sessão Ativa - Protocolo Nóbile")
    st.markdown("---")

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
            logger.error(f"Erro ao processar módulo otimizador (ETAPA_0_DIAGNOSTICO): {e}")
            prompt_otimizador = None
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("🔍 Diagnosticando gaps no seu CV..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
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
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            with st.chat_message("assistant"):
                st.markdown(prompt_otimizador)
                st.session_state.mensagens.append({"role": "assistant", "content": prompt_otimizador})
                # Move to next state - wait for gap response
                st.session_state.etapa_modulo = 'AGUARDANDO_RESPOSTA_GAP'
            st.rerun()
    
    # Auto-trigger resumo do diagnóstico
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_0_DIAGNOSTICO_RESUMO' and
        not st.session_state.get('etapa_0_resumo_triggered')):
        
        st.session_state.etapa_0_resumo_triggered = True
        prompt_otimizador = processar_modulo_otimizador("")
        
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
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("📝 Preparando coleta de dados..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        temperature=0.3,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait for data
                        st.session_state.etapa_modulo = 'AGUARDANDO_DADOS_COLETA'
            st.rerun()
    
    # Auto-trigger ETAPA_6_LINKEDIN
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_6_LINKEDIN' and
        not st.session_state.get('etapa_6_linkedin_triggered')):
        
        st.session_state.etapa_6_linkedin_triggered = True
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("🔵 Otimizando seu perfil LinkedIn..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
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
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("✅ Validando dados coletados..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
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
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("✍️ Reescrevendo experiência profissional..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        temperature=0.4,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Extract experience number from etapa
                        etapa = st.session_state.get('etapa_modulo', '')
                        exp_num = int(etapa.split('_')[-1])
                        # Move to approval state for this experience
                        st.session_state.etapa_modulo = f'AGUARDANDO_APROVACAO_EXP_{exp_num}'
            st.rerun()
    
    # Auto-trigger ETAPA_2_REESCRITA_FINAL
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_2_REESCRITA_FINAL' and
        not st.session_state.get('etapa_2_final_triggered')):
        
        st.session_state.etapa_2_final_triggered = True
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
            with st.chat_message("assistant"):
                with st.spinner("🎯 Finalizando reescrita do CV..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
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
                    from modules.otimizador.processor import processar_modulo_otimizador
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
            prompt_otimizador = processar_modulo_otimizador(prompt)

            if prompt_otimizador:
                st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador, "internal": True})
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Processando etapa..."):
                        resp = chamar_gpt(
                            st.session_state.openai_client, 
                            st.session_state.mensagens,
                            temperature=0.3,  # Consistência para otimização
                            seed=42           # Determinístico
                        )
                        if resp:
                            st.markdown(resp)
                            st.session_state.mensagens.append({"role": "assistant", "content": resp})
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
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.markdown(resp)
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})