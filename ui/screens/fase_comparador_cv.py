import streamlit as st
from core.ats_scorer import calcular_score_ats
import difflib

def fase_comparador_cv():
    st.markdown("# 🔄 Comparador de CVs")
    st.markdown("---")
    
    st.info("📊 Compare seu CV original com a versão otimizada")
    
    # Upload do CV otimizado
    st.markdown("### 📥 Upload do CV Otimizado")
    
    cv_otimizado_file = st.file_uploader(
        "Faça upload do seu CV após otimizações:",
        type=['txt'],
        help="Cole o conteúdo do seu CV otimizado em um arquivo .txt",
        key="cv_otimizado"
    )
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV original não encontrado. Faça upload primeiro.")
        return
    
    if cv_otimizado_file:
        cv_otimizado_texto = cv_otimizado_file.read().decode('utf-8')
        
        cargo = st.session_state.perfil.get('cargo_alvo', 'Cargo Geral')
        
        # Calcular scores
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📕 CV Original")
            score_original = calcular_score_ats(st.session_state.cv_texto, cargo)
            
            st.metric(
                "Score ATS",
                f"{score_original['score_total']}/100",
                help="Pontuação do CV original"
            )
            st.progress(score_original['score_total'] / 100)
            st.caption(f"Classificação: {score_original['nivel']}")
        
        with col2:
            st.markdown("### 📗 CV Otimizado")
            score_otimizado = calcular_score_ats(cv_otimizado_texto, cargo)
            
            diferenca = score_otimizado['score_total'] - score_original['score_total']
            st.metric(
                "Score ATS",
                f"{score_otimizado['score_total']}/100",
                delta=f"+{diferenca:.1f}" if diferenca > 0 else f"{diferenca:.1f}",
                delta_color="normal"
            )
            st.progress(score_otimizado['score_total'] / 100)
            st.caption(f"Classificação: {score_otimizado['nivel']}")
        
        st.markdown("---")
        
        # Comparação detalhada
        st.markdown("### 📊 Análise Comparativa Detalhada")
        
        categorias = {
            'secoes': ('Seções Essenciais', 20),
            'keywords': ('Palavras-Chave', 30),
            'metricas': ('Métricas Quantificáveis', 20),
            'formatacao': ('Formatação', 15),
            'tamanho': ('Tamanho Adequado', 15)
        }
        
        for key, (nome, max_pontos) in categorias.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{nome}**")
            
            with col2:
                score_orig = score_original['detalhes'][key]['score']
                st.caption(f"Original: {score_orig:.1f}/{max_pontos}")
            
            with col3:
                score_otim = score_otimizado['detalhes'][key]['score']
                diff = score_otim - score_orig
                emoji = "🟢" if diff > 0 else "🔴" if diff < 0 else "⚪"
                st.caption(f"Otimizado: {score_otim:.1f}/{max_pontos} {emoji}")
        
        st.markdown("---")
        
        # Visualização de diferenças (texto)
        st.markdown("### 🔍 Diferenças Textuais")
        
        tab1, tab2, tab3 = st.tabs(["📊 Resumo", "📝 Lado a Lado", "🔀 Diff Detalhado"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📕 CV Original**")
                st.metric("Palavras", len(st.session_state.cv_texto.split()))
                st.metric("Caracteres", len(st.session_state.cv_texto))
                st.metric("Números encontrados", len([c for c in st.session_state.cv_texto if c.isdigit()]))
            
            with col2:
                st.markdown("**📗 CV Otimizado**")
                st.metric("Palavras", len(cv_otimizado_texto.split()))
                st.metric("Caracteres", len(cv_otimizado_texto))
                st.metric("Números encontrados", len([c for c in cv_otimizado_texto if c.isdigit()]))
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📕 CV Original**")
                st.text_area("", st.session_state.cv_texto[:1000] + "...", height=400, key="orig_preview")
            
            with col2:
                st.markdown("**📗 CV Otimizado**")
                st.text_area("", cv_otimizado_texto[:1000] + "...", height=400, key="otim_preview")
        
        with tab3:
            # Diff usando difflib
            diff = difflib.unified_diff(
                st.session_state.cv_texto.splitlines(keepends=True),
                cv_otimizado_texto.splitlines(keepends=True),
                lineterm='',
                fromfile='CV Original',
                tofile='CV Otimizado'
            )
            
            diff_text = ''.join(diff)
            
            if diff_text:
                st.code(diff_text, language='diff')
            else:
                st.info("Nenhuma diferença detectada")
        
        st.markdown("---")
        
        # Recomendações finais
        if score_otimizado['score_total'] > score_original['score_total']:
            st.success(f"🎉 **Parabéns!** Seu CV melhorou {diferenca:.1f} pontos!")
            st.balloons()
        elif score_otimizado['score_total'] < score_original['score_total']:
            st.warning(f"⚠️ O CV otimizado pontuou {abs(diferenca):.1f} pontos a menos. Revise as mudanças.")
        else:
            st.info("📊 Ambos os CVs têm pontuação similar.")
    
    st.markdown("---")
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
