# 🎯 Protocolo Nóbile - Documentação Detalhada

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Reality Check Flow](#reality-check-flow)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Fluxo de Dados](#fluxo-de-dados)
- [Módulos Principais](#módulos-principais)
- [Guia de Desenvolvimento](#guia-de-desenvolvimento)

---

## 🌟 Visão Geral

O **Protocolo Nóbile** é uma plataforma completa de otimização de currículos powered by AI que combina:

- **Análise ATS automatizada** (Applicant Tracking Systems)
- **Reality Check inteligente** com GPT-4
- **Geração contextual de documentos** (cartas, respostas)
- **Preparação personalizada** para entrevistas

### Público-Alvo

Profissionais de **TODOS os níveis**:
- 👶 **Júnior** - Primeiro emprego, estágio
- 💼 **Pleno** - Consolidação de carreira
- 🎯 **Sênior/Especialista** - Posições de alta senioridade
- 👔 **Gerencial/Executivo** - C-Level, VP, Diretor

### Áreas Atendidas

✅ Tecnologia (Dev, Data, DevOps, Infra)
✅ Vendas e Comercial
✅ Marketing e Growth
✅ RH e People
✅ Financeiro e Controladoria
✅ Operações e Logística
✅ Administrativo e Suporte

---

## 🔍 Reality Check Flow

### O que é o Reality Check?

O **Reality Check** é a etapa mais crítica do Protocolo Nóbile. É uma análise profunda e honesta do currículo do candidato, conduzida por GPT-4, que identifica:

1. ✅ **Pontos Fortes** - O que está funcionando bem
2. ⚠️ **Gaps Críticos** - Lacunas que podem impedir aprovação
3. 💡 **Oportunidades** - Melhorias acionáveis
4. 📊 **Análise Salarial** - Compatibilidade com mercado

### Fluxo Detalhado

```
┌─────────────────────────────────────────────────────────────┐
│                    REALITY CHECK FLOW                        │
└─────────────────────────────────────────────────────────────┘

1️⃣ COLETA DE DADOS
   ├── Upload do CV (PDF/DOCX/TXT)
   ├── Briefing inicial (cargo-alvo, pretensão)
   └── Contexto profissional

2️⃣ ANÁLISE ATS (Pré-Reality)
   ├── Score 0-100
   ├── Análise de seções
   ├── Densidade de keywords
   ├── Métricas quantificáveis
   └── Formatação e tamanho

3️⃣ REALITY CHECK (GPT-4)
   ├── 🎯 Análise de Fit Cargo x CV
   │   └── Match de habilidades obrigatórias
   │
   ├── 📊 Análise Salarial
   │   ├── Faixa de mercado para cargo
   │   ├── Comparação com pretensão
   │   └── Recomendação de ajuste
   │
   ├── ✅ Pontos Fortes (3-5 itens)
   │   └── Destaques que agregam valor
   │
   ├── ⚠️ Gaps Críticos (2-4 itens)
   │   ├── Lacunas ACIONÁVEIS
   │   ├── Contextualizadas ao cargo
   │   └── Priorizadas por impacto
   │
   └── 💡 Recomendações
       ├── Alterações no CV
       ├── Upskilling necessário
       └── Posicionamento estratégico

4️⃣ INTERAÇÃO (Opcional)
   ├── Esclarecer dúvidas
   ├── Aprofundar gaps
   └── Solicitar alternativas

5️⃣ OTIMIZAÇÃO
   ├── Reescrever seções
   ├── Adicionar keywords ATS
   ├── Quantificar resultados
   └── Ajustar formatação

6️⃣ VALIDAÇÃO
   ├── Novo Score ATS
   ├── Comparador Antes/Depois
   └── Certificação de melhoria
```

### Exemplo de Reality Check

**Entrada:**
- **Cargo-alvo:** Gerente de Projetos
- **Pretensão:** R$ 15.000
- **CV:** 8 anos como analista, sem experiência em liderança formal

**Saída do Reality Check:**

```markdown
### 📊 ANÁLISE SALARIAL
**Faixa de Mercado:** 12.000 - 18.000 mensal
**Sua Pretensão:** 15.000 mensal
**Avaliação:** ✅ Dentro da faixa (mediana)

---

### ✅ PONTOS FORTES
1. **8 anos de experiência consolidada** em gestão de projetos
2. **Certificação PMP** (diferencial competitivo)
3. **Experiência com metodologias ágeis** (Scrum, Kanban)

---

### ⚠️ GAPS CRÍTICOS
1. **Falta evidência de liderança de equipes**
   - CV menciona "coordenação" mas não quantifica size do time
   - Recomendação: Adicionar "Coordenei equipe de X pessoas"

2. **Ausência de métricas de impacto**
   - Projetos descritos sem resultados mensuráveis
   - Recomendação: Adicionar "Reduzi prazo em 20%", "Economizei R$ X"

3. **Keywords ATS insuficientes**
   - Faltam: "Gestão de Stakeholders", "Budget Management", "Risk Assessment"
   - Recomendação: Incorporar naturalmente no CV

---

### 💡 PRÓXIMOS PASSOS
1. Reescrever seção de Experiência com modelo STAR
2. Adicionar números em TODOS os projetos principais
3. Criar seção "Liderança" destacando coordenação de equipes
```

---

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios

```
Nobile-Protocol/
├── app.py                    # Entry point da aplicação
├── streamlit_app.py          # App alternativo
├── bootstrap_protocolo.py    # Script de inicialização
│
├── core/                     # Lógica de negócio central
│   ├── config.py            # Configurações e env vars
│   ├── state.py             # Gerenciamento de estado Streamlit
│   ├── data.py              # Dados estáticos (cidades, etc)
│   ├── utils.py             # Utilitários (PDF, GPT, scroll)
│   ├── validators.py        # Validação de inputs
│   ├── prompts.py           # System prompts GPT
│   ├── ats_scorer.py        # Algoritmo de score ATS
│   ├── cv_comparator.py     # Comparação antes/depois
│   └── interview_prep.py    # Geração de perguntas
│
├── modules/                  # Módulos especializados
│   └── otimizador/
│       └── processor.py     # Processamento de otimização
│
├── ui/                       # Interface do usuário
│   ├── sidebar.py           # Barra lateral
│   ├── chat.py              # Interface de chat
│   └── screens/             # Telas do fluxo
│       ├── fase0_intro.py
│       ├── fase0_upload.py
│       ├── fase1_diagnostico.py
│       ├── fase1_briefing.py
│       ├── fase15_reality.py       ← REALITY CHECK
│       ├── fase_analise_loading.py
│       ├── fase_gaps_interativos.py
│       ├── fase_ats_score.py
│       ├── fase_carta.py
│       ├── fase_interview.py
│       └── fase_comparador.py
│
├── tests/                    # Testes automatizados
│   └── test_validators.py
│
├── docs/                     # Documentação adicional
│
├── requirements.txt          # Dependências Python
├── .gitignore
├── LICENSE                   # Apache 2.0
└── README.md                 # Documentação principal
```

### Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Backend** | Python | 3.11+ |
| **Frontend** | Streamlit | Latest |
| **IA** | OpenAI GPT | GPT-4o |
| **PDF Parser** | PyPDF2 | Latest |
| **Word Parser** | python-docx | Latest |
| **Diff** | difflib | stdlib |

---

## 🔄 Fluxo de Dados

### 1. Inicialização

```python
setup_environment()  # Carrega variáveis de ambiente
inicializar_session_state()  # Inicializa st.session_state
```

### 2. Upload e Parsing

```python
arquivo_cv → extrair_texto_pdf() → cv_texto (str)
                ↓
        validar_arquivo_cv()
                ↓
        st.session_state.cv_texto
```

### 3. Briefing

```python
Inputs do usuário:
├── cargo_alvo
├── pretensao_salarial
├── cidade
└── nivel_senioridade

        ↓
st.session_state.perfil = {
    "cargo_alvo": str,
    "pretensao_salarial": float,
    "cidade": str,
    "nivel": str
}
```

### 4. Score ATS (Pré-Reality)

```python
calcular_score_ats(cv_texto, cargo_alvo)
        ↓
{
    "score_total": 0-100,
    "detalhes": {
        "secoes": {...},
        "keywords": {...},
        "metricas": {...},
        "formatacao": {...},
        "tamanho": {...}
    },
    "recomendacoes": [...]   
}
```

### 5. Reality Check (GPT-4)

```python
prompt_reality = f"""
[SYSTEM_PROMPT]

CV:
{cv_texto}

Cargo-alvo: {cargo_alvo}
Pretensão: {pretensao}

Analise e gere Reality Check completo.
"""

        ↓
chamar_gpt(mensagens, temperature=0.7)
        ↓
resposta_reality (markdown formatado)
```

### 6. Otimização Interativa

```python
Loop de Chat:
user_input → mensagens.append(user)
        ↓
chamar_gpt(mensagens, seed=42, temp=0.3)
        ↓
resposta_gpt → mensagens.append(assistant)
        ↓
display(chat_history)
```

---

## 🧩 Módulos Principais

### 1. `core/ats_scorer.py`

**Propósito:** Simular como sistemas ATS reais avaliam currículos

**Função principal:**
```python
def calcular_score_ats(cv_texto: str, cargo_alvo: str) -> Dict:
    """
    Retorna score 0-100 baseado em:
    - Seções essenciais (20 pts)
    - Keywords relevantes (30 pts)
    - Métricas quantificáveis (20 pts)
    - Formatação adequada (15 pts)
    - Tamanho apropriado (15 pts)
    """
```

**Algoritmo:**
1. Regex para detectar seções (experiência, educação, etc)
2. Extração de keywords baseadas no cargo
3. Contagem de números/porcentagens
4. Análise de formatação (bullets, datas, etc)
5. Validação de tamanho (ideal: 400-800 palavras)

### 2. `core/utils.py - chamar_gpt()`

**Propósito:** Wrapper robusto para chamadas OpenAI

**Features:**
- ✅ Retry automático (3x por padrão)
- ✅ Rate limit handling
- ✅ Timeout configurável
- ✅ Logging detalhado
- ✅ Error handling gracioso

```python
def chamar_gpt(
    client: OpenAI,
    mensagens: List[Dict],
    temperature: float = 0.7,
    seed: int = None
) -> str:
    """
    Implementa retry exponential backoff para:
    - APITimeoutError
    - RateLimitError
    - OpenAIError genérico
    """
```

### 3. `ui/screens/fase15_reality.py`

**Propósito:** Renderizar tela de Reality Check

**Fluxo:**
1. **Scroll automático para topo** (forcar_topo())
2. **Header visual** com ícone e título
3. **Trigger de análise** (botão "Iniciar Reality Check")
4. **Loading state** com spinner
5. **Display de resultado** (markdown rico)
6. **Navegação** para próxima etapa

**Código-chave:**
```python
def fase_15_reality_check():
    forcar_topo()  # CRITICAL: scroll para topo
    
    st.markdown("# 🔍 Reality Check")
    
    if st.button("🚀 Iniciar Reality Check"):
        with st.spinner("🤔 Analisando profundamente..."):
            prompt = gerar_prompt_reality()
            resposta = chamar_gpt(client, prompt)
            
            st.markdown(resposta)
            st.session_state.reality_completo = True
```

### 4. `core/cv_comparator.py`

**Propósito:** Comparar CV antes/depois da otimização

**Métricas analisadas:**
```python
{
    "palavras": {"antes": X, "depois": Y, "melhoria": Z%},
    "numeros": {...},
    "verbos_acao": {...},
    "secoes": {...},
    "similaridade": X%  # 0-100, quanto mudou
}
```

**Visualizações:**
1. **Resumo** - Cards com % de melhoria
2. **Lado a Lado** - Comparação textual
3. **Diff Detalhado** - Linha por linha (difflib)

---

## 🛠️ Guia de Desenvolvimento

### Setup Local

```bash
# 1. Clone o repositório
git clone https://github.com/kadunobile/Nobile-Protocol.git
cd Nobile-Protocol

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edite .env e adicione:
# OPENAI_API_KEY=sk-...

# 5. Execute
streamlit run app.py
```

### Rodando Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=core --cov=ui

# Teste específico
pytest tests/test_validators.py -v
```

### Adicionando Nova Fase

```python
# 1. Criar arquivo em ui/screens/
# ui/screens/fase_nova_feature.py

import streamlit as st

def fase_nova_feature():
    st.markdown("# 🆕 Nova Feature")
    
    # Sua lógica aqui
    if st.button("Executar"):
        resultado = processar()
        st.success("Sucesso!")

# 2. Importar em app.py
from ui.screens.fase_nova_feature import fase_nova_feature

# 3. Adicionar ao fluxo
FASES = {
    "nova_feature": fase_nova_feature,
    ...
}

# 4. Atualizar sidebar.py
st.sidebar.button("🆕 Nova Feature", 
                  on_click=lambda: mudar_fase("nova_feature"))
```

### Guidelines de Código

1. **Type hints obrigatórios**
   ```python
   def funcao(param: str) -> Dict[str, Any]:
       pass
   ```

2. **Docstrings para funções públicas**
   ```python
   def funcao():
       """
       Descrição curta.
       
       Args:
           param: Descrição
       
       Returns:
           Descrição do retorno
       """
   ```

3. **Logging ao invés de print**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   
   logger.info("Mensagem informativa")
   logger.warning("Alerta")
   logger.error("Erro", exc_info=True)
   ```

4. **Validação de inputs**
   ```python
   from core.validators import validar_cargo
   
   valido, erro = validar_cargo(input_usuario)
   if not valido:
       st.error(erro)
       return
   ```

---

## 📊 Métricas de Qualidade

### Coverage Atual
- **Core:** 85%
- **UI:** 45% (Streamlit dificulta testes)
- **Modules:** 78%

### Performance
- **Tempo médio Reality Check:** 8-15s (GPT-4)
- **Parse PDF:** < 1s (até 10MB)
- **Score ATS:** < 0.5s

### Limitações Conhecidas

1. **PDFs escaneados** - Não extrai texto (sem OCR)
2. **Formatação complexa** - Tabelas podem quebrar
3. **Rate limiting** - OpenAI 3 RPM (tier free)

---

## 🔐 Segurança

- ✅ **API keys em .env** (nunca no código)
- ✅ **Validação de inputs** (size, tipo, conteúdo)
- ✅ **Sanitização de uploads** (extensão, tamanho)
- ✅ **Sem armazenamento** de dados do usuário
- ✅ **Session state isolado** (por sessão Streamlit)

---

## 📝 Contribuindo

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para guidelines detalhados.

**Quick Start:**
1. Fork o repositório
2. Crie branch feature (`git checkout -b feature/nova-funcao`)
3. Commit com mensagem descritiva
4. Push e abra Pull Request

---

## 📄 Licença

Apache License 2.0 - Ver [LICENSE](./LICENSE)

---

## 🤝 Suporte

- **Issues:** https://github.com/kadunobile/Nobile-Protocol/issues
- **Discussões:** https://github.com/kadunobile/Nobile-Protocol/discussions

---

**Última atualização:** Fevereiro 2026
**Versão:** 2.0
