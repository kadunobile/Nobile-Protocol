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

**INSTRUÇÕES:**

Para CADA experiência profissional relevante identificada no diagnóstico, faça apenas 3 perguntas essenciais.

**MODELO DE COLETA (para cada experiência):**

---

### 🏢 EXPERIÊNCIA: [Empresa - Cargo - Período]

**Contexto:** [Breve descrição do que o candidato fazia]

**Gap(s) a resolver:** [Lista dos gaps que esta experiência vai abordar]

---

**❓ PERGUNTA 1: Resultado Quantificável**

Qual foi o principal resultado mensurável que você alcançou nesta posição?  
(Ex: "Aumentei vendas em 30%", "Reduzi custos em R$ 50k", "Gerenciei equipe de 15 pessoas")

_[Campo para resposta do usuário]_

---

**❓ PERGUNTA 2: Métrica/Indicador**

Qual métrica ou indicador você usava para medir esse resultado?  
(Ex: "Revenue mensal", "NPS", "Tempo de entrega", "Taxa de conversão")

_[Campo para resposta do usuário]_

---

**❓ PERGUNTA 3: Contexto do Gap**

Como essa conquista demonstra que você tem a competência do gap identificado?  
(Ex: "Isso mostra minha capacidade de liderança porque...", "Evidencia domínio de Python pois...")

_[Campo para resposta do usuário]_

---

[Repita este bloco para cada experiência relevante - máximo 3-4 experiências]

---

### ✅ RESUMO DA COLETA

Total de experiências a otimizar: [X]

Você terá que responder: [X × 3 = Y perguntas]

---

⏸️ **Preencha as respostas abaixo no formato:**

**Experiência 1 - [Empresa]:**
- Resultado: [sua resposta]
- Métrica: [sua resposta]
- Contexto: [sua resposta]

**Experiência 2 - [Empresa]:**
- Resultado: [sua resposta]
- Métrica: [sua resposta]
- Contexto: [sua resposta]

(etc)

**Após preencher todos os dados, responda "CONTINUAR" para validação.**
"""
