import streamlit as st
import difflib
from core.ats_scorer import calcular_score_ats

# Constants
PREVIEW_MAX_LENGTH = 1000

def fase_comparador_cv():
    st.markdown("# 🔄 Comparador de CVs")
    st.markdown("---")
    
    st.info("📊 Compare seu CV original com a versão otimizada e veja as melhorias no Score ATS")
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV original não encontrado. Faça upload primeiro.")
        return
    
    # Upload do CV otimizado
    st.markdown("### 📄 Upload do CV Otimizado")
    uploaded_file = st.file_uploader(
        "Faça upload do seu CV otimizado (.txt)",
        type=['txt'],
        help="Selecione o arquivo .txt com seu CV otimizado"
    )
    
    if uploaded_file is not None:
        # Lê o conteúdo do arquivo
        cv_otimizado = uploaded_file.read().decode('utf-8')
        
        cargo_alvo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
        
        with st.spinner("📊 Calculando scores ATS e analisando diferenças..."):
            # Calcula scores ATS
            score_original = calcular_score_ats(st.session_state.cv_texto, cargo_alvo)
            score_otimizado = calcular_score_ats(cv_otimizado, cargo_alvo)
            
            # Calcula delta
            delta_score = score_otimizado['score_total'] - score_original['score_total']
        
        st.markdown("---")
        st.markdown("## 📊 Comparação de Score ATS")
        
        # Métricas principais com delta
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Score ATS Original",
                f"{score_original['score_total']:.0f}/100",
                help="Pontuação do CV original"
            )
            st.progress(score_original['score_total'] / 100)
        
        with col2:
            st.metric(
                "Score ATS Otimizado",
                f"{score_otimizado['score_total']:.0f}/100",
                delta=f"{delta_score:+.0f}",
                delta_color="normal" if delta_score >= 0 else "inverse",
                help="Pontuação do CV otimizado"
            )
            st.progress(score_otimizado['score_total'] / 100)
        
        with col3:
            st.metric(
                "Melhoria",
                f"{abs(delta_score):.0f} pontos",
                help="Diferença absoluta entre os scores"
            )
            if delta_score > 0:
                st.success("🟢 Melhorou!")
            elif delta_score < 0:
                st.error("🔴 Piorou")
            else:
                st.info("⚪ Manteve igual")
        
        # Análise detalhada por categoria
        st.markdown("---")
        st.markdown("### 📋 Análise Detalhada por Categoria")
        
        categorias = [
            ('Seções Essenciais', 'secoes', 20),
            ('Palavras-Chave', 'keywords', 30),
            ('Métricas Quantificáveis', 'metricas', 20),
            ('Formatação', 'formatacao', 15),
            ('Tamanho Adequado', 'tamanho', 15)
        ]
        
        for nome, chave, max_pts in categorias:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            orig_val = score_original['breakdown'][chave]
            otim_val = score_otimizado['breakdown'][chave]
            delta_val = otim_val - orig_val
            
            with col1:
                st.markdown(f"**{nome}** (máx: {max_pts} pts)")
            
            with col2:
                st.text(f"{orig_val:.1f}")
            
            with col3:
                st.text(f"{otim_val:.1f}")
            
            with col4:
                if delta_val > 0:
                    st.markdown("🟢")
                elif delta_val < 0:
                    st.markdown("🔴")
                else:
                    st.markdown("⚪")
        
        # Tabs de visualização
        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📊 Resumo", "📝 Lado a Lado", "🔀 Diff Detalhado"])
        
        with tab1:
            st.markdown("### 📊 Estatísticas Resumidas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### CV Original")
                palavras_orig = len(st.session_state.cv_texto.split())
                chars_orig = len(st.session_state.cv_texto)
                digitos_orig = len([c for c in st.session_state.cv_texto if c.isdigit()])
                
                st.metric("Palavras", palavras_orig)
                st.metric("Caracteres", chars_orig)
                st.metric("Dígitos", digitos_orig)
            
            with col2:
                st.markdown("#### CV Otimizado")
                palavras_otim = len(cv_otimizado.split())
                chars_otim = len(cv_otimizado)
                digitos_otim = len([c for c in cv_otimizado if c.isdigit()])
                
                st.metric("Palavras", palavras_otim, delta=palavras_otim - palavras_orig)
                st.metric("Caracteres", chars_otim, delta=chars_otim - chars_orig)
                st.metric("Dígitos", digitos_otim, delta=digitos_otim - digitos_orig)
        
        with tab2:
            st.markdown("### 📝 Visualização Lado a Lado")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📄 CV Original (preview)")
                preview_orig = st.session_state.cv_texto[:PREVIEW_MAX_LENGTH] + ('...' if len(st.session_state.cv_texto) > PREVIEW_MAX_LENGTH else '')
                st.text_area("", value=preview_orig, height=400, key="preview_orig", disabled=True)
            
            with col2:
                st.markdown("#### ✨ CV Otimizado (preview)")
                preview_otim = cv_otimizado[:PREVIEW_MAX_LENGTH] + ('...' if len(cv_otimizado) > PREVIEW_MAX_LENGTH else '')
                st.text_area("", value=preview_otim, height=400, key="preview_otim", disabled=True)
        
        with tab3:
            st.markdown("### 🔀 Diff Detalhado (Unified Diff)")
            st.caption("Linhas removidas em vermelho (-), linhas adicionadas em verde (+)")
            
            # Gera unified diff
            diff = difflib.unified_diff(
                st.session_state.cv_texto.splitlines(keepends=True),
                cv_otimizado.splitlines(keepends=True),
                fromfile='CV Original',
                tofile='CV Otimizado',
                lineterm=''
            )
            
            diff_text = ''.join(diff)
            
            if diff_text:
                st.code(diff_text, language='diff')
            else:
                st.info("Os CVs são idênticos - nenhuma diferença encontrada.")
        
        # Recomendações finais
        st.markdown("---")
        st.markdown("### 💡 Recomendações")
        
        if delta_score >= 10:
            st.balloons()
            st.success(f"""
            ✅ **Excelente melhoria!** Seu CV otimizado subiu **{delta_score:.0f} pontos** no Score ATS.
            
            Principais avanços:
            - Score passou de {score_original['score_total']:.0f} para {score_otimizado['score_total']:.0f}
            - Maior chance de passar por sistemas automatizados
            - CV mais competitivo no mercado
            """)
        elif delta_score >= 5:
            st.success(f"""
            ✅ **Boa melhoria!** Seu CV otimizado subiu **{delta_score:.0f} pontos**.
            
            Continue refinando para alcançar scores ainda mais altos.
            """)
        elif delta_score > -5 and delta_score < 5:
            st.info(f"""
            ℹ️ **Pontuação similar** (diferença de {abs(delta_score):.0f} pontos).
            
            As mudanças foram pequenas. Considere:
            - Adicionar mais métricas quantificáveis
            - Incluir palavras-chave relevantes
            - Verificar formatação e estrutura
            """)
        else:
            st.warning(f"""
            ⚠️ **Atenção!** O CV otimizado teve uma queda de **{abs(delta_score):.0f} pontos**.
            
            Revise as mudanças feitas:
            - Verifique se não removeu seções importantes
            - Confirme que palavras-chave estão presentes
            - Valide a formatação do documento
            """)
    
    else:
        st.warning("👆 Faça upload do CV otimizado para começar a comparação")
    
    st.markdown("---")
    
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
