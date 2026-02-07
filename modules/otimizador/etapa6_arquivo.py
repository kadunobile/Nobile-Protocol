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

**FORMATAÇÃO VISUAL (baseada no modelo Carlos Eduardo Nóbile):**
- Use bullets (•) para lista de conquistas
- Máximo 4-5 bullets por experiência
- Cada bullet inicia com verbo de ação forte (Gerenciei, Implementei, Aumentei)
- Sempre inclua métricas (%, R$, tempo, tamanho equipe)
- Separe seções com linha em branco

---

Nota: Use cabeçalhos em Inglês para ATS (SUMMARY, EXPERIENCE, EDUCATION)

[Nome Completo]
[Telefone] | [Email] | [LinkedIn] | [Cidade/Estado]

═══════════════════════════════════════════

**SUMMARY**

[Resumo otimizado da Etapa 4A - texto completo, 3-4 linhas máximo]

═══════════════════════════════════════════

**EXPERIENCE**

**[Cargo Atual/Mais Recente]**  
*[Empresa]* | *[Período]*

• [Conquista 1 com métrica]
• [Conquista 2 com métrica]
• [Conquista 3 com métrica]
• [Conquista 4 com métrica]

---

**[Cargo Anterior]**  
*[Empresa]* | *[Período]*

• [Conquista 1 com métrica]
• [Conquista 2 com métrica]
• [Conquista 3 com métrica]

[Repetir para todas as experiências da Etapa 4B]

═══════════════════════════════════════════

**EDUCATION**
[Formação acadêmica original do CV]

**LANGUAGES**
[Idiomas originais]

**CERTIFICATIONS**
[Se houver no CV original]

═══════════════════════════════════════════

Após gerar o arquivo completo, avance para ETAPA 7."""
