def prompt_etapa2():
    return """Ótimo! Recebi suas respostas sobre as keywords. Avançando para ETAPA 2.

### 📊 ETAPA 2: INTERROGATÓRIO TÁTICO

Instrução Crítica: Você NÃO pode aceitar generalismos. Analise TODAS as experiências do CV, da atual até a mais antiga, sem exceção.

Para CADA cargo no CV, apresente o "Relatório de Gaps":

**EXPERIÊNCIA [N]: [Nome da Empresa] - [Cargo] | [Período]**

*Frase Genérica encontrada no CV:*  
> "[Cite a frase EXATA do CV original]"

⚠️ **A Cobrança:** "Isso não vende. Qual foi o impacto exato?"

🔍 **DADOS NECESSÁRIOS:**
1. **Impacto Financeiro:** Quanto gerou/economizou? (R$, %)
2. **Tamanho da Equipe:** Quantas pessoas gerenciava?
3. **Orçamento/Budget:** Qual valor sob sua responsabilidade?
4. **Resultados Mensuráveis:** Que métricas melhorou? (tempo, qualidade, NPS)

---

(Repita este bloco para TODAS as empresas do CV, uma por uma, sem exceção)

---

🔴 **COMANDO FINAL:**

"Responda abaixo com os números brutos para cada ponto acima.
Se não tiver o número exato, me dê sua melhor estimativa conservadora."

**Formato esperado:**

Experiência 1 ([Empresa]):
- Impacto: [resposta]
- Equipe: [resposta]
- Orçamento: [resposta]
- Resultados: [resposta]

Experiência 2 ([Empresa]):
(mesmo formato)

⏸️ **PAUSE - AGUARDO OS DADOS COMPLETOS.**

NÃO mostre o CV completo."""
