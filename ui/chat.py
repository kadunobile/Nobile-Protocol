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
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
        elif msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])

    # Auto-trigger ETAPA_1_SEO if just entering that state (but not if still waiting for Iniciar button)
    if (st.session_state.get('modulo_ativo') == 'OTIMIZADOR' and 
        st.session_state.get('etapa_modulo') == 'ETAPA_1_SEO' and
        not st.session_state.get('etapa_1_triggered')):
        
        st.session_state.etapa_1_triggered = True
        prompt_otimizador = processar_modulo_otimizador("")
        
        if prompt_otimizador:
            st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador})
            with st.chat_message("assistant"):
                with st.spinner("🤔 Analisando keywords para seu cargo..."):
                    resp = chamar_gpt(
                        st.session_state.openai_client, 
                        st.session_state.mensagens,
                        temperature=0.3,
                        seed=42
                    )
                    if resp:
                        st.markdown(resp)
                        st.session_state.mensagens.append({"role": "assistant", "content": resp})
                        # Move to next state - wait for OK to continue
                        st.session_state.etapa_modulo = 'AGUARDANDO_OK_KEYWORDS'
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
                st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador})
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