def prompt_etapa6(cargo):
    return f"""### 📦 ETAPA 6: ARQUIVO MESTRE (Compilação Final)

Gere um bloco de texto único contendo TUDO para facilitar importação:

═══════════════════════════════════════════
**SEÇÃO 1: LINKEDIN METADATA**
═══════════════════════════════════════════

**HEADLINE OTIMIZADA:**
[{cargo}] | [Proposta de valor] | [Diferencial]

**TOP SKILLS (para LinkedIn):**
• [Skill 1]
• [Skill 2]
• [Skill 3]
• [Skill 4]
• [Skill 5]
• [Skill 6]
• [Skill 7]
• [Skill 8]
• [Skill 9]
• [Skill 10]

═══════════════════════════════════════════
**SEÇÃO 2: CV COMPLETO (COPIAR PARA FLOWCV)**
═══════════════════════════════════════════

**FORMATAÇÃO RIGOROSA (baseada no modelo Carlos Eduardo Nóbile):**
- Use bullets (•) para lista de conquistas
- Máximo 5 bullets por experiência
- Mínimo 3 bullets por experiência
- Cada bullet inicia com verbo de ação forte em INGLÊS (Led, Managed, Implemented, Achieved, Increased, etc.)
- SEMPRE inclua métricas (%, R$, tempo, tamanho equipe, quantidade)
- Separe seções com linha em branco
- **IMPORTANTE: Use cabeçalhos em INGLÊS para ATS** (SUMMARY, EXPERIENCE, EDUCATION, LANGUAGES, CERTIFICATIONS)

---

[Nome Completo]
[Telefone] | [Email] | [LinkedIn] | [Cidade/Estado]

═══════════════════════════════════════════

**SUMMARY**

[Resumo otimizado da Etapa 4A - texto completo, 3-4 linhas máximo]

═══════════════════════════════════════════

**EXPERIENCE**

**[Job Title]** | [Company Name] | [Start Date] - [End Date/Present]
• [Achievement with metric - Led/Managed/Implemented + action + number]
• [Achievement with metric - percentage/value/time improvement]
• [Achievement with metric - team size/revenue/impact]
• [Achievement with metric - process/tool/result]

---

**[Previous Job Title]** | [Company Name] | [Start Date] - [End Date]
• [Achievement with metric]
• [Achievement with metric]
• [Achievement with metric]

[Repetir para todas as experiências da Etapa 4B - SEMPRE com métricas]

═══════════════════════════════════════════

**EDUCATION**

[Formação acadêmica original do CV]

**LANGUAGES**

[Idiomas originais]

**CERTIFICATIONS**

[Se houver no CV original]

═══════════════════════════════════════════

**VALIDAÇÃO FINAL:**

Antes de entregar, verifique:
✅ Todos os bullets têm métricas/números
✅ Verbos de ação em inglês em cada bullet
✅ Seções em INGLÊS (SUMMARY, EXPERIENCE, EDUCATION)
✅ Estrutura segue modelo Carlos Eduardo Nóbile
✅ Máximo 5 bullets por experiência
✅ Mínimo 3 bullets por experiência

Após gerar o arquivo completo, avance para ETAPA 7."""
