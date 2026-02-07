import streamlit as st
from core.utils import scroll_topo, filtrar_cidades

def fase_1_briefing():
    scroll_topo()
    st.markdown("# 🎯 Briefing Estratégico")
    st.markdown("---")
    st.markdown("**Para traçar a estratégia correta, responda apenas:**")

    with st.form("briefing"):
        # Use responsive columns: 2 columns on desktop, 1 on mobile
        col1, col2 = st.columns([1, 1])

        with col1:
            p1 = st.selectbox("**P1. Objetivo Principal:**",
                ["", "Recolocação no Mercado", "Transição de Carreira", "Promoção Interna", "Trabalho Internacional"])
            p2 = st.text_input("**P2. Cargo que você procura:**",
                placeholder="Ex: Gerente de Vendas")

        with col2:
            p3 = st.number_input("**P3. Pretensão Salarial (mensal):**",
                min_value=0, step=1000, format="%d",
                help="Apenas números. Valor mensal")
            p4 = st.text_input("**P4. Localização (Cidade/Remoto):**",
                placeholder="Digite a cidade")

        if p4:
            sugestoes = filtrar_cidades(p4)
            if sugestoes:
                st.info(f"💡 {', '.join(sugestoes[:5])}")

        remoto = st.checkbox("📍 Aceito trabalho 100% remoto")

        if st.form_submit_button("🚀 EXECUTAR REALITY CHECK", use_container_width=True):
            if p1 and p2 and p3 > 0 and p4:
                st.session_state.mensagens = []
                st.session_state.modulo_ativo = None
                st.session_state.etapa_modulo = None
                st.session_state.force_scroll_top = True

                st.session_state.perfil = {
                    'objetivo': p1,
                    'cargo_alvo': p2,
                    'pretensao_salarial': f"{p3:,}".replace(",", "."),
                    'localizacao': p4,
                    'remoto': remoto
                }
                st.session_state.fase = 'FASE_15_REALITY'
                st.rerun()
            else:
                st.error("⚠️ Preencha todos os campos (P1 a P4)")