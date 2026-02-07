import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt

def renderizar_sidebar():
    with st.sidebar:
        st.markdown("# 🎯 Protocolo Nóbile")
        st.markdown("---")

        if st.session_state.perfil.get('cargo_alvo'):
            st.markdown("### 📋 Seu Perfil")
            st.info(f"""
**Objetivo:** {st.session_state.perfil.get('objetivo', 'N/A')}
**Cargo:** {st.session_state.perfil['cargo_alvo']}
**Pretensão:** {st.session_state.perfil.get('pretensao_salarial', 'N/A')} mensal
**Local:** {st.session_state.perfil.get('localizacao', 'N/A')}
            """)
            st.markdown("---")

        st.markdown("### ⚡ Comandos")
        habilitado = st.session_state.fase == 'CHAT'

        if st.button("🔧 Otimizar CV + LinkedIn", disabled=not habilitado, key="b1", use_container_width=True):
            # Reset state before transitioning to loading phase
            st.session_state.mensagens = []
            st.session_state.modulo_ativo = None
            st.session_state.etapa_modulo = None
            st.session_state.fase = 'FASE_ANALISE_LOADING'
            st.rerun()

        if st.button("🏢 Empresas Discovery", disabled=not habilitado, key="b2", use_container_width=True):
            with st.spinner("🔍 Buscando empresas..."):
                cargo = st.session_state.perfil.get('cargo_alvo', 'seu cargo')
                local = st.session_state.perfil.get('localizacao', 'Brasil')
                st.session_state.mensagens = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"""[/empresas_discovery]

Perfil:
- Cargo: {cargo}
- Local: {local}
- Pretensão: {st.session_state.perfil.get('pretensao_salarial', 'N/A')} mensal

Etapa 1: Pergunte sobre fit cultural.
Etapa 2: Liste 5-10 empresas com Match + Localização + Cultura.
Adicione o "Porquê" e Raio-X Salarial."""}
                ]
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
                    st.session_state.modulo_ativo = "EMPRESAS"
                    st.rerun()

        if st.button("🎯 Analisar Vaga (Fit)", disabled=not habilitado, key="b3", use_container_width=True):
            st.session_state.aguardando_vaga = True
            st.session_state.modulo_ativo = "FIT"
            st.info("👇 Cole a descrição da vaga no chat")

        if st.button("🎤 Prep. Entrevista", disabled=not habilitado, key="b4", use_container_width=True):
            with st.spinner("📚 Preparando..."):
                cargo = st.session_state.perfil.get('cargo_alvo', 'seu cargo')
                st.session_state.mensagens = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"""[/entrevista]

Cargo: {cargo}

Etapa 1: Dossiê + Talking Points
Etapa 2: Simulação STAR com 5 perguntas difíceis + respostas modelo"""}
                ]
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
                    st.session_state.modulo_ativo = "ENTREVISTA"
                    st.rerun()

        if st.button("📊 Análise Mercado", disabled=not habilitado, key="b5", use_container_width=True):
            with st.spinner("📈 Analisando..."):
                cargo = st.session_state.perfil.get('cargo_alvo', 'seu cargo')
                local = st.session_state.perfil.get('localizacao', 'Brasil')
                st.session_state.mensagens = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"""Analise mercado para {cargo} em {local}:
1. Tendências salariais
2. Skills em alta
3. Setores em crescimento
4. Certificações valorizadas"""}
                ]
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
                    st.session_state.modulo_ativo = "MERCADO"
                    st.rerun()

        if st.button("🤖 Score ATS", disabled=not habilitado, key="b_ats", use_container_width=True):
            st.session_state.fase = 'FASE_ATS_SCORE'
            st.rerun()

        st.markdown("### 📝 Ferramentas Avançadas")

        if st.button("✉️ Carta de Apresentação", disabled=not habilitado, key="b_carta", use_container_width=True):
            st.session_state.fase = 'FASE_CARTA'
            st.rerun()

        if st.button("🎤 Prep. Entrevista", disabled=not habilitado, key="b_interview", use_container_width=True):
            st.session_state.fase = 'FASE_INTERVIEW'
            st.rerun()

        if st.button("🔄 Comparar CVs", disabled=not habilitado, key="b_comparador", use_container_width=True):
            st.session_state.fase = 'FASE_COMPARADOR'
            st.rerun()

        st.markdown("---")
        
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
        if not habilitado:
            st.warning("⚠️ Complete o briefing para desbloquear")

        st.markdown("---")
        if st.button("🔄 Reiniciar Tudo", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()