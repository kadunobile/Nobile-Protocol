import streamlit as st
from core.utils import scroll_topo
from core.ats_scorer import calcular_score_ats, extrair_cargo_do_cv
from core.ats_constants import SKILL_DESCRIPTIONS

CARGO_FALLBACK = "Profissional"


def limpar_cache_ats():
    """Limpa o cache de score ATS do session_state."""
    for key in ['score_ats_inicial', 'cargo_atual']:
        if key in st.session_state:
            del st.session_state[key]


def fase_1_diagnostico():
    scroll_topo()
    
    # ─── Extrair cargo para o título ───
    cargo_atual = st.session_state.get('cargo_atual', CARGO_FALLBACK)
    
    st.markdown(f"# 🔍 Diagnóstico do Perfil — {cargo_atual}")
    st.markdown("---")
    
    # ─── Calcular ATS (apenas uma vez) ───
    if 'score_ats_inicial' not in st.session_state or 'cargo_atual' not in st.session_state:
        with st.spinner("📊 Analisando seu perfil com ATS inteligente..."):
            # Extrair cargo atual do CV
            cargo_atual = extrair_cargo_do_cv(
                st.session_state.openai_client,
                st.session_state.cv_texto
            )
            
            if not cargo_atual:
                cargo_atual = CARGO_FALLBACK
            
            st.session_state.cargo_atual = cargo_atual
            
            # Calcular score ATS completo
            resultado_ats = calcular_score_ats(
                st.session_state.cv_texto,
                cargo_atual,
                client=st.session_state.openai_client,
                objetivo=None,  # Ainda não definiu objetivo
                cargo_atual=cargo_atual  # Required to ensure same prompt generation as FASE_15_REALITY
            )
            
            st.session_state.score_ats_inicial = resultado_ats
    
    resultado = st.session_state.score_ats_inicial
    cargo_atual = st.session_state.cargo_atual
    score = resultado['score_total']
    nivel = resultado['nivel']
    
    # ─── Card de Score ATS ───
    if score >= 70:
        cor = "#2ecc71"
        emoji = "🟢"
    elif score >= 50:
        cor = "#f39c12"
        emoji = "🟡"
    elif score >= 30:
        cor = "#e67e22"
        emoji = "🟠"
    else:
        cor = "#e74c3c"
        emoji = "🔴"
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); border: 2px solid {cor}; 
                border-radius: 12px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
        <p style="margin: 0; font-size: 0.9rem; color: #aaa;">Score ATS para <strong>{cargo_atual}</strong></p>
        <p style="margin: 0.5rem 0; font-size: 3rem; font-weight: 700; color: {cor};">{score:.0f}<span style="font-size: 1.5rem; color: #888;">/100</span></p>
        <p style="margin: 0; font-size: 1.1rem; color: {cor};">{emoji} {nivel}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    st.info(
        "📊 **O que é o Score ATS?** É a compatibilidade do seu perfil com o que "
        "sistemas automatizados de recrutamento buscam para seu cargo atual. "
        "Quanto maior, mais chances de seu CV passar pelos filtros automáticos."
    )
    
    st.markdown("---")
    
    # ─── Pontos Fortes ───
    pontos_fortes = resultado.get('pontos_fortes', [])
    if pontos_fortes:
        st.markdown("### ✅ Pontos Fortes")
        st.markdown(
            "Termos do seu perfil que **já estão alinhados** com o que o mercado busca:"
        )
        # Mostrar como tags/chips
        tags_html = " ".join(
            f'<span style="background: rgba(46,204,113,0.15); color: #2ecc71; '
            f'padding: 4px 12px; border-radius: 20px; margin: 4px; '
            f'display: inline-block; font-size: 0.9rem;">{termo}</span>'
            for termo in pontos_fortes
        )
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("")
    
    # ─── Gaps com Descrições ───
    gaps = resultado.get('gaps_identificados', [])
    if gaps:
        st.markdown(f"### ❌ Skills que FALTAM no seu CV (exigidas para {cargo_atual})")
        st.markdown(
            "Termos importantes para o cargo que **não aparecem** no seu perfil:"
        )
        st.markdown("")
        
        # Criar lookup eficiente (lowercase)
        skill_descriptions_lower = {k.lower(): v for k, v in SKILL_DESCRIPTIONS.items()}
        
        for termo in gaps[:8]:
            # Extrair nome do gap (pode ser string simples ou dict)
            nome_gap = termo if isinstance(termo, str) else termo.get('nome', str(termo))
            
            # Buscar descrição da skill (O(1) lookup)
            descricao = skill_descriptions_lower.get(nome_gap.lower())
            
            # Fallback se skill não está no dicionário
            if not descricao:
                descricao = "Competência relevante para o cargo — pesquise mais sobre esta skill para entender como aplicá-la."
            
            st.markdown(f"""
<div style="background:#2a1a1a; border-left:3px solid #e74c3c; padding:10px 14px; border-radius:6px; margin:6px 0;">
    <div style="color:#e74c3c; font-weight:bold; font-size:0.95rem;">❌ {nome_gap}</div>
    <div style="color:#ccc; font-size:0.82rem; margin-top:4px;">
        📌 Skill exigida para <strong>{cargo_atual}</strong> — não encontrada no seu CV atual
    </div>
    <div style="color:#888; font-size:0.8rem; margin-top:6px; padding-top:6px; border-top:1px solid #333;">ℹ️ <strong>O que é:</strong> {descricao}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("")
    
    # ─── Transparência: Skills NÃO consideradas gaps (SEMPRE VISÍVEL) ───
    gaps_falsos = resultado.get('gaps_falsos_ignorados', [])
    st.markdown("**🔍 Transparência — Skills analisadas e DESCARTADAS como gaps:**")
    if gaps_falsos:
        st.caption("Nosso algoritmo analisou estas skills mas seu CV já as cobre adequadamente:")
        st.markdown("")
        
        # Renderizar como badges amarelos inline
        badges_html = ""
        for item in gaps_falsos[:8]:
            nome = item if isinstance(item, str) else item.get('nome', str(item))
            badges_html += (
                f"<span style='background:#3a3a1a; color:#facc15; padding:5px 12px; "
                f"border-radius:20px; font-size:0.85rem; display:inline-block; margin:4px;'>"
                f"🟡 {nome}</span>"
            )
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.caption(f"Nenhuma skill descartada como gap para este cargo.")
    st.markdown("")
    
    # ─── Plano de Ação ───
    plano = resultado.get('plano_acao', [])
    if plano:
        st.markdown("### 💡 Plano de Ação")
        for item in plano:
            st.markdown(item)
        st.markdown("")
    
    st.markdown("---")
    
    # ─── Botões ───
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Voltar", use_container_width=True):
            limpar_cache_ats()
            st.session_state.fase = 'FASE_0_UPLOAD'
            st.rerun()
    
    with col2:
        if st.button("🚀 PROSSEGUIR PARA BRIEFING", use_container_width=True, type="primary"):
            st.session_state.fase = 'FASE_1_BRIEFING'
            st.rerun()
