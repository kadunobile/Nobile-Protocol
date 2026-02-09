"""
Etapa 1: Coleta Focada - Perguntas contextuais por experiência.

Esta etapa faz perguntas ESPECÍFICAS para cada experiência profissional,
correlacionadas ao cargo desejado, como um headhunter faria.
"""

import streamlit as st


def prompt_etapa1_coleta_focada():
    """
    Gera prompt para coleta focada de dados com perguntas contextuais.
    
    As perguntas devem ser específicas ao cargo desejado e à experiência,
    não genéricas. Pensa como um headhunter que quer extrair:
    - Métricas e resultados quantificáveis
    - Ferramentas e tecnologias específicas do setor
    - Impacto e volume de trabalho
    - Nomenclatura adequada do cargo para ATS
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão."""
    
    # Preparar contexto dos gaps com experiência
    gaps_com_contexto = []
    for gap, info in gaps_respostas.items():
        if info.get('tem_experiencia'):
            gaps_com_contexto.append({
                'gap': gap,
                'contexto': info.get('resposta', '')
            })
    
    gaps_contexto_texto = ""
    if gaps_com_contexto:
        gaps_contexto_texto = "\n".join([
            f"- **{g['gap']}**: {g['contexto']}" 
            for g in gaps_com_contexto
        ])
    
    return f"""📝 **ETAPA 1: COLETA FOCADA DE DADOS**

**CARGO-ALVO:** {cargo}

---

### 📊 Contexto dos Gaps Mapeados

Durante o diagnóstico, você indicou ter experiência com:

{gaps_contexto_texto if gaps_contexto_texto else "- (Nenhum gap mapeado ainda)"}

---

### 🎯 INSTRUÇÕES PARA O ASSISTENTE GPT

Você é um **headhunter expert** especializado em otimização de CVs para o cargo de **{cargo}**.

Sua missão: fazer perguntas CONTEXTUAIS e ESPECÍFICAS para cada experiência profissional no CV, extraindo dados que permitam:

1. **Transformar tarefas passivas em conquistas ativas**
   - ❌ Fraco: "Alimentação de planilhas"
   - ✅ Forte: "Gestão de Dados Estratégicos com redução de 40% no tempo de processamento via Power BI"

2. **Incluir métricas e KPIs relevantes ao setor**
   - Volume (quantas pessoas, projetos, vendas, processos)
   - Impacto (% de melhoria, economia, crescimento)
   - Ferramentas específicas (tecnologias, sistemas, metodologias)

3. **Melhorar nomenclatura de cargos para ATS**
   - Usar títulos que sistemas ATS reconhecem
   - Correlacionar com "trigger words" do RH para este cargo

4. **Fazer perguntas que um headhunter faria**
   - Não genéricas ("qual foi o resultado?")
   - Específicas ao cargo e setor ("Na ARQUIVEI como RevOps, qual ferramenta de BI você usava para dashboards de receita recorrente?")

---

### 📋 FORMATO DE COLETA (conversacional)

Para CADA experiência profissional no CV, faça o seguinte:

1. **Mostre o que está no CV atual** para essa experiência (empresa, cargo, período, descrição)

2. **Analise o que falta ou está fraco** em relação ao cargo-alvo **{cargo}**
   - Faltam métricas?
   - Faltam ferramentas específicas?
   - O cargo poderia ter nomenclatura melhor para ATS?
   - A descrição está passiva ou ativa?

3. **Faça 2-4 perguntas ESPECÍFICAS** ao candidato, correlacionadas ao cargo **{cargo}**
   - Pergunte sobre volume, impacto, ferramentas, resultados
   - Pense em trigger words que RH procura neste cargo
   - Seja direto e objetivo

4. **Sugira melhoria de nomenclatura** se o cargo atual for genérico

---

### 💡 EXEMPLOS DE PERGUNTAS CONTEXTUAIS (não genéricas):

**Cargo Alvo: Gerente de Revenue Operations**
- "Na ARQUIVEI como RevOps Manager, qual ferramenta de BI você usava para gerar dashboards de receita? (Tableau, Power BI, Looker?)"
- "Qual era o volume de receita recorrente (ARR) que você gerenciava?"
- "Você implementou alguma automação? Se sim, qual foi o impacto em tempo/eficiência?"

**Cargo Alvo: Product Manager**
- "Quantos produtos/features você lançou durante esse período?"
- "Qual metodologia ágil você usava? (Scrum, Kanban, outro?)"
- "Qual foi o impacto mensurável nos KPIs do produto? (adoção, retenção, revenue)"

**Cargo Alvo: Engenheiro de Dados**
- "Qual stack de tecnologias você usava? (Python, Spark, Airflow, DBT?)"
- "Qual era o volume de dados processado? (GB/TB por dia?)"
- "Você otimizou algum pipeline? Qual foi a melhoria em performance?"

---

**CV DO CANDIDATO:**

{cv_texto}

---

⏭️ **COMECE AGORA:** Identifique a primeira experiência profissional relevante no CV e faça as perguntas contextuais.

⏸️ **Aguardando suas perguntas para a primeira experiência...**
"""
