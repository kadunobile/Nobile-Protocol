"""
Fase Validação Score ATS - Mostra Score ATS antes/depois da otimização.

Esta fase:
- Calcula novo Score ATS do CV otimizado
- Mostra comparação visual antes → depois
- Breakdown detalhado por categoria
- % de melhoria e gaps resolvidos
- Valida se atingiu a meta (80)
"""

import streamlit as st
from core.ats_scorer import calcular_score_ats
from core.utils import forcar_topo
from modules.otimizador.helpers_export import gerar_analytics_data, formatar_comparacao_antes_depois


def fase_validacao_score_ats():
    """
    Tela de validação do Score ATS pós-otimização.
    
    Calcula o novo score, compara com o inicial e mostra
    a melhoria alcançada em cada categoria.
    """
    # Forçar scroll ao topo
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    forcar_topo()
    
    st.markdown("# 📊 [6] Validação Score ATS - Antes × Depois")
    st.markdown("---")
    
    # Verificar se temos CV otimizado
    cv_otimizado = st.session_state.get('cv_otimizado', '')
    
    if not cv_otimizado:
        # Tentar pegar o CV original como fallback
        cv_otimizado = st.session_state.get('cv_texto', '')
    
    if not cv_otimizado:
        st.error("⚠️ CV otimizado não encontrado. Por favor, refaça o processo de otimização.")
        if st.button("🔙 Voltar"):
            st.session_state.fase = 'FASE_15_REALITY'
            st.rerun()
        return
    
    # Calcular Score ATS final se ainda não foi calculado
    if st.session_state.get('score_ats_final') is None:
        with st.spinner("📊 Calculando novo Score ATS do CV otimizado..."):
            cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
            score_resultado = calcular_score_ats(cv_otimizado, cargo)
            st.session_state.score_ats_final = score_resultado
    
    score_inicial = st.session_state.get('score_ats_inicial')
    score_final = st.session_state.score_ats_final
    
    if not score_inicial:
        st.warning("⚠️ Score inicial não encontrado. Mostrando apenas score final.")
        score_inicial = {'score_total': 0, 'percentual': 0, 'nivel': 'N/A', 'detalhes': {
            'secoes': {'encontradas': 0, 'total': 4}, 
            'keywords': {'encontradas': 0, 'total': 10},
            'metricas': {'quantidade': 0},
            'formatacao': {'bullets': 0, 'datas': 0},
            'tamanho': {'palavras': 0}
        }}
    
    # Calcular melhoria - handle case when initial score is 0
    melhoria = score_final['score_total'] - score_inicial['score_total']
    if score_inicial['score_total'] > 0:
        melhoria_percentual = ((melhoria / score_inicial['score_total']) * 100)
    else:
        # Se score inicial era 0, mostrar progresso em relação à meta de 80
        melhoria_percentual = (score_final['score_total'] / 80) * 100
    
    # Exibir comparação principal
    st.markdown("## 🎯 Score Total - Comparação")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Score Inicial",
            f"{score_inicial['score_total']:.1f}/100",
            delta=None,
            delta_color="off"
        )
        st.caption(f"Nível: {score_inicial['nivel']}")
    
    with col2:
        st.metric(
            "Score Final",
            f"{score_final['score_total']:.1f}/100",
            delta=f"+{melhoria:.1f}",
            delta_color="normal"
        )
        st.caption(f"Nível: {score_final['nivel']}")
    
    with col3:
        meta = 80
        if score_final['score_total'] >= meta:
            st.metric("Meta Atingida! 🎉", f"{meta}", delta="✅", delta_color="off")
        else:
            falta = meta - score_final['score_total']
            st.metric("Falta para Meta", f"{meta}", delta=f"-{falta:.1f}", delta_color="inverse")
    
    # Progress bars comparativas
    st.markdown("---")
    st.markdown("### 📈 Visualização da Melhoria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**ANTES**")
        st.progress(score_inicial['percentual'] / 100)
        st.caption(f"{score_inicial['percentual']:.1f}%")
    
    with col2:
        st.markdown("**DEPOIS**")
        st.progress(score_final['percentual'] / 100)
        st.caption(f"{score_final['percentual']:.1f}%")
    
    if melhoria > 0:
        st.success(f"🎉 **Melhoria de {melhoria:.1f} pontos ({melhoria_percentual:.1f}%)!**")
    elif melhoria == 0:
        st.info("ℹ️ Score mantido igual. Considere adicionar mais dados quantitativos.")
    else:
        st.warning(f"⚠️ Score diminuiu {abs(melhoria):.1f} pontos. Verifique o CV otimizado.")
    
    # Breakdown detalhado por categoria
    st.markdown("---")
    st.markdown("## 📋 Breakdown por Categoria")
    
    detalhes_inicial = score_inicial.get('detalhes', {})
    detalhes_final = score_final.get('detalhes', {})
    
    # Verificar se é análise LLM
    is_llm_inicial = detalhes_inicial.get('metodo', '').startswith('LLM')
    is_llm_final = detalhes_final.get('metodo', '').startswith('LLM')
    
    if is_llm_final or is_llm_inicial:
        # Se pelo menos um é LLM, mostrar informação
        st.info(
            "✨ **Análise via LLM (Inteligência Artificial)**\n\n"
            "A análise contextual não possui breakdown detalhado por categoria como o método TF-IDF. "
            "A pontuação é baseada em análise semântica profunda que entende o contexto e "
            "identifica habilidades específicas e gaps relevantes para o cargo."
        )
    else:
        # Ambos são TF-IDF - mostrar breakdown detalhado
        secoes_inicial = detalhes_inicial.get('secoes', {})
        secoes_final = detalhes_final.get('secoes', {})
        keywords_inicial = detalhes_inicial.get('keywords', {})
        keywords_final = detalhes_final.get('keywords', {})
        metricas_inicial = detalhes_inicial.get('metricas', {})
        metricas_final = detalhes_final.get('metricas', {})
        formatacao_inicial = detalhes_inicial.get('formatacao', {})
        formatacao_final = detalhes_final.get('formatacao', {})
        tamanho_inicial = detalhes_inicial.get('tamanho', {})
        tamanho_final = detalhes_final.get('tamanho', {})
        
        # Seções
        with st.expander("📑 Seções do CV", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Antes", f"{secoes_inicial.get('encontradas', 0)}/{secoes_inicial.get('total', 0)}")
            with col2:
                delta = secoes_final.get('encontradas', 0) - secoes_inicial.get('encontradas', 0)
                st.metric("Depois", f"{secoes_final.get('encontradas', 0)}/{secoes_final.get('total', 0)}", delta=f"+{delta}" if delta > 0 else delta)
        
        # Keywords
        with st.expander("🔑 Keywords Relevantes", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Antes", f"{keywords_inicial.get('encontradas', 0)}/{keywords_inicial.get('total', 0)}")
            with col2:
                delta = keywords_final.get('encontradas', 0) - keywords_inicial.get('encontradas', 0)
                st.metric("Depois", f"{keywords_final.get('encontradas', 0)}/{keywords_final.get('total', 0)}", delta=f"+{delta}" if delta > 0 else delta)
            
            if delta > 0:
                st.success(f"✅ {delta} novas keywords adicionadas!")
        
        # Métricas
        with st.expander("📊 Métricas Quantificáveis", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Antes", f"{metricas_inicial.get('quantidade', 0)} números")
            with col2:
                delta = metricas_final.get('quantidade', 0) - metricas_inicial.get('quantidade', 0)
                st.metric("Depois", f"{metricas_final.get('quantidade', 0)} números", delta=f"+{delta}" if delta > 0 else delta)
            
            if delta > 0:
                st.success(f"✅ {delta} novos dados quantificáveis adicionados!")
        
        # Formatação
        with st.expander("✏️ Formatação"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Bullets (Antes)", formatacao_inicial.get('bullets', 0))
                st.metric("Datas (Antes)", formatacao_inicial.get('datas', 0))
            with col2:
                st.metric("Bullets (Depois)", formatacao_final.get('bullets', 0))
                st.metric("Datas (Depois)", formatacao_final.get('datas', 0))
        
        # Tamanho
        with st.expander("📏 Tamanho do CV"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Antes", f"{tamanho_inicial.get('palavras', 0)} palavras")
            with col2:
                delta = tamanho_final.get('palavras', 0) - tamanho_inicial.get('palavras', 0)
                st.metric("Depois", f"{tamanho_final.get('palavras', 0)} palavras", delta=f"+{delta}" if delta > 0 else delta)
            st.caption(f"Ideal: {tamanho_final.get('ideal', 'N/A')}")
    
    # Gaps resolvidos
    st.markdown("---")
    st.markdown("## ✅ Gaps Resolvidos")
    
    gaps_alvo = st.session_state.get('gaps_alvo', [])
    if gaps_alvo:
        for i, gap in enumerate(gaps_alvo, 1):
            st.markdown(f"{i}. ✅ {gap}")
    else:
        st.info("Nenhum gap específico foi identificado inicialmente.")
    
    st.markdown("---")
    
    # Botões de navegação
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔵 Continuar para Otimização LinkedIn", use_container_width=True, type="primary"):
            st.session_state.fase = 'CHAT'
            st.session_state.etapa_modulo = 'ETAPA_6_LINKEDIN'
            forcar_topo()
            st.rerun()
    
    with col2:
        if st.button("📥 Ir para Exports", use_container_width=True):
            st.session_state.fase = 'FASE_EXPORTS_COMPLETO'
            st.rerun()
