def prompt_etapa1_5(cargo, keywords_selecionadas):
    """
    Gera prompt para análise profunda do CV e integração de keywords.
    
    Args:
        cargo: Cargo alvo do candidato
        keywords_selecionadas: Lista de keywords que o usuário selecionou/preencheu
        
    Returns:
        String com o prompt formatado para análise do CV
    """
    keywords_str = "\n".join([f"- {kw}" for kw in keywords_selecionadas])
    
    return f"""### 🔍 ETAPA 1.5: ANÁLISE PROFUNDA DO CV + INTEGRAÇÃO DE KEYWORDS

Agora vou analisar seu CV atual em detalhes e sugerir como integrar as keywords selecionadas.

**KEYWORDS A INTEGRAR:**
{keywords_str}

---

**INSTRUÇÕES PARA ANÁLISE:**

1. **LEIA O CV ORIGINAL** (já no contexto)
2. **IDENTIFIQUE:**
   - Como cada experiência está escrita
   - Estilo de escrita (genérico vs específico)
   - Presença ou ausência de métricas
   - Verbos de ação utilizados
   - Estrutura de cada seção

3. **ANÁLISE CRÍTICA POR EXPERIÊNCIA:**

Para CADA experiência profissional do CV:

**[Empresa X - Cargo Y]**

**Como está escrito agora:**
[Transcreva como aparece no CV]

**Problemas identificados:**
- ❌ [Problema 1 - ex: falta métricas]
- ❌ [Problema 2 - ex: verbos fracos]
- ❌ [Problema 3 - ex: descrição genérica]

**Keywords ausentes que podem ser integradas:**
- [Keyword 1] - pode ser adicionada ao mencionar [contexto específico]
- [Keyword 2] - pode ser integrada ao falar sobre [atividade específica]

**Sugestão de reescrita (exemplo STAR):**
[Mostre UMA VERSÃO reescrita da experiência, integrando keywords naturalmente]

---

4. **ANÁLISE DO RESUMO PROFISSIONAL:**

**Resumo atual:**
[Transcreva resumo se existir, ou diga "Não possui"]

**Melhorias necessárias:**
- Adicionar keywords: {keywords_str[:100]}...
- Incluir proposta de valor clara para {cargo}
- Quantificar anos de experiência
- Destacar realizações macro

**Sugestão de novo resumo:**
[Escreva resumo otimizado com keywords integradas]

---

5. **PRÓXIMOS PASSOS:**

Após esta análise, vamos para a **ETAPA 2** onde vou entrevistar você sobre CADA experiência para coletar:
- Números exatos (%, R$, tempo, tamanho equipe)
- Contexto de negócio
- Desafios superados
- Resultados mensuráveis

⏸️ **Revise as sugestões acima antes de continuar.**

Quando estiver pronto, responda **"CONTINUAR"** para iniciar a ETAPA 2.
"""
