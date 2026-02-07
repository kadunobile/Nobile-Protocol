"""
Fase Bridge Otimização - Ponte estratégica entre Reality Check e Otimização de CV.

Esta fase mostra:
- Score ATS inicial do CV atual
- Resumo dos 3 gaps críticos do Reality Check
- Meta esperada de score (padrão: 80)
- Confirmação para iniciar otimização
"""

import streamlit as st
from core.ats_scorer import calcular_score_ats
from core.utils import forcar_topo


def fase_bridge_otimizacao():
    """
    Tela de ponte estratégica que conecta Reality Check com o processo de otimização.
    
    Calcula e exibe o score ATS inicial, extrai gaps do Reality Check e
    prepara o usuário para iniciar o processo de otimização.
    """
    # Forçar scroll ao topo
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    forcar_topo()
    
    st.markdown("# 🌉 Ponte Estratégica - Preparação para Otimização")
    st.markdown("---")
    
    # Verificar se temos CV e Reality Check
    if not st.session_state.get('cv_texto'):
        st.error("⚠️ CV não encontrado. Por favor, faça upload do CV novamente.")
        if st.button("🔙 Voltar para Upload"):
            st.session_state.fase = 'FASE_0_UPLOAD'
            st.rerun()
        return
    
    # Calcular Score ATS inicial se ainda não foi calculado
    if st.session_state.get('score_ats_inicial') is None:
        with st.spinner("📊 Calculando Score ATS do seu CV atual..."):
            cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
            score_resultado = calcular_score_ats(
                st.session_state.cv_texto, 
                cargo
            )
            st.session_state.score_ats_inicial = score_resultado
    
    score_inicial = st.session_state.score_ats_inicial
    
    # Exibir Score ATS Inicial
    st.markdown("## 📊 Score ATS do Seu CV Atual")
    
    # Criar visualização do score
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Progress bar para o score
        score_percentual = score_inicial['percentual']
        if score_percentual >= 80:
            cor = "🟢"
        elif score_percentual >= 60:
            cor = "🟡"
        else:
            cor = "🔴"
        
        st.markdown(f"### {cor} Score Atual: {score_inicial['score_total']}/100")
        st.progress(score_percentual / 100)
        st.markdown(f"**Nível:** {score_inicial['nivel']}")
    
    with col2:
        st.metric("Meta", "80", delta=None)
    
    with col3:
        diferenca = 80 - score_inicial['score_total']
        if diferenca > 0:
            st.metric("A Ganhar", f"+{diferenca:.1f}", delta=diferenca, delta_color="normal")
        else:
            st.metric("Acima da Meta", f"{abs(diferenca):.1f}", delta=abs(diferenca), delta_color="inverse")
    
    st.markdown("---")
    
    # Breakdown do Score
    st.markdown("### 📋 Detalhamento do Score")
    
    detalhes = score_inicial['detalhes']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Seções do CV**")
        secoes = detalhes['secoes']
        st.progress(secoes['score'] / 20)
        st.caption(f"{secoes['encontradas']}/{secoes['total']} seções encontradas")
        
        st.markdown("**Keywords Relevantes**")
        keywords = detalhes['keywords']
        st.progress(keywords['score'] / 30)
        st.caption(f"{keywords['encontradas']}/{keywords['total']} keywords presentes")
        if keywords.get('faltando'):
            with st.expander("Ver keywords faltando"):
                for kw in keywords['faltando'][:5]:
                    st.markdown(f"- {kw}")
        
        st.markdown("**Métricas Quantificáveis**")
        metricas = detalhes['metricas']
        st.progress(metricas['score'] / 20)
        st.caption(f"{metricas['quantidade']} números/métricas encontrados")
    
    with col2:
        st.markdown("**Formatação**")
        formatacao = detalhes['formatacao']
        st.progress(formatacao['score'] / 15)
        st.caption(f"{formatacao['bullets']} bullets, {formatacao['datas']} datas")
        
        st.markdown("**Tamanho do CV**")
        tamanho = detalhes['tamanho']
        st.progress(tamanho['score'] / 15)
        st.caption(f"{tamanho['palavras']} palavras (ideal: {tamanho['ideal']})")
    
    st.markdown("---")
    
    # Extrair gaps do Reality Check
    st.markdown("## 🎯 Gaps Identificados no Reality Check")
    
    reality_text = st.session_state.get('reality_check_resultado', '')
    
    # Tentar extrair gaps do texto do reality check
    # Procurar por seção de gaps ou pontos fracos
    gaps = []
    if reality_text and ('gap' in reality_text.lower() or 'lacuna' in reality_text.lower()):
        # Extrair algumas linhas que mencionam gaps
        linhas = reality_text.split('\n')
        for linha in linhas:
            if any(palavra in linha.lower() for palavra in ['gap', 'lacuna', 'falta', 'ausência', 'carece']):
                gaps.append(linha.strip())
        
        # Limitar a 3 gaps principais
        gaps = gaps[:3]
    
    # Se não encontrou gaps, usar genéricos baseados no score
    if not gaps:
        if detalhes['keywords']['score'] < 20:
            gaps.append("⚠️ Faltam keywords estratégicas para o cargo")
        if detalhes['metricas']['quantidade'] < 5:
            gaps.append("⚠️ Poucos resultados quantificáveis demonstrados")
        if detalhes['secoes']['encontradas'] < 4:
            gaps.append("⚠️ Estrutura do CV incompleta")
    
    st.session_state.gaps_alvo = gaps
    
    if gaps:
        for i, gap in enumerate(gaps, 1):
            st.markdown(f"{i}. {gap}")
    else:
        st.success("✅ Nenhum gap crítico identificado! Mas ainda podemos melhorar seu CV.")
    
    st.markdown("---")
    
    # Informações sobre o processo
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
    
    # Botões de ação
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Iniciar Otimização Completa", use_container_width=True, type="primary"):
            # Preparar para iniciar otimização
            st.session_state.modulo_ativo = 'OTIMIZADOR'
            st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO'
            st.session_state.mensagens = []
            st.session_state.fase = 'CHAT'
            forcar_topo()
            st.rerun()
    
    with col2:
        if st.button("🔙 Voltar", use_container_width=True):
            st.session_state.fase = 'FASE_15_REALITY'
            st.rerun()
