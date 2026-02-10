"""Sidebar simplificada - apenas progresso visual."""
import streamlit as st
import logging

logger = logging.getLogger(__name__)


def renderizar_sidebar():
    """Renderiza sidebar com progresso visual apenas."""
    
    # Mapa de fases para exibição
    fases_display = {
        'FASE_0_INTRO': ('0️⃣', 'Introdução'),
        'FASE_0_UPLOAD': ('1️⃣', 'Upload de CV'),
        'FASE_1_DIAGNOSTICO': ('2️⃣', 'Diagnóstico'),
        'FASE_1_BRIEFING': ('3️⃣', 'Briefing'),
        'FASE_15_REALITY': ('4️⃣', 'Reality Check'),
        'CHAT': ('5️⃣', 'Headhunter Elite'),
        'FASE_VALIDACAO_SCORE_ATS': ('6️⃣', 'Validação ATS'),
        'FASE_EXPORTS_COMPLETO': ('7️⃣', 'Exports'),
    }
    
    fase_atual = st.session_state.get('fase', 'FASE_0_INTRO')
    emoji, nome = fases_display.get(fase_atual, ('❓', 'Desconhecida'))
    
    with st.sidebar:
        st.markdown("# 🎯 Protocolo Nóbile")
        
        # ── Usuário Logado ──
        if st.session_state.get('user'):
            st.caption(f"👤 {st.session_state.get('user')}")
        
        st.markdown("---")
        
        # ── Progresso Visual ──
        st.markdown("### 📍 Você está em:")
        st.info(f"**{emoji} {nome}**")
        
        st.markdown("---")

        # ── Perfil do Usuário (se disponível) ──
        if st.session_state.perfil.get('cargo_alvo'):
            st.markdown("### 📋 Seu Perfil")
            st.info(f"""
**Objetivo:** {st.session_state.perfil.get('objetivo', 'N/A')}
**Cargo:** {st.session_state.perfil['cargo_alvo']}
**Pretensão:** {st.session_state.perfil.get('pretensao_salarial', 'N/A')} mensal
**Local:** {st.session_state.perfil.get('localizacao', 'N/A')}
            """)
            st.markdown("---")
        
        # ── Glossário ──
        with st.expander("❓ Glossário de Termos"):
            st.markdown("""
            **ATS (Applicant Tracking System)**  
            Sistema automático que filtra CVs antes de chegarem ao recrutador.
            
            **Score ATS**  
            Nota 0-100 da compatibilidade do seu CV com sistemas automáticos:
            - 0-40: Precisa melhorias urgentes
            - 41-70: Pode ser melhorado
            - 71-100: Bem otimizado
            
            **Keywords (Palavras-Chave)**  
            Termos técnicos que sistemas ATS procuram (ex: "Python", "Liderança").
            
            **Método STAR**  
            Técnica para entrevistas:
            - **S**ituação
            - **T**arefa
            - **A**ção
            - **R**esultado
            
            **Reality Check**  
            Análise crítica identificando pontos fortes e fracos do CV.
            """)
        
        with st.expander("🎯 Para Quem é?"):
            st.markdown("""
            ✅ **Todos os níveis**:
            - Júnior / Trainee
            - Pleno / Sênior
            - Especialista / Líder
            - Gerente / Diretor
            - C-Level (CEO, CTO, etc.)
            
            ✅ **Todas as áreas**:
            Tech, Vendas, Marketing, RH, Financeiro, Operações, Design, etc.
            """)
        
        st.markdown("---")
        
        # ── Botão de Reiniciar (apenas se não estiver na intro) ──
        if fase_atual != 'FASE_0_INTRO':
            if st.button("🔄 Reiniciar Protocolo", use_container_width=True):
                logger.info("Usuário solicitou reiniciar protocolo")
                # Limpar TUDO exceto autenticação
                for key in list(st.session_state.keys()):
                    if key not in ['authenticated', 'api_key_hash', 'user', 'openai_client']:
                        del st.session_state[key]
                st.session_state.fase = 'FASE_0_INTRO'
                st.rerun()
        
        # ── Logout (se tiver função de logout) ──
        if st.button("🚪 Sair", type="secondary", use_container_width=True):
            from core.auth import logout
            logout()
            st.rerun()