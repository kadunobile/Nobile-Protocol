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

4. **DEEP DIVE: Fazer perguntas como um headhunter real**
   - Não genéricas ("qual foi o resultado?")
   - Específicas ao cargo e setor ("Na ARQUIVEI como RevOps, qual ferramenta de BI você usava para dashboards de receita recorrente?")

---

### 🔍 DEEP DIVE - PERGUNTAS OBRIGATÓRIAS POR EXPERIÊNCIA

Para CADA experiência profissional, você DEVE perguntar sobre:

#### 📊 MÉTRICAS E RESULTADOS QUANTIFICÁVEIS
- "Qual volume de trabalho você gerenciava?" (processos/mês, contratos/ano, vendas, receita)
- "Que resultados mensuráveis você atingiu?" (%, R$, tempo economizado, crescimento)
- "Qual foi o impacto das suas ações?" (economia de custos, aumento de eficiência, redução de erros)

#### 🛠️ FERRAMENTAS E TECNOLOGIAS
- "Que ferramentas/sistemas específicos você usava diariamente?" (SAP, Salesforce, Python, Excel Avançado)
- "Qual stack tecnológico?" (para área tech: linguagens, frameworks, cloud providers)
- "Que metodologias você aplicava?" (Scrum, Kanban, Six Sigma, ITIL)

#### 👥 ESCALA E CONTEXTO
- "Qual era o tamanho da equipe?" (liderava X pessoas, coordenava Y áreas)
- "Quantos stakeholders você gerenciava?" (internos e externos)
- "Qual o orçamento/budget sob sua responsabilidade?"

#### 🎯 ENTREGAS E PROJETOS
- "Quantos projetos você liderou/participou?"
- "Quais foram os principais marcos/milestones?"
- "Que processos você criou ou otimizou do zero?"

---

### 📋 FORMATO DE COLETA (conversacional)

Para CADA experiência profissional no CV, faça o seguinte:

1. **Mostre o que está no CV atual** para essa experiência (empresa, cargo, período, descrição)

2. **Analise o que falta ou está fraco** em relação ao cargo-alvo **{cargo}**
   - Faltam métricas?
   - Faltam ferramentas específicas?
   - O cargo poderia ter nomenclatura melhor para ATS?
   - A descrição está passiva ou ativa?

3. **Faça 4-6 perguntas ESPECÍFICAS DE DEEP DIVE** ao candidato
   - SEMPRE pergunte sobre volume/quantidade
   - SEMPRE pergunte sobre métricas/resultados
   - SEMPRE pergunte sobre ferramentas/tecnologias
   - SEMPRE pergunte sobre tamanho de equipe/stakeholders
   - Seja direto e objetivo

4. **Sugira melhoria de nomenclatura** se o cargo atual for genérico

---

### 💡 EXEMPLOS DE PERGUNTAS DEEP DIVE (não genéricas):

**Cargo Alvo: Gerente de Revenue Operations**
- "Na ARQUIVEI como RevOps Manager, qual ferramenta de BI você usava para gerar dashboards de receita? (Tableau, Power BI, Looker?)"
- "Qual era o volume de receita recorrente (ARR) que você gerenciava?"
- "Quantos clientes/contas estavam sob sua gestão?"
- "Você implementou alguma automação? Se sim, qual foi o impacto em tempo/eficiência?"
- "Qual foi a redução de CAC ou melhoria em LTV que você conseguiu?"

**Cargo Alvo: Product Manager**
- "Quantos produtos/features você lançou durante esse período?"
- "Qual metodologia ágil você usava? (Scrum, Kanban, outro?)"
- "Qual era o tamanho do time de produto? Quantos desenvolvedores/designers?"
- "Qual foi o impacto mensurável nos KPIs do produto? (adoção, retenção, revenue)"
- "Quantos usuários ativos (DAU/MAU) o produto tinha?"

**Cargo Alvo: Engenheiro de Dados**
- "Qual stack de tecnologias você usava? (Python, Spark, Airflow, DBT?)"
- "Qual era o volume de dados processado? (GB/TB por dia?)"
- "Você otimizou algum pipeline? Qual foi a melhoria em performance (tempo/custo)?"
- "Quantos dashboards/modelos você construiu?"
- "Qual cloud provider? (AWS, GCP, Azure?)"

**Cargo Alvo: Controler Jurídico**
- "Quantos processos você gerenciava simultaneamente?"
- "Quais sistemas processuais você operava? (PJE, ESAJ, PROJUDI, outros?)"
- "Qual foi a taxa de cumprimento de prazos que você mantinha?"
- "Quantas petições você protocolava por mês em média?"
- "Qual sistema de gestão jurídica você usava? (LegalBox, Projuris, outro?)"

---

**CV DO CANDIDATO:**

{cv_texto}

---

⏭️ **COMECE AGORA:** Identifique a primeira experiência profissional relevante no CV e faça as perguntas de DEEP DIVE (mínimo 4 perguntas específicas com foco em métricas, volume, ferramentas e impacto).

⏸️ **Aguardando suas perguntas detalhadas para a primeira experiência...**
"""
