# Headhunter Elite - Dynamic Question Generation & Telemetry

## Visão Geral

Este documento descreve as melhorias implementadas no fluxo do Headhunter Elite, incluindo:

1. **Telemetria de Chamadas GPT** - Badge visível mostrando número de chamadas na sessão
2. **Cache/Resumo de CV** - Redução de tokens através de caching inteligente
3. **Geração Dinâmica de Perguntas** - Perguntas contextuais adaptativas em cada interação
4. **Anti-Loop** - Prevenção de perguntas repetitivas através de histórico de Q&A
5. **Stop Conditions** - Avanço automático quando informações suficientes são coletadas
6. **Guardrails** - Prevenção de invenção de dados

## Arquitetura

### Módulos Principais

#### 1. `core/gpt_telemetry.py`
Responsável por rastrear e exibir o número de chamadas GPT.

**Funções principais:**
- `inicializar_telemetria()` - Inicializa variáveis de telemetria no session state
- `incrementar_contador_gpt(contexto)` - Incrementa contador a cada chamada
- `chamar_gpt_com_telemetria(client, msgs, contexto, **kwargs)` - Wrapper que rastreia chamadas
- `renderizar_badge_gpt_calls()` - Renderiza badge visual no topo do chat
- `obter_estatisticas_gpt()` - Retorna breakdown detalhado por contexto

**Contextos de rastreamento:**
- `diagnostico` - Chamadas na etapa de diagnóstico de gaps
- `coleta_focada` - Chamadas na coleta de dados
- `reescrita` - Chamadas na reescrita do CV
- `linkedin` - Chamadas na otimização do LinkedIn
- `validacao` - Chamadas nas validações
- `outros` - Outras chamadas

#### 2. `core/cv_cache.py`
Gerencia cache e resumo do CV para reduzir tokens.

**Funções principais:**
- `gerar_resumo_cv(client, cv_texto, cargo_alvo)` - Gera resumo conciso (~400 palavras)
- `obter_resumo_cv_cached(client, force_regenerate)` - Obtém resumo do cache ou gera novo
- `get_cv_contexto_para_prompt()` - Retorna contexto do CV para inclusão em prompts
- `invalidar_cache_cv()` - Invalida cache quando CV é modificado
- `inicializar_cache_cv_async(client)` - Pré-gera resumo em background

**Formato do resumo:**
1. **PERFIL**: Senioridade + área (1 linha)
2. **EXPERIÊNCIAS**: Top 3 experiências (empresa, cargo, período, conquistas)
3. **COMPETÊNCIAS**: 5-8 skills mais relevantes
4. **FORMAÇÃO**: Graduação/pós

#### 3. `core/dynamic_questions.py`
Motor de geração dinâmica de perguntas com anti-loop.

**Funções principais:**
- `gerar_proxima_pergunta_dinamica(...)` - Gera pergunta contextual via GPT
- `adicionar_qa_historico(etapa, pergunta, resposta)` - Adiciona Q&A ao histórico
- `obter_historico_qa(etapa)` - Obtém histórico de uma etapa
- `formatar_historico_qa(etapa)` - Formata histórico para prompts
- `verificar_stop_condition_experiencia(historico_qa)` - Verifica se pode avançar
- `detectar_resposta_evasiva(resposta)` - Detecta respostas vagas

**Stop Conditions:**
Uma experiência está completa quando:
- Mínimo de 4-5 perguntas foram respondidas
- Pelo menos 2 de 3 categorias cobertas:
  - ✅ Métricas/impacto (%, R$, crescimento, etc.)
  - ✅ Ferramentas/tecnologias (sistemas, stack, plataformas)
  - ✅ Volume/escala (equipe, projetos, stakeholders)

#### 4. `modules/otimizador/etapa0_diagnostico_dinamico.py`
Diagnóstico de gaps com geração dinâmica de perguntas.

**Funções principais:**
- `gerar_pergunta_dinamica_gap(...)` - Gera pergunta sobre gap específico
- `verificar_resposta_negativa_gap(resposta)` - Detecta se usuário não tem experiência
- `deve_aprofundar_gap(resposta)` - Verifica se resposta requer aprofundamento

**Fluxo:**
1. Pergunta inicial: "Você tem experiência com [gap]?"
2. Se SIM e resposta superficial → aprofundar com GPT
3. Se NÃO → marcar como gap não resolvível e avançar
4. Se detalhado → aceitar e avançar para próximo gap

#### 5. `modules/otimizador/etapa1_coleta_dinamica.py`
Coleta focada com deep dive adaptativo.

**Funções principais:**
- `prompt_etapa1_coleta_dinamica_inicial()` - Prompt inicial da coleta
- `gerar_proxima_pergunta_coleta(client, ultima_resposta)` - Gera próxima pergunta
- `verificar_pronto_para_avancar_coleta()` - Verifica stop conditions
- `gerar_mensagem_transicao_coleta()` - Mensagem de conclusão

