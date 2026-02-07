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

Nota: Use cabeçalhos em Inglês para ATS (SUMMARY, EXPERIENCE, EDUCATION)

[Nome Completo]
[Telefone] | [Email] | [LinkedIn] | [Cidade/Estado]

**SUMMARY**
[Resumo otimizado da Etapa 4A - texto completo]

**EXPERIENCE**

[Todas as experiências reescritas na Etapa 4B - ordem cronológica inversa]

**EDUCATION**
[Formação acadêmica original do CV]

**LANGUAGES**
[Idiomas originais]

**CERTIFICATIONS**
[Se houver no CV original]

═══════════════════════════════════════════

Após gerar o arquivo completo, avance para ETAPA 7."""
