def prompt_etapa6(cargo):
    """
    Gera prompt para ETAPA 6: Arquivo Mestre (Compilação Final).
    
    CRITICAL: Este prompt deve injetar TODOS os dados coletados para que a LLM
    use informações REAIS ao invés de inventar placeholders.
    """
    import streamlit as st
    from core.cv_estruturado import gerar_contexto_para_prompt, obter_cv_estruturado
    
    # Obter dados estruturados coletados
    contexto_dados = gerar_contexto_para_prompt()
    cv_estruturado = obter_cv_estruturado()
    
    # Obter dados do session_state
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    dados_coletados = st.session_state.get('dados_coletados', {})
    cv_texto_original = st.session_state.get('cv_texto', '')
    
    # Preparar contexto de gaps
    gaps_resolvidos = [gap for gap, info in gaps_respostas.items() if info.get('tem_experiencia')]
    gaps_contexto = ""
    if gaps_resolvidos:
        gaps_contexto = "**GAPS RESOLVIDOS (usar no posicionamento):**\n"
        for gap in gaps_resolvidos:
            info = gaps_respostas[gap]
            resposta = info.get('resposta', '')
            gaps_contexto += f"- {gap}: {resposta}\n"
    
    # Preparar histórico de dados coletados
    historico_coleta = dados_coletados.get('historico', [])
    contexto_coleta = ""
    if historico_coleta:
        contexto_coleta = "**DADOS COLETADOS NA ENTREVISTA (usar nas experiências):**\n\n"
        for i, resposta in enumerate(historico_coleta, 1):
            contexto_coleta += f"{i}. {resposta}\n\n"
    
    return f"""### 📦 ETAPA 6: ARQUIVO MESTRE (Compilação Final)

═══════════════════════════════════════════════════════════════════
⚠️ **ATENÇÃO CRÍTICA**: Use SOMENTE dados REAIS coletados abaixo
NUNCA invente informações, métricas ou conquistas
═══════════════════════════════════════════════════════════════════

{contexto_dados}

---

{gaps_contexto}

---

{contexto_coleta}

---

**CV ORIGINAL DO CANDIDATO (para extrair dados factuais):**

{cv_texto_original}

---

### 📋 TAREFA: Gerar DOIS BLOCOS de Output

Gere um bloco de texto único contendo TUDO para facilitar importação:

═══════════════════════════════════════════
**SEÇÃO 1: LINKEDIN METADATA**
═══════════════════════════════════════════

**HEADLINE OTIMIZADA:**
[Usar cargo-alvo + diferencial REAL baseado nos gaps resolvidos]
Exemplo: "Controler Jurídico | Legal Operations & Compliance | Especialista em Peticionamento Eletrônico Nacional"

**TOP SKILLS (para LinkedIn - máximo 10):**
• [Skill 1 - baseada em gap resolvido ou experiência real]
• [Skill 2 - baseada em ferramenta/tecnologia mencionada]
• [Skill 3 - baseada em competência demonstrada]
• [Skill 4]
• [Skill 5]
• [Skill 6]
• [Skill 7]
• [Skill 8]
• [Skill 9]
• [Skill 10]

**ABOUT (Resumo LinkedIn - 2-3 parágrafos):**
[Usar posicionamento estratégico baseado nos gaps RESOLVIDOS]
[Incluir senioridade real, não inventar]
[Mencionar diferenciais concretos das experiências]

═══════════════════════════════════════════
**SEÇÃO 2: CV COMPLETO (COPIAR PARA FLOWCV)**
═══════════════════════════════════════════

**FORMATAÇÃO RIGOROSA:**
- Use bullets (•) para lista de conquistas
- Máximo 5 bullets por experiência
- Mínimo 3 bullets por experiência
- Cada bullet DEVE ter formato: **[CATEGORIA]:** Descrição com métrica/resultado
- Categorias comuns: [GESTÃO DE SISTEMAS], [COMPLIANCE], [TECNOLOGIA], [PROTOCOLOS], [MÉTRICAS], [IMPACTO], [LIDERANÇA], [PROCESSOS]
- SEMPRE inclua métricas (%, R$, tempo, quantidade, volume)
- Separe seções com linha em branco
- **IMPORTANTE: Use cabeçalhos em INGLÊS para ATS** (SUMMARY, EXPERIENCE, EDUCATION, LANGUAGES, CERTIFICATIONS)

---

[Nome Completo - extrair do CV original]
[Telefone] | [Email] | [LinkedIn] | [Cidade/Estado - extrair do CV original]

═══════════════════════════════════════════

**SUMMARY**

[Resumo otimizado - 3-4 linhas máximo]
[Usar posicionamento estratégico baseado nos gaps RESOLVIDOS]
[Mencionar senioridade real do CV original]
[Incluir foco/especialização baseado nas experiências REAIS]
[Destacar competências que TEM (não inventar)]

═══════════════════════════════════════════

**EXPERIENCE**

[Para CADA experiência do CV original, otimizar seguindo este formato:]

**[Job Title - melhorar nomenclatura se genérico]** | [Company Name] | [Start Date] - [End Date/Present]

• **[CATEGORIA]:** [Conquista com métrica REAL dos dados coletados - usar verbo de ação em inglês: Led, Managed, Implemented, Achieved, Increased, etc.]
• **[CATEGORIA]:** [Conquista com métrica REAL - percentual, valor, tempo de melhoria]
• **[CATEGORIA]:** [Conquista com métrica REAL - tamanho de equipe, receita, impacto]
• **[CATEGORIA]:** [Conquista com métrica REAL - processo, ferramenta, resultado]
• **[CATEGORIA]:** [Conquista adicional se houver dados coletados]

**EXEMPLO REAL (Controler Jurídico):**
**[GESTÃO DE SISTEMAS]:** Operação técnica avançada em PJE, ESAJ, PROJUIDI e TRT em tribunais de todo o Brasil
**[COMPLIANCE]:** Verificação de andamentos processuais e formalização de documentos de status, mitigando riscos de perda de prazos
**[TECNOLOGIA]:** Alimentação e auditoria de dados no sistema LegalBox garantindo integridade para +50 processos
**[PROTOCOLOS]:** Realização de protocolos e distribuições de novos processos com foco em erro zero

---

[Repetir para TODAS as experiências do CV original - SEMPRE usar dados REAIS, nunca inventar]

═══════════════════════════════════════════

**EDUCATION**

[Copiar do CV original - não modificar]

**LANGUAGES**

[Copiar do CV original - não modificar]

**CERTIFICATIONS**

[Copiar do CV original se houver - não inventar]

═══════════════════════════════════════════

### ⚠️ REGRAS CRÍTICAS DE VALIDAÇÃO:

Antes de entregar, verifique:
✅ Todos os bullets têm métricas/números REAIS dos dados coletados
✅ Todos os bullets usam formato **[CATEGORIA]:** Descrição
✅ Verbos de ação (pode ser em português se mais natural)
✅ Seções em INGLÊS (SUMMARY, EXPERIENCE, EDUCATION)
✅ Estrutura segue modelo com categorias
✅ Máximo 5 bullets por experiência
✅ Mínimo 3 bullets por experiência
✅ ZERO informações inventadas - tudo baseado em dados coletados ou CV original
✅ Summary menciona APENAS gaps que foram resolvidos
✅ Skills do LinkedIn baseadas em experiências REAIS

### 🚫 O QUE NÃO FAZER:

❌ NÃO invente métricas ("aumentou vendas em 45%" se não foi mencionado)
❌ NÃO invente ferramentas ("usou Power BI" se não foi mencionado)
❌ NÃO invente conquistas genéricas sem base real
❌ NÃO use placeholders como [valor], [ferramenta], [métrica]
❌ NÃO mencione skills que o candidato não demonstrou ter

---

🎯 **GERE O OUTPUT COMPLETO AGORA** seguindo rigorosamente as instruções acima.

Após gerar o arquivo completo, avance para ETAPA 7."""
