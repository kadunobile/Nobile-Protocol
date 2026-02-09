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
            resultado = calcular_score_ats(st.session_state.cv_texto, cargo)
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
    
    # Verificar se é análise LLM (não tem breakdown detalhado)
    is_llm_analysis = detalhes.get('metodo', '').startswith('LLM')
    
    if is_llm_analysis:
        # Para análise LLM, mostrar informação sobre o método
        st.info(
            f"✨ **Análise Contextual via {detalhes.get('modelo', 'LLM')}**\n\n"
            "Esta análise usa inteligência artificial para entender o contexto do seu CV, "
            "identificando habilidades específicas e gaps relevantes para o cargo.\n\n"
            "Os pontos fortes e gaps identificados são baseados em análise semântica profunda, "
            "não apenas em palavras-chave."
        )
        st.markdown("")
    else:
        # Análise TF-IDF - mostrar breakdown detalhado se disponível
        secoes = detalhes.get('secoes', {})
        keywords = detalhes.get('keywords', {})
        metricas = detalhes.get('metricas', {})
        formatacao = detalhes.get('formatacao', {})
        tamanho = detalhes.get('tamanho', {})
        
        if secoes and keywords and metricas and formatacao and tamanho:
            # 1. Seções Essenciais
            st.markdown(f"**1. Seções Essenciais:** {secoes.get('score', 0):.1f}/20 pontos")
            st.progress(secoes.get('score', 0) / 20)
            st.caption(f"✅ Encontradas: {secoes.get('encontradas', 0)}/{secoes.get('total', 0)}")
            st.markdown("")  # Espaço
            
            # 2. Palavras-Chave
            st.markdown(f"**2. Palavras-Chave:** {keywords.get('score', 0):.1f}/30 pontos")
            st.progress(keywords.get('score', 0) / 30)
            st.caption(f"📍 Encontradas: {keywords.get('encontradas', 0)}/{keywords.get('total', 0)}")
            if keywords.get('faltando', []):
                faltando_str = ', '.join(keywords['faltando'][:5])
                st.caption(f"⚠️ Faltam: {faltando_str}")
            st.markdown("")
            
            # 3. Métricas Quantificáveis
            st.markdown(f"**3. Métricas Quantificáveis:** {metricas.get('score', 0):.1f}/20 pontos")
            st.progress(metricas.get('score', 0) / 20)
            st.caption(f"📊 Números encontrados: {metricas.get('quantidade', 0)}")
            st.markdown("")
            
            # 4. Formatação
            st.markdown(f"**4. Formatação:** {formatacao.get('score', 0):.1f}/15 pontos")
            st.progress(formatacao.get('score', 0) / 15)
            st.caption(f"• Bullets: {formatacao.get('bullets', 0)} | Datas: {formatacao.get('datas', 0)}")
            st.markdown("")
            
            # 5. Tamanho
            st.markdown(f"**5. Tamanho:** {tamanho.get('score', 0):.1f}/15 pontos")
            st.progress(tamanho.get('score', 0) / 15)
            st.caption(f"📝 {tamanho.get('palavras', 0)} palavras (ideal: {tamanho.get('ideal', 'N/A')})")
        else:
            # Fallback se não houver breakdown detalhado
            st.info(
                f"**Método de Análise:** {detalhes.get('metodo', 'N/A')}\n\n"
                "Análise simplificada sem breakdown detalhado disponível."
            )
    
    st.markdown("---")
    
    # ===== SKILLS ENCONTRADAS E GAPS (v5.0) =====
    # Display skills only for LLM analysis that has these fields
    if is_llm_analysis and resultado.get('pontos_fortes'):
        st.markdown("### ✅ Skills Encontradas no CV")
        pontos_fortes = resultado.get('pontos_fortes', [])
        if pontos_fortes:
            for i, termo in enumerate(pontos_fortes[:8]):
                st.markdown(f"<span style='background:#1a472a; color:#4ade80; padding:4px 10px; border-radius:20px; font-size:0.85rem; white-space:nowrap; display:inline-block; margin:4px;'>✅ {termo}</span>", unsafe_allow_html=True)
        st.markdown("")
    
    if is_llm_analysis and resultado.get('gaps_identificados'):
        st.markdown("### ❌ Skills Faltantes")
        gaps = resultado.get('gaps_identificados', [])
        if gaps:
            for i, termo in enumerate(gaps[:10]):
                st.markdown(f"<span style='background:#4a1a1a; color:#f87171; padding:4px 10px; border-radius:20px; font-size:0.85rem; white-space:nowrap; display:inline-block; margin:4px;'>❌ {termo}</span>", unsafe_allow_html=True)
        st.markdown("")
    
    # ── Transparência: Skills NÃO consideradas gaps ──
    if is_llm_analysis and resultado.get('gaps_falsos_ignorados'):
        gaps_falsos = resultado.get('gaps_falsos_ignorados', [])
        if gaps_falsos:
            with st.expander("🔍 Transparência: Skills que NÃO foram consideradas gaps"):
                st.caption("Estas skills foram analisadas mas **descartadas** como gaps:")
                for item in gaps_falsos[:8]:
                    st.markdown(f"- 🟡 {item}")
            st.markdown("")
    
    st.markdown("---")
    
    # ===== RECOMENDAÇÕES =====
    st.markdown("### 💡 Recomendações para Melhorar")
    
    if resultado['percentual'] < 80:
        recomendacoes = []
        
        # Para análise LLM, usar plano de ação
        if is_llm_analysis:
            if resultado.get('plano_acao'):
                for acao in resultado['plano_acao']:
                    st.warning(acao)
            else:
                st.info("✨ Seu CV está no caminho certo! Continue refinando.")
        else:
            # Gerar recomendações específicas baseadas em breakdown (TF-IDF)
            secoes = detalhes.get('secoes', {})
            keywords = detalhes.get('keywords', {})
            metricas = detalhes.get('metricas', {})
            formatacao = detalhes.get('formatacao', {})
            tamanho = detalhes.get('tamanho', {})
            
            if secoes.get('score', 0) < 15:
                recomendacoes.append("• Adicione seções faltantes (Experiência, Educação, Habilidades, Contato)")
            
            if keywords.get('score', 0) < 20:
                keywords_faltando = keywords.get('faltando', [])[:3]
                if keywords_faltando:
                    recomendacoes.append(f"• Inclua keywords importantes: {', '.join(keywords_faltando)}")
            
            if metricas.get('quantidade', 0) < 5:
                recomendacoes.append("• Adicione mais resultados quantificáveis (%, valores, números)")
            
            if formatacao.get('bullets', 0) < 5:
                recomendacoes.append("• Use mais bullet points para destacar conquistas")
            
            if tamanho.get('palavras', 0) < 300:
                recomendacoes.append("• CV muito curto. Expanda descrições de experiências")
            elif tamanho.get('palavras', 0) > 800:
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
