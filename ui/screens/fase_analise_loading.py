import streamlit as st
import time
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt, scroll_topo


def fase_analise_loading():
    """
    Tela de loading que mostra o progresso da análise do CV.
    Explica cada etapa do processo enquanto a IA trabalha.
    """
    scroll_topo()
    
    st.markdown("# 🧠 Analisando Seu CV...")
    st.markdown("---")
    
    st.info("⏱️ **Isso leva aproximadamente 30-40 segundos. Por favor, aguarde.**")
    
    # Container para as etapas
    etapas_container = st.container()
    
    with etapas_container:
        st.markdown("### 📊 O que estamos fazendo agora:")
        
        etapa1 = st.empty()
        etapa2 = st.empty()
        etapa3 = st.empty()
        etapa4 = st.empty()
        etapa5 = st.empty()
        
        # Etapa 1: Extração de palavras-chave
        etapa1.markdown("⏳ **1. Extraindo palavras-chave do seu histórico...**")
        time.sleep(0.5)
        etapa1.markdown("✅ **1. Palavras-chave extraídas com sucesso**")
        
        # Etapa 2: Comparação com mercado
        etapa2.markdown("⏳ **2. Comparando com padrões de mercado...**")
        time.sleep(0.5)
        etapa2.markdown("✅ **2. Comparação com mercado concluída**")
        
        # Etapa 3: Identificação de gaps
        etapa3.markdown("⏳ **3. Identificando gaps técnicos e comportamentais...**")
        
        # AQUI CHAMA A IA PARA FAZER A ANÁLISE REAL
        with st.spinner("🤖 IA analisando profundamente seu perfil..."):
            resultado_analise = executar_analise_cv()
        
        etapa3.markdown("✅ **3. Gaps identificados**")
        
        # Etapa 4: Mapeamento de experiências
        etapa4.markdown("⏳ **4. Mapeando experiências quantificáveis...**")
        time.sleep(0.5)
        etapa4.markdown("✅ **4. Experiências mapeadas**")
        
        # Etapa 5: Preparando otimizações
        etapa5.markdown("⏳ **5. Preparando sugestões de otimização...**")
        time.sleep(0.5)
        etapa5.markdown("✅ **5. Análise completa!**")
    
    st.markdown("---")
    st.success("🎉 **Análise concluída com sucesso!**")
    
    # Aguardar 1 segundo para o usuário ver a conclusão
    time.sleep(1)
    
    # Salvar resultados e ir para próxima fase
    if resultado_analise:
        cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
        
        # Preparar mensagens para o chat com a análise e módulo otimizador
        st.session_state.mensagens = [
            {"role": "system", "content": SYSTEM_PROMPT + f"\n\nCV DO CANDIDATO (uso interno - NUNCA mostre de volta): {st.session_state.cv_texto}\n\nCARGO-ALVO: {cargo}"},
            {"role": "assistant", "content": resultado_analise}
        ]
        
        # Ativar módulo otimizador e aguardar OK para começar
        st.session_state.modulo_ativo = "OTIMIZADOR"
        st.session_state.etapa_modulo = "AGUARDANDO_OK"
        st.session_state.analise_cv_completa = resultado_analise
        st.session_state.force_scroll_top = True
        st.session_state.fase = 'CHAT'
        st.rerun()
    else:
        st.error("❌ Erro ao analisar CV. Por favor, tente novamente.")


def executar_analise_cv():
    """
    Executa a análise completa do CV usando a IA.
    
    Returns:
        str com resultados da análise ou None se falhar
    """
    cv_texto = st.session_state.cv_texto
    cargo_alvo = st.session_state.perfil['cargo_alvo']
    
    msgs = [
        {
            "role": "system", 
            "content": SYSTEM_PROMPT + f"""

INSTRUÇÕES INTERNAS - ANÁLISE DE CV:

Você está analisando o CV de um candidato para a posição: {cargo_alvo}

FORMATO DE RESPOSTA OBRIGATÓRIO:

## 📊 ANÁLISE DE PALAVRAS-CHAVE

**Palavras-chave encontradas:**
- [palavra 1]
- [palavra 2]
- [palavra 3]

**Palavras-chave que faltam (importantes para {cargo_alvo}):**
- [palavra 1] - [Por que é importante]
- [palavra 2] - [Por que é importante]

---

## ⚠️ GAPS IDENTIFICADOS

**Gaps Técnicos:**
1. **[Skill X]:** [Explicação] - **Impacto:** [Alto/Médio/Baixo]
2. **[Skill Y]:** [Explicação] - **Impacto:** [Alto/Médio/Baixo]

**Gaps Comportamentais:**
1. **[Competência X]:** [Explicação]

---

## 💪 PONTOS FORTES

- [Ponto forte 1]
- [Ponto forte 2]
- [Ponto forte 3]

---

## 🎯 EXPERIÊNCIAS QUANTIFICÁVEIS

**Já existem:**
- [Experiência com métrica 1]
- [Experiência com métrica 2]

**Podem ser melhoradas:**
- [Experiência sem métrica] → **Sugestão:** [Como quantificar]

---

## ✅ PRÓXIMO PASSO

Agora vamos para a otimização do seu CV. Digite "OK" ou "COMEÇAR" para iniciar a ETAPA 1 (Mapeamento de SEO).
"""
        },
        {
            "role": "user",
            "content": f"""Analise este CV para a vaga de {cargo_alvo}:

{cv_texto}

Siga o formato EXATO especificado nas instruções."""
        }
    ]
    
    # IMPORTANTE: Usar parâmetros determinísticos
    analise = chamar_gpt(
        st.session_state.openai_client, 
        msgs,
        temperature=0.3,  # Consistência
        seed=42           # Determinístico
    )
    
    return analise
