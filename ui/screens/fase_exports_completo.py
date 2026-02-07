"""
Fase Exports Completo - Exports multi-formato + Analytics + Próximos Passos.

Esta fase oferece:
- Downloads: PDF, DOCX, TXT
- LinkedIn Ready-to-Use: Copiar Headline, Skills, About
- Comparador Antes/Depois visual
- Analytics: Keywords, Métricas, Tempo estimado
- Próximos Passos: Botões para outras funcionalidades
"""

import streamlit as st
from core.utils import forcar_topo
from modules.otimizador.helpers_export import (
    gerar_txt, 
    gerar_analytics_data, 
    formatar_comparacao_antes_depois,
    formatar_linkedin_ready
)


def fase_exports_completo():
    """
    Tela de exports completos e analytics.
    
    Oferece múltiplas opções de download, visualização de dados de LinkedIn,
    comparação detalhada antes/depois e sugestões de próximos passos.
    """
    # Forçar scroll ao topo
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    forcar_topo()
    
    st.markdown("# 📥 Exports & Analytics - Resultados Completos")
    st.markdown("---")
    
    # Verificar dados disponíveis
    cv_otimizado = st.session_state.get('cv_otimizado', st.session_state.get('cv_texto', ''))
    score_inicial = st.session_state.get('score_ats_inicial')
    score_final = st.session_state.get('score_ats_final')
    linkedin_data = st.session_state.get('linkedin_data', {})
    
    if not cv_otimizado:
        st.error("⚠️ CV otimizado não encontrado.")
        if st.button("🔙 Voltar"):
            st.session_state.fase = 'FASE_15_REALITY'
            st.rerun()
        return
    
    # Seção 1: Downloads
    st.markdown("## 📥 Downloads do CV Otimizado")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download TXT
        txt_data = gerar_txt(cv_otimizado)
        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name="cv_otimizado.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Download DOCX (placeholder - requires python-docx)
        st.button(
            "📝 Download DOCX",
            use_container_width=True,
            help="Funcionalidade em desenvolvimento",
            disabled=True
        )
    
    with col3:
        # Download PDF (placeholder - requires reportlab or similar)
        st.button(
            "📕 Download PDF",
            use_container_width=True,
            help="Funcionalidade em desenvolvimento",
            disabled=True
        )
    
    st.markdown("---")
    
    # Seção 2: LinkedIn Ready-to-Use
    st.markdown("## 🔵 LinkedIn Ready-to-Use")
    
    if linkedin_data:
        # Headline
        if linkedin_data.get('headline'):
            st.markdown("### 🎯 Headline Escolhida")
            st.code(linkedin_data['headline'], language=None)
            st.caption("👆 Copie e cole no campo 'Headline' do seu perfil LinkedIn")
        
        # Skills
        if linkedin_data.get('skills'):
            st.markdown("### 🛠️ Top Skills (em ordem)")
            skills_text = "\n".join([f"{i}. {skill}" for i, skill in enumerate(linkedin_data['skills'][:10], 1)])
            st.code(skills_text, language=None)
            st.caption("👆 Adicione essas skills no LinkedIn na ordem mostrada")
        
        # About
        if linkedin_data.get('about'):
            st.markdown("### 📝 About Section")
            st.code(linkedin_data['about'], language=None)
            st.caption("👆 Copie e cole na seção 'Sobre' do seu perfil LinkedIn")
        
        # Conquistas por experiência
        if linkedin_data.get('conquistas'):
            with st.expander("🏆 Conquistas por Experiência"):
                st.markdown(linkedin_data['conquistas'])
    else:
        st.info("ℹ️ Dados de LinkedIn não disponíveis. Complete a etapa de Otimização LinkedIn primeiro.")
        if st.button("🔵 Ir para Otimização LinkedIn"):
            st.session_state.fase = 'CHAT'
            st.session_state.etapa_modulo = 'ETAPA_6_LINKEDIN'
            st.rerun()
    
    st.markdown("---")
    
    # Seção 3: Comparador Antes/Depois
    st.markdown("## 📊 Comparador Antes × Depois")
    
    if score_inicial and score_final:
        # Gerar analytics
        gaps_alvo = st.session_state.get('gaps_alvo', [])
        analytics = gerar_analytics_data(score_inicial, score_final, gaps_alvo)
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Melhoria Total",
                f"+{analytics['score_melhoria']:.1f}",
                f"{analytics['score_melhoria_percentual']:.1f}%"
            )
        
        with col2:
            st.metric(
                "Keywords",
                f"+{analytics['keywords_adicionadas']}",
                "adicionadas"
            )
        
        with col3:
            st.metric(
                "Métricas",
                f"+{analytics['metricas_adicionadas']}",
                "inseridas"
            )
        
        with col4:
            st.metric(
                "Gaps",
                f"{analytics['gaps_resolvidos']}",
                "resolvidos"
            )
        
        # Comparação detalhada
        with st.expander("📋 Ver Comparação Detalhada"):
            comparacao_texto = formatar_comparacao_antes_depois(score_inicial, score_final)
            st.markdown(comparacao_texto)
        
        # Status da meta
        if analytics['atingiu_meta']:
            st.success("🎉 **Meta de 80 pontos atingida!** Seu CV está otimizado para ATS.")
        else:
            falta = 80 - score_final['score_total']
            st.info(f"ℹ️ Faltam {falta:.1f} pontos para atingir a meta de 80. Considere adicionar mais dados quantitativos.")
    else:
        st.warning("⚠️ Comparação não disponível. Scores inicial ou final não encontrados.")
    
    st.markdown("---")
    
    # Seção 4: Analytics
    st.markdown("## 📈 Analytics da Otimização")
    
    if score_inicial and score_final:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔑 Keywords")
            st.markdown(f"- **Antes:** {score_inicial['detalhes']['keywords']['encontradas']}")
            st.markdown(f"- **Depois:** {score_final['detalhes']['keywords']['encontradas']}")
            st.markdown(f"- **Adicionadas:** {analytics['keywords_adicionadas']}")
            
            if score_final['detalhes']['keywords'].get('faltando'):
                with st.expander("Keywords ainda faltando"):
                    for kw in score_final['detalhes']['keywords']['faltando'][:5]:
                        st.markdown(f"- {kw}")
        
        with col2:
            st.markdown("### 📊 Métricas")
            st.markdown(f"- **Antes:** {score_inicial['detalhes']['metricas']['quantidade']} números")
            st.markdown(f"- **Depois:** {score_final['detalhes']['metricas']['quantidade']} números")
            st.markdown(f"- **Adicionadas:** {analytics['metricas_adicionadas']}")
        
        st.markdown("### ⏱️ Tempo Estimado de Resultado")
        st.info("""
        Com seu CV otimizado e LinkedIn atualizado:
        - **Candidaturas:** 2-3x mais chances de passar no ATS
        - **Respostas:** Espere feedback em 1-2 semanas
        - **Entrevistas:** Potencial de 30-50% mais convites
        """)
    
    st.markdown("---")
    
    # Seção 5: Próximos Passos
    st.markdown("## 🚀 Próximos Passos Recomendados")
    
    st.markdown("""
    Agora que seu CV e LinkedIn estão otimizados, sugerimos:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Encontrar Vagas Compatíveis", use_container_width=True):
            st.info("🔧 Funcionalidade em desenvolvimento")
        
        if st.button("🎤 Preparação para Entrevistas", use_container_width=True):
            st.session_state.fase = 'FASE_INTERVIEW'
            st.rerun()
    
    with col2:
        if st.button("💰 Análise Salarial", use_container_width=True):
            st.info("🔧 Funcionalidade em desenvolvimento")
        
        if st.button("📚 Plano de Upskilling", use_container_width=True):
            st.info("🔧 Funcionalidade em desenvolvimento")
    
    st.markdown("---")
    
    # Opções finais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Ver Reality Check", use_container_width=True):
            st.session_state.fase = 'FASE_15_REALITY'
            st.rerun()
    
    with col2:
        if st.button("📊 Ver Score ATS", use_container_width=True):
            st.session_state.fase = 'FASE_VALIDACAO_SCORE_ATS'
            st.rerun()
    
    with col3:
        if st.button("💬 Chat com IA", use_container_width=True):
            st.session_state.fase = 'CHAT'
            st.rerun()