**Estratégia de perguntas:**
- Analisa histórico de Q&A para evitar repetição
- Identifica o que ainda falta coletar (métricas, ferramentas, volume)
- Gera pergunta específica baseada no contexto
- Detecta respostas evasivas e reformula

## Integração com o Fluxo Existente

### Session State

Novas variáveis adicionadas em `core/state.py`:

```python
# Telemetria
'gpt_calls_count': 0,
'gpt_calls_by_context': {...},

# Cache
'cv_resumo_cache': None,

# Histórico Q&A
'qa_history_diagnostico': [],
'qa_history_coleta': [],
'qa_history_deep_dive': [],
```

### UI (ui/chat.py)

**Mudanças principais:**
1. Badge de telemetria renderizado no topo
2. Inicialização do cache de CV em background
3. Todas as chamadas GPT usam `chamar_gpt_com_telemetria()`

**Badge de Telemetria:**
```
🟢 Chamadas GPT nesta sessão: 3
```
Cores:
- ⚪ 0 chamadas (cinza)
- 🟢 1-5 chamadas (verde)
- 🟡 6-15 chamadas (amarelo)
- 🟠 16-30 chamadas (laranja)
- 🔴 31+ chamadas (vermelho)

### Processor (modules/otimizador/processor.py)

**Feature Flag:**
```python
ENABLE_DYNAMIC_QUESTIONS = True  # Ativar/desativar geração dinâmica
```

**Integração:**
- `ETAPA_1_COLETA_FOCADA` → usa prompt dinâmico inicial
- `AGUARDANDO_DADOS_COLETA` → gera próximas perguntas dinamicamente
- Verifica stop conditions automaticamente
- Avança quando informações suficientes coletadas

## Guardrails Implementados

### 1. Prevenção de Invenção de Dados

Todos os prompts incluem instruções explícitas:

```
**IMPORTANTE:**
- NÃO invente dados que não estão no CV
- Use APENAS informações fornecidas pelo candidato
- Se faltar contexto, pergunte minimamente
- NUNCA adicione métricas ou conquistas que o usuário não mencionou
```

### 2. Anti-Loop

- Histórico de Q&A rastreado por etapa
- Prompt verifica histórico e instrui: "NÃO repita perguntas já feitas"
- Detecção de perguntas semanticamente similares

### 3. Validação de Respostas

- Detecta respostas negativas (`não tenho`, `não sei`, etc.)
- Detecta respostas evasivas (muito curtas, vagas)
- Reformula ou avança conforme necessário

### 4. Stop Conditions Inteligentes

Evita questionários infinitos através de:
- Mínimo de perguntas por etapa
- Cobertura de categorias (métricas, ferramentas, volume)
- Mensagem clara de transição quando completo

## Redução de Tokens

### Antes (sem cache)
- CV completo enviado em cada prompt: ~3000 tokens
- 10 perguntas na coleta: 10 × 3000 = 30.000 tokens só de CV

### Depois (com cache)
- CV resumido: ~500 tokens
- 10 perguntas na coleta: 10 × 500 = 5.000 tokens
- **Redução de 83% nos tokens de CV**

### Estratégia de Caching

1. **Primeiro acesso:** Gera resumo (~1 chamada GPT, 3500 tokens input)
2. **Próximas chamadas:** Usa resumo cacheado (500 tokens input)
3. **Break-even:** Após 2-3 perguntas, já compensa o custo inicial

## Exemplo de Fluxo

### Diagnóstico (ETAPA_0)

```
🔍 DIAGNÓSTICO ESTRATÉGICO (1/3)

Gap: "Experiência com CRM (Salesforce, HubSpot)"

Você tem experiência com CRM?
```

**Resposta do usuário:** "Sim, usei Salesforce"

```
[Sistema detecta resposta superficial]
[Gera aprofundamento via GPT]

Em qual empresa você usava Salesforce e qual era o volume de dados/leads que gerenciava?
```

**Resposta:** "Na XYZ Corp, gerenciava ~500 leads/mês"

```
[Sistema salva contexto completo]
[Stop condition não atingida ainda - 1 pergunta apenas]
[Avança para próximo gap]
```

### Coleta Focada (ETAPA_1)

```
📝 DEEP DIVE - COLETA FOCADA

Qual foi sua experiência mais recente relevante para [cargo]?
```

**Resposta:** "Gerente de Vendas na ABC, 2020-2023"

```
[Sistema adiciona ao histórico Q&A]
[Gera próxima pergunta via GPT baseada no contexto]

Qual era o tamanho da equipe de vendas que você liderava e qual foi o crescimento de receita no período?
```

