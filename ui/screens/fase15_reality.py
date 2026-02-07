import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt, scroll_topo, forcar_topo

def fase_15_reality_check():
    # Add top anchor for scroll positioning
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    scroll_topo()
    st.markdown("# 🧠 Reality Check - Análise Crítica")
    st.markdown("---")
    
    st.info("""
    **O que é Reality Check?**  
    Uma análise honesta e detalhada do seu CV, identificando:
    - ✅ Pontos fortes que você deve enfatizar
    - ❌ Gaps (lacunas) que precisam ser corrigidos
    - 💡 Oportunidades de melhoria
    
    Esta análise funciona para **qualquer cargo**: júnior, pleno, sênior, gerente, diretor, etc.
    """)

    with st.spinner("🧠 Cruzando CV × Cargo × Salário × Região..."):
        perfil = st.session_state.perfil
        pretensao = perfil['pretensao_salarial']
        cargo = perfil['cargo_alvo']
        local = perfil['localizacao']

        msgs = [
            {"role": "system", "content": SYSTEM_PROMPT + f"""

INSTRUÇÕES INTERNAS (NÃO MOSTRAR AO USUÁRIO):

⚠️ REGRA CRÍTICA ao mencionar gaps:
- ANTES de marcar algo como gap, busque sinônimos e variações no CV do candidato
  * Ex: "liderança" pode aparecer como "gestão de equipe", "coordenação"
  * Ex: "Python" pode estar em "automação", "scripts", "análise de dados"
- Só mencione como gap se NÃO encontrado em NENHUMA forma (literal ou contextual)
- APENAS mencione gaps diretamente relacionados ao cargo {cargo}
- Gaps devem ser corrigíveis (não invente barreiras inexistentes)
- Relevância para o mercado de {local}

❌ NÃO MENCIONE:
- "Falta experiência internacional" (removido - não é relevante para a maioria dos cargos)
- "Falta conhecimento em [tecnologia X]" (a menos que seja padrão obrigatório no cargo)
- Gaps genéricos de livros de carreira

IMPORTANTE: Seja ESPECÍFICO e REALISTA. Base-se APENAS no CV fornecido e nas expectativas reais do mercado para {cargo} em {local}.
"""},
            {"role": "user", "content": f"""REALITY CHECK:

P1 Objetivo: {perfil['objetivo']}
P2 Cargo: {cargo}
P3 Pretensão: {pretensao} mensal
P4 Local: {local}
Remoto: {'Sim' if perfil.get('remoto') else 'Não'}

DEEP SCAN:
{st.session_state.analise_inicial}

FORMATO EXATO OBRIGATÓRIO:

🎯 **REALITY CHECK - ANÁLISE ESTRATÉGICA**

**CARGO DESEJADO:** {cargo}

**NOMENCLATURAS SIMILARES NO MERCADO:**
• [Variação 1]
• [Variação 2]
• [Variação 3]

*(Recrutadores usam diferentes nomes para a mesma função)*

---

### 📊 ANÁLISE SALARIAL

**Pretensão Informada:** {pretensao} mensal

**Faixa Salarial Geral:** [mínimo] a [máximo]

**Veredito:** [Abaixo/Na Média/Acima]

[Contexto]

---

### 🎯 VEREDITO DO HEADHUNTER

**Nível de Desafio:** [Baixo/Médio/Alto]

**Estratégia:** Focar em [ponto forte] para justificar {pretensao}"""}
        ]

        reality = chamar_gpt(
            st.session_state.openai_client, 
            msgs,
            temperature=0.3,  # Reduzir criatividade para maior consistência
            seed=42  # Seed fixo para reprodutibilidade
        )

        if reality:
            st.session_state.mensagens = [
                {"role": "system", "content": SYSTEM_PROMPT + f"\n\nCV DO CANDIDATO (uso interno): {st.session_state.cv_texto}\n\nCARGO-ALVO: {cargo}"},
                {"role": "assistant", "content": reality}
            ]
            st.session_state.force_scroll_top = True
            
            # Display reality check result
            st.markdown(reality)
            
            # Add interactive buttons for next steps
            st.markdown("---")
            st.markdown("### ✅ PRÓXIMOS PASSOS")
            st.markdown("Escolha uma das opções para continuar:")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Otimizar CV + LinkedIn", use_container_width=True, type="primary"):
                    # Check if CV is available
                    if not st.session_state.get('cv_texto'):
                        st.error("⚠️ CV não encontrado. Por favor, faça upload do CV novamente.")
                        st.session_state.fase = 'FASE_0_UPLOAD'
                        st.rerun()
                    
                    st.session_state.mensagens = []
                    st.session_state.modulo_ativo = None
                    st.session_state.etapa_modulo = None
                    
                    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
                    intro = f"""# 🔧 OTIMIZAÇÃO COMPLETA DE CV
## PROTOCOLO NÓBILE

**Vou otimizar seu CV experiência por experiência seguindo metodologia de Alta Performance.**

---

## 📋 PROCESSO EM 6 ETAPAS:

### **ETAPA 1: Análise de Keywords (SEO)**
→ Identificar as 10 palavras-chave essenciais para **{cargo}**  
→ Verificar presença no seu CV atual

### **ETAPA 2: Interrogatório Tático**
→ Análise detalhada de CADA experiência profissional  
→ Cobrança de dados quantitativos (KPIs, resultados)

### **ETAPA 3: Análise de Expertise**
→ Hard skills × Soft skills × Certificações  
→ Identificar gaps técnicos

### **ETAPA 4: Reescrita Estratégica**
→ Seguir o formato do seu CV original
→ Headlines de impacto para LinkedIn

### **ETAPA 5: Apresentação do CV Revisado**
→ Apresentar CV com todas as melhorias
→ Arquivo final formatado

---

⏱️ **TEMPO ESTIMADO:** 15-20 minutos  
📋 **VOCÊ PRECISARÁ:** Dados de impacto, tamanho de equipe, resultados quantitativos

---

⏸️ **Clique em "Iniciar" quando estiver pronto para começar.**"""
                    
                    st.session_state.mensagens.append({"role": "assistant", "content": intro})
                    st.session_state.modulo_ativo = 'OTIMIZADOR'
                    st.session_state.etapa_modulo = 'AGUARDANDO_INICIAR'
                    st.session_state.fase = 'CHAT'
                    forcar_topo()
                    st.rerun()

                if st.button("🎯 Analisar Vaga", use_container_width=True):
                    st.session_state.aguardando_vaga = True
                    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
                    msg = f"""🎯 **ANÁLISE DE FIT - VAGA × SEU PERFIL**

Cole abaixo a **descrição completa da vaga** que você quer aplicar.

Vou analisar:
- 📊 Estimativa salarial da vaga vs sua pretensão ({st.session_state.perfil.get('pretensao_salarial', 'N/A')})
- 🎯 Score de Match (0-100%)
- ⚠️ Pontos de atenção
- ✏️ Edições necessárias no CV
- ✅ Veredito: APLICAR ou NÃO APLICAR

**Cole a descrição da vaga:**"""
                    st.session_state.mensagens.append({"role": "assistant", "content": msg})
                    st.session_state.fase = 'CHAT'
                    forcar_topo()
                    st.rerun()

            with col2:
                if st.button("🎤 Prep. Entrevista", use_container_width=True):
                    st.session_state.fase = 'FASE_PREP_ENTREVISTA'
                    forcar_topo()
                    st.rerun()

                if st.button("🔄 Comparar CVs", use_container_width=True):
                    st.session_state.fase = 'FASE_COMPARADOR'
                    forcar_topo()
                    st.rerun()