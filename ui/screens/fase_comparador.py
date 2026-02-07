import streamlit as st
from core.cv_comparator import comparar_cvs

def fase_comparador_cv():
    st.markdown("# 🔄 Comparador de CVs")
    st.markdown("---")
    
    st.info("📊 Compare seu CV original com a versão otimizada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 CV Original")
        cv_original = st.text_area(
            "Cole seu CV original",
            height=300,
            placeholder="Cole aqui o texto do seu CV antes das otimizações..."
        )
    
    with col2:
        st.markdown("### ✨ CV Otimizado")
        cv_otimizado = st.text_area(
            "Cole seu CV otimizado",
            height=300,
            placeholder="Cole aqui o texto do CV após otimizações..."
        )
    
    if st.button("🔍 Comparar CVs", type="primary", use_container_width=True):
        if not cv_original or not cv_otimizado:
            st.error("⚠️ Preencha ambos os campos")
            return
        
        with st.spinner("📊 Analisando diferenças..."):
            metricas = comparar_cvs(cv_original, cv_otimizado)
        
        st.markdown("---")
        st.markdown("### 📊 Relatório de Melhorias")
        
        # Métricas em cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta_palavras = metricas["palavras"]["depois"] - metricas["palavras"]["antes"]
            st.metric(
                "Palavras",
                metricas["palavras"]["depois"],
                delta=f"{delta_palavras:+d}",
                delta_color="normal"
            )
        
        with col2:
            delta_numeros = metricas["numeros"]["depois"] - metricas["numeros"]["antes"]
            st.metric(
                "Números/Métricas",
                metricas["numeros"]["depois"],
                delta=f"{delta_numeros:+d}",
                delta_color="normal" if delta_numeros >= 0 else "inverse"
            )
        
        with col3:
            delta_verbos = metricas["verbos_acao"]["depois"] - metricas["verbos_acao"]["antes"]
            st.metric(
                "Verbos de Ação",
                metricas["verbos_acao"]["depois"],
                delta=f"{delta_verbos:+d}",
                delta_color="normal" if delta_verbos >= 0 else "inverse"
            )
        
        with col4:
            delta_secoes = metricas["secoes"]["depois"] - metricas["secoes"]["antes"]
            st.metric(
                "Seções",
                metricas["secoes"]["depois"],
                delta=f"{delta_secoes:+d}",
                delta_color="normal" if delta_secoes >= 0 else "inverse"
            )
        
        # Gráficos de melhoria
        st.markdown("---")
        st.markdown("### 📈 Percentual de Melhoria")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Métricas Quantificáveis**")
            st.progress(min(metricas["numeros"]["melhoria"] / 100, 1.0))
            st.caption(f"+{metricas['numeros']['melhoria']}% em números e percentuais")
        
        with col2:
            st.markdown("**Linguagem Ativa**")
            st.progress(min(metricas["verbos_acao"]["melhoria"] / 100, 1.0))
            st.caption(f"+{metricas['verbos_acao']['melhoria']}% em verbos de ação")
        
        # Análise qualitativa
        st.markdown("---")
        st.markdown("### 💡 Análise Qualitativa")
        
        if metricas["numeros"]["melhoria"] > 50:
            st.success("✅ Excelente aumento de dados quantificáveis! Seu CV está muito mais impactante.")
        elif metricas["numeros"]["melhoria"] > 20:
            st.info("🟡 Boa melhoria em métricas. Considere adicionar mais números se possível.")
        else:
            st.warning("⚠️ Pouca melhoria quantitativa. Tente adicionar mais resultados com números.")
        
        if metricas["verbos_acao"]["melhoria"] > 30:
            st.success("✅ Linguagem muito mais ativa e impactante!")
        
        if metricas["secoes"]["depois"] >= 5:
            st.success("✅ CV bem estruturado com seções claras.")
        
        # Similaridade
        st.markdown("---")
        st.metric(
            "Similaridade com Original",
            f"{metricas['similaridade']}%",
            help="Quanto menor, mais mudanças foram feitas"
        )
    
    st.markdown("---")
    
    if st.button("⬅️ Voltar", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
