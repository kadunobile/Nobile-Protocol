"""
Etapa 1: Coleta Focada - Apenas 3 perguntas por experiência relevante.

Esta etapa substitui o interrogatório pesado (25+ campos) por uma coleta
simplificada e focada de apenas 3 perguntas essenciais por experiência.
"""

import streamlit as st


def prompt_etapa1_coleta_focada():
    """
    Gera prompt para coleta focada de dados.
    
    Ao invés de 25+ campos, pergunta apenas:
    1. Resultado quantificável principal
    2. Métrica/indicador usado
    3. Como isso resolve o gap identificado
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão."""
    
    return f"""📝 **ETAPA 1: COLETA FOCADA DE DADOS**

**CARGO-ALVO:** {cargo}

---

**INSTRUÇÕES PARA O ASSISTENTE:**

Você vai agora coletar dados adicionais do candidato, **uma experiência por vez**, para otimizar o CV.

Para CADA experiência profissional relevante identificada no diagnóstico:

1. **Leia a experiência atual** no CV
2. **Identifique o que falta ou pode melhorar** (resultados quantificáveis, métricas, contexto sobre gaps)
3. **Faça 2-3 perguntas diretas** no chat para o candidato preencher as informações

**FORMATO DE COLETA (conversacional):**

---

### 🏢 [Nome da Empresa] - [Cargo] - [Período]

**O que está no CV agora:**
[Breve resumo do que consta no CV atual para essa experiência]

**Gap(s) a resolver:**
[Lista dos gaps que esta experiência vai abordar]

**Perguntas:**

1. Qual foi o principal resultado mensurável que você alcançou nesta posição? (Ex: "Aumentei vendas em 30%", "Reduzi custos em R$ 50k", "Gerenciei equipe de 15 pessoas")

2. Qual métrica ou indicador você usava para medir esse resultado? (Ex: "Revenue mensal", "NPS", "Tempo de entrega", "Taxa de conversão")

3. Como essa conquista demonstra que você tem a competência necessária para o cargo-alvo? (Ex: "Isso mostra minha capacidade de liderança porque...", "Evidencia domínio de Python pois...")

---

⏸️ **Aguardando suas respostas.** Digite as respostas no chat, ou responda **"não tenho"**, **"pular"** ou **"próxima"** se quiser avançar sem preencher esta experiência.

Após coletar dados de todas as experiências relevantes (máximo 3-4), pediremos aprovação antes de reescrever o CV.
"""
