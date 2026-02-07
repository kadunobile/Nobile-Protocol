def prompt_etapa1(cargo):
    return f"""Inicie a ETAPA 1 do otimizador de CV.

Analise o CV do candidato (no contexto) e identifique as 10 KEYWORDS mais importantes para o cargo de {cargo}.

Compare cada keyword com o CV atual.

Formato EXATO:

🎯 **ETAPA 1: MAPEAMENTO DE SEO - {cargo.upper()}**

**TOP 10 KEYWORDS DO MERCADO:**
1. [Keyword 1] - ✅ PRESENTE no CV / ❌ AUSENTE no CV
2. [Keyword 2] - Status
3. [Keyword 3] - Status
4. [Keyword 4] - Status
5. [Keyword 5] - Status
6. [Keyword 6] - Status
7. [Keyword 7] - Status
8. [Keyword 8] - Status
9. [Keyword 9] - Status
10. [Keyword 10] - Status

---

🔴 **AÇÃO NECESSÁRIA:**

Para cada keyword ❌ AUSENTE, pergunte:
- Você tem experiência com [keyword]? Em qual contexto/empresa? Como e onde?

⏸️ **AGUARDO SUA RESPOSTA ANTES DE CONTINUAR PARA A ETAPA 2.**

NÃO mostre o CV completo."""