**Resposta:** "Equipe de 8 pessoas, crescimento de 150% em ARR"

```
[Sistema detecta: métricas ✓, volume ✓]
[Gera próxima pergunta focada em ferramentas]

Quais ferramentas/sistemas você usava para gestão de vendas?
```

**Resposta:** "Salesforce, Power BI, Excel"

```
[Histórico: 3 perguntas]
[Categorias cobertas: 3/3 (métricas, volume, ferramentas)]
[Stop condition ATINGIDA]

✅ COLETA FOCADA CONCLUÍDA!
Coletei 3 informações importantes...
```

## Testes e Validação

### Checklist de Validação

- [ ] Badge de telemetria aparece no topo do chat
- [ ] Contador incrementa a cada chamada GPT
- [ ] CV é resumido e cacheado após upload
- [ ] Perguntas dinâmicas são geradas sem repetição
- [ ] Stop conditions funcionam (avança automaticamente)
- [ ] Respostas negativas são detectadas corretamente
- [ ] Guardrails previnem invenção de dados

### Como Testar

1. **Telemetria:**
   - Iniciar sessão
   - Verificar badge mostra "0"
   - Passar pelas etapas
   - Observar incremento do contador

2. **Cache de CV:**
   - Upload CV
   - Observar log de geração do resumo
   - Verificar `st.session_state.cv_resumo_cache` existe
   - Conferir tamanho ~400 palavras

3. **Perguntas Dinâmicas:**
   - Modo: `ENABLE_DYNAMIC_QUESTIONS = True`
   - Responder primeira pergunta da coleta
   - Verificar próxima pergunta é diferente e contextual
   - Responder 5+ perguntas
   - Verificar stop condition e mensagem de transição

4. **Anti-Loop:**
   - Responder pergunta sobre ferramenta (ex: "Salesforce")
   - Verificar próxima pergunta NÃO pergunta de novo sobre Salesforce
   - Verificar nova pergunta é sobre métrica/volume/outro gap

## Configuração

### Ativar/Desativar Geração Dinâmica

Em `modules/otimizador/processor.py`:

```python
# True = perguntas geradas dinamicamente via GPT
# False = usar prompts estáticos antigos
ENABLE_DYNAMIC_QUESTIONS = True
```

### Ajustar Stop Conditions

Em `core/dynamic_questions.py`:

```python
def verificar_stop_condition_experiencia(
    historico_qa: List[Dict],
    min_perguntas: int = 4  # Ajustar aqui
) -> bool:
    # ...
    return categorias_cobertas >= 2  # Ajustar aqui (2 de 3 categorias)
```

### Personalizar Resumo do CV

Em `core/cv_cache.py`:

```python
MAX_RESUMO_TOKENS = 500  # Ajustar tamanho máximo do resumo
```

## Métricas e Observabilidade

### Logs

Todos os módulos usam logger Python padrão:

```python
logger.info("Gerando próxima pergunta dinâmica...")
logger.debug(f"Stop condition check: {categorias}/3 categorias")
logger.warning("Resposta evasiva detectada")
logger.error("Erro ao gerar pergunta", exc_info=True)
```

### Estatísticas de Telemetria

Acessar via `obter_estatisticas_gpt()`:

```python
{
    'total': 15,
    'por_contexto': {
        'diagnostico': 3,
        'coleta_focada': 8,
        'reescrita': 2,
        'linkedin': 1,
        'validacao': 1,
        'outros': 0
    }
}
```

## Troubleshooting

### Badge não aparece
- Verificar `renderizar_badge_gpt_calls()` é chamado em `ui/chat.py`
- Verificar `gpt_calls_count` no session state

### Perguntas estáticas ainda sendo usadas
- Verificar `ENABLE_DYNAMIC_QUESTIONS = True` no processor
- Verificar cliente OpenAI está disponível

### Stop conditions não funcionam
- Verificar histórico Q&A está sendo salvo
- Verificar keywords de métricas/ferramentas/volume
- Ajustar threshold de categorias cobertas

### Cache de CV não funciona
- Verificar chamada GPT para gerar resumo não falhou
- Verificar `cv_resumo_cache` no session state
- Força regeneração com `force_regenerate=True`

## Próximos Passos

Possíveis melhorias futuras:

1. **Deep Dive por experiência separada** - Perguntas específicas para cada experiência profissional
2. **Aprendizado de padrões** - Salvar padrões de respostas bem-sucedidas
3. **Sugestões proativas** - Sugerir informações que candidatos costumam esquecer
4. **Validação semântica** - Verificar consistência de métricas (ex: % > 100%)
5. **Export de relatório** - Gerar PDF com histórico de Q&A e estatísticas

## Autoria

Implementado por: GitHub Copilot Agent
Data: Fevereiro 2026
Repositório: kadunobile/Nobile-Protocol
