"""
Tela de Análise ATS (Applicant Tracking System).

Exibe pontuação detalhada de como sistemas automatizados de recrutamento
avaliariam o currículo do usuário.
"""

import streamlit as st
import logging
from core.ats_scorer import calcular_score_ats

# Configurar logger
logger = logging.getLogger(__name__)


def fase_ats_score():
    """
    Renderiza a tela de análise ATS.
    
    Mostra:
    - Score total e classificação
    - Breakdown detalhado por categoria
    - Recomendações de melhoria
    - Opções de navegação
    """
    st.markdown("# 🤖 Análise ATS - Applicant Tracking System")
    st.markdown("---")
    
    st.info("""
    **O que é ATS?**  
    ATS (Applicant Tracking System) é um sistema automático usado por empresas para filtrar currículos. 
    Seu CV precisa ter palavras-chave corretas, formatação adequada e informações relevantes para passar por esses sistemas.
    
    **Como funciona o Score?**
    - 0-40: ❌ Baixa chance (precisa melhorias urgentes)
    - 41-70: ⚠️ Média chance (pode ser melhorado)
    - 71-100: ✅ Alta chance (bem otimizado para ATS)
    """)
    
    st.markdown("📊 Simula como sistemas automatizados de recrutamento avaliam seu CV")
    
    # Validar se CV existe
    if not st.session_state.get('cv_texto'):
        logger.warning("Tentativa de acessar ATS score sem CV carregado")
        st.error("⚠️ CV não encontrado. Faça upload novamente.")
        
        if st.button("⬅️ Voltar ao Upload", use_container_width=True):
            st.session_state.fase = 'FASE_0_UPLOAD'
            st.rerun()
        return
    
    # Obter cargo alvo
    cargo = st.session_state.perfil.get('cargo_alvo', 'Cargo Geral')
    
    logger.info(f"Calculando score ATS para cargo: {cargo}")
    
    # Calcular score
    with st.spinner("🔍 Analisando CV com algoritmo ATS..."):
        try:
            # Pass OpenAI client to enable job variations and better JD generation
            resultado = calcular_score_ats(
                st.session_state.cv_texto, 
                cargo,
                client=st.session_state.get('openai_client')
            )
        except Exception as e:
            logger.error(f"Erro ao calcular score ATS: {e}", exc_info=True)
            st.error(f"❌ Erro ao calcular score: {e}")
            return
    
    # ===== SCORE PRINCIPAL =====
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score ATS", f"{resultado['score_total']}/100")
    
    with col2:
        st.metric("Percentual", f"{resultado['percentual']}%")
    
    with col3:
        nivel_emoji = {
            "Excelente": "🟢",
            "Bom": "🟡",
            "Regular": "🟠",
            "Precisa Melhorar": "🔴"
        }
        emoji = nivel_emoji.get(resultado['nivel'], '⚪')
        st.metric("Classificação", f"{emoji} {resultado['nivel']}")
    
    st.markdown("---")
    
    # ===== BREAKDOWN DETALHADO =====
    st.markdown("### 📋 Detalhamento da Pontuação")
    
    detalhes = resultado['detalhes']
    
    # 1. Seções Essenciais
    st.markdown(f"**1. Seções Essenciais:** {detalhes['secoes']['score']:.1f}/20 pontos")
    st.progress(detalhes['secoes']['score'] / 20)
    st.caption(f"✅ Encontradas: {detalhes['secoes']['encontradas']}/{detalhes['secoes']['total']}")
    st.markdown("")  # Espaço
    
    # 2. Palavras-Chave
    st.markdown(f"**2. Palavras-Chave:** {detalhes['keywords']['score']:.1f}/30 pontos")
    st.progress(detalhes['keywords']['score'] / 30)
    st.caption(f"📍 Encontradas: {detalhes['keywords']['encontradas']}/{detalhes['keywords']['total']}")
    if detalhes['keywords']['faltando']:
        faltando_str = ', '.join(detalhes['keywords']['faltando'][:5])
        st.caption(f"⚠️ Faltam: {faltando_str}")
    st.markdown("")
    
    # 3. Métricas Quantificáveis
    st.markdown(f"**3. Métricas Quantificáveis:** {detalhes['metricas']['score']:.1f}/20 pontos")
    st.progress(detalhes['metricas']['score'] / 20)
    st.caption(f"📊 Números encontrados: {detalhes['metricas']['quantidade']}")
    st.markdown("")
    
    # 4. Formatação
    st.markdown(f"**4. Formatação:** {detalhes['formatacao']['score']:.1f}/15 pontos")
    st.progress(detalhes['formatacao']['score'] / 15)
    st.caption(f"• Bullets: {detalhes['formatacao']['bullets']} | Datas: {detalhes['formatacao']['datas']}")
    st.markdown("")
    
    # 5. Tamanho
    st.markdown(f"**5. Tamanho:** {detalhes['tamanho']['score']:.1f}/15 pontos")
    st.progress(detalhes['tamanho']['score'] / 15)
    st.caption(f"📝 {detalhes['tamanho']['palavras']} palavras (ideal: {detalhes['tamanho']['ideal']})")
    
    st.markdown("---")
    
    # ===== RECOMENDAÇÕES =====
    st.markdown("### 💡 Recomendações para Melhorar")
    
    if resultado['percentual'] < 80:
        recomendacoes = []
        
        # Gerar recomendações específicas
        if detalhes['secoes']['score'] < 15:
            recomendacoes.append("• Adicione seções faltantes (Experiência, Educação, Habilidades, Contato)")
        
        if detalhes['keywords']['score'] < 20:
            keywords_faltando = detalhes['keywords']['faltando'][:3]
            if keywords_faltando:
                recomendacoes.append(f"• Inclua keywords importantes: {', '.join(keywords_faltando)}")
        
        if detalhes['metricas']['quantidade'] < 5:
            recomendacoes.append("• Adicione mais resultados quantificáveis (%, valores, números)")
        
        if detalhes['formatacao']['bullets'] < 5:
            recomendacoes.append("• Use mais bullet points para destacar conquistas")
        
        if detalhes['tamanho']['palavras'] < 300:
            recomendacoes.append("• CV muito curto. Expanda descrições de experiências")
        elif detalhes['tamanho']['palavras'] > 800:
            recomendacoes.append("• CV muito longo. Seja mais conciso e objetivo")
        
        # Exibir recomendações
        if recomendacoes:
            for rec in recomendacoes:
                st.warning(rec)
        else:
            st.info("✨ Seu CV está no caminho certo! Continue refinando.")
    else:
        st.success("✅ Seu CV está bem otimizado para ATS!")
        st.balloons()
    
    st.markdown("---")
    
    # ===== AÇÕES =====
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔧 Otimizar CV", use_container_width=True):
            logger.info("Navegando para otimização de CV")
            st.session_state.fase = 'CHAT'
            st.rerun()
    
    with col2:
        if st.button("⬅️ Voltar", use_container_width=True):
            logger.info("Retornando ao chat")
            st.session_state.fase = 'CHAT'
            st.rerun()
