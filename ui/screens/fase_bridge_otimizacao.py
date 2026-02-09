"""
Fase Bridge Otimização - Ponte estratégica entre Reality Check e Otimização de CV.

Versão simplificada: usa dados já calculados no Reality Check (ATS v3.2)
para mostrar resumo rápido antes de iniciar o otimizador.
"""

import streamlit as st
import logging
from core.ats_scorer import calcular_score_ats
from core.utils import forcar_topo

logger = logging.getLogger(__name__)


def fase_bridge_otimizacao():
    """
    Tela de ponte estratégica entre Reality Check e Otimização.

    Usa os dados ATS já calculados no Reality Check (session_state)
    para exibir um resumo rápido antes de iniciar o otimizador de 8 etapas.
    """
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    forcar_topo()

    st.markdown("# 🌉 Preparação para Otimização")
    st.markdown("---")

    # ── Validação ──
    if not st.session_state.get('cv_texto'):
        st.error("⚠️ CV não encontrado. Por favor, faça upload do CV novamente.")
        if st.button("🔙 Voltar para Upload"):
            st.session_state.fase = 'FASE_0_UPLOAD'
            st.rerun()
        return

    # ── Recuperar dados ATS do Reality Check (ou recalcular) ──
    ats_resultado = st.session_state.get('reality_ats_resultado')

    if not ats_resultado:
        # Fallback: calcular se não veio do Reality Check
        with st.spinner("📊 Calculando Score ATS do seu CV atual..."):
            cargo = st.session_state.get('perfil', {}).get('cargo_alvo', 'cargo desejado')
            perfil = st.session_state.get('perfil', {})
            ats_resultado = calcular_score_ats(
                cv_texto=st.session_state.cv_texto,
                cargo_alvo=cargo,
                client=st.session_state.get('openai_client'),
                objetivo=perfil.get('objetivo'),
                cargo_atual=perfil.get('cargo_atual')
            )
            st.session_state.reality_ats_resultado = ats_resultado
            logger.info(f"ATS recalculado na Bridge: {ats_resultado.get('score_total')}/100")

    score = ats_resultado.get('score_total', 0)
    nivel = ats_resultado.get('nivel', 'N/A')
    pontos_fortes = ats_resultado.get('pontos_fortes', [])
    gaps = ats_resultado.get('gaps_identificados', [])
    plano = ats_resultado.get('plano_acao', [])

    # ── Score ATS Resumo ──
    st.markdown("## 📊 Resumo do Seu Score ATS")

    if score >= 70:
        cor = "#4ade80"
        emoji = "🟢"
    elif score >= 50:
        cor = "#facc15"
        emoji = "🟡"
    elif score >= 30:
        cor = "#fb923c"
        emoji = "🟠"
    else:
        cor = "#f87171"
        emoji = "🔴"

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"### {emoji} Score Atual: **{score}/100** ({nivel})")
        st.progress(min(score / 100, 1.0))

    with col2:
        st.metric("Meta", "80", delta=None)

    with col3:
        diferenca = 80 - score
        if diferenca > 0:
            st.metric("A Ganhar", f"+{diferenca:.1f}", delta=diferenca, delta_color="normal")
        else:
            st.metric("Acima da Meta", f"{abs(diferenca):.1f}", delta=abs(diferenca), delta_color="inverse")

    st.markdown("---")

    # ── Skills + Gaps (do ATS real) ──
    col_forte, col_gap = st.columns(2)

    with col_forte:
        st.markdown("### ✅ Skills Encontradas")
        if pontos_fortes:
            for termo in pontos_fortes[:6]:
                st.markdown(f"- ✅ **{termo}**")
        else:
            st.caption("Nenhum ponto forte identificado pelo ATS.")

    with col_gap:
        st.markdown("### ❌ Skills Faltantes")
        if gaps:
            for termo in gaps[:6]:
                st.markdown(f"- ❌ **{termo}**")
        else:
            st.success("Nenhum gap crítico identificado!")

    # Salvar gaps para uso no otimizador
    st.session_state.gaps_alvo = gaps

    # ── Seção de Transparência v5.0: Skills NÃO consideradas gaps ──
    gaps_falsos = ats_resultado.get('gaps_falsos_ignorados', [])
    if gaps_falsos:
        with st.expander("🔍 Transparência: Skills que NÃO foram consideradas gaps"):
            st.caption("Estas skills foram analisadas mas **descartadas** como gaps por não serem padrão obrigatório para o cargo:")
            for item in gaps_falsos[:8]:
                st.markdown(f"- 🟡 {item}")

    # ── Arquétipo e Método v5.0 ──
    arquetipo = ats_resultado.get('arquetipo_cargo', 'N/A')
    metodo = ats_resultado.get('metodo', 'N/A')
    fonte = ats_resultado.get('fonte_vaga', 'N/A')
    
    if arquetipo != 'N/A':
        st.caption(f"🎯 **Arquétipo identificado:** {arquetipo} | **Fonte:** {fonte}")

    st.markdown("---")

    # ── Input Opcional: Texto da Vaga Real (v5.0) ──
    with st.expander("📄 Tem a descrição da vaga? Cole aqui para análise SUPER precisa"):
        st.caption("Se você tiver o texto completo da vaga, cole abaixo. O sistema vai **recalcular** o score usando APENAS os requisitos que estão na vaga real.")
        texto_vaga_input = st.text_area(
            "Descrição da vaga (opcional):", 
            height=200,
            placeholder="Cole aqui o texto da vaga..."
        )
        
        if st.button("🔄 Recalcular Score com Vaga Real", disabled=not texto_vaga_input.strip()):
            with st.spinner("📊 Recalculando score com vaga real..."):
                cargo = st.session_state.get('perfil', {}).get('cargo_alvo', 'cargo desejado')
                perfil = st.session_state.get('perfil', {})
                ats_resultado_novo = calcular_score_ats(
                    cv_texto=st.session_state.cv_texto,
                    cargo_alvo=cargo,
                    client=st.session_state.get('openai_client'),
                    texto_vaga=texto_vaga_input.strip(),
                    objetivo=perfil.get('objetivo'),
                    cargo_atual=perfil.get('cargo_atual')
                )
                st.session_state.reality_ats_resultado = ats_resultado_novo
                st.success("✅ Score recalculado com a vaga real!")
                st.rerun()

    st.markdown("---")

    # ── Plano de Ação ──
    if plano:
        st.markdown("### 📋 Plano de Ação")
        for item in plano:
            st.markdown(f"  {item}")
        st.markdown("---")

    # ── O que vamos fazer ──
    st.info("""
    ### 🚀 O Que Vamos Fazer Agora?

    O processo de otimização vai:

    1. **Diagnosticar** onde cada gap pode ser resolvido no seu CV
    2. **Coletar dados** focados (apenas 3 perguntas por experiência)
    3. **Validar informações** antes de reescrever
    4. **Reescrever progressivamente** cada experiência (com destaque das mudanças)
    5. **Calcular novo Score ATS** e mostrar a melhoria
    6. **Otimizar LinkedIn** (headlines, skills, about)
    7. **Gerar exports** em múltiplos formatos (PDF, DOCX, TXT)

    ⏱️ **Tempo estimado:** 15-20 minutos
    """)

    st.markdown("---")

    # ── Botão único de ação ──
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 INICIAR OTIMIZAÇÃO COMPLETA", use_container_width=True, type="primary"):
            # Limpar TODAS as flags de trigger para evitar que prompts sejam vistos pelo usuário
            st.session_state.etapa_0_diagnostico_triggered = False
            st.session_state.etapa_1_coleta_focada_triggered = False
            st.session_state.etapa_1_triggered = False
            st.session_state.etapa_6_linkedin_triggered = False
            
            st.session_state.modulo_ativo = 'OTIMIZADOR'
            st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO'
            st.session_state.mensagens = []
            st.session_state.fase = 'CHAT'
            st.session_state.force_scroll_top = True
            st.rerun()
