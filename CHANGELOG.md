# 📦 Histórico de Versões

## [2.0.0] - Fevereiro 2026

### ✨ Novas Funcionalidades

#### 📝 Gerador de Carta de Apresentação
- Formulário completo (empresa, cargo, recrutador opcional, descrição da vaga)
- 4 tons de escrita: Formal, Entusiasmado, Técnico, Criativo
- Geração contextualizada usando CV do candidato
- Editor de texto com preview
- Download em TXT
- Botão para regenerar versões alternativas

#### 🎤 Preparação para Entrevista
- Seleção de 5 tipos de entrevista:
  - Entrevista Inicial com RH
  - Entrevista Técnica
  - Entrevista com Gestor
  - Painel com Múltiplos Entrevistadores
  - Case de Negócio
- Geração de 10 perguntas personalizadas via GPT
- Contexto de cada pergunta (por que perguntam isso?)
- Dicas de resposta baseadas no CV
- Método STAR explicado
- Campos para rascunhar respostas
- Download de todas as perguntas em TXT
- Expander com dicas gerais (antes/durante/depois da entrevista)

#### 🔄 Comparador de CVs
- Upload de CV otimizado para comparação
- Scores ATS lado a lado (original vs. otimizado)
- Delta visual com cores
- Breakdown detalhado por 5 categorias:
  - Seções Essenciais (20 pontos)
  - Palavras-Chave (30 pontos)
  - Métricas Quantificáveis (20 pontos)
  - Formatação (15 pontos)
  - Tamanho Adequado (15 pontos)
- Emojis visuais: 🟢 melhorou | 🔴 piorou | ⚪ igual
- 3 tabs de visualização:
  - Resumo: estatísticas (palavras, caracteres, dígitos)
  - Lado a Lado: preview dos primeiros 1000 caracteres
  - Diff Detalhado: unified diff linha a linha
- Celebração com `st.balloons()` quando score melhora
- Recomendações finais personalizadas

### 🔧 Melhorias Técnicas

- Regex robusto para parse de JSON: `r'\{[\s\S]*"perguntas"[\s\S]*\[[\s\S]*\][\s\S]*\}'`
- Constante extraída: `PREVIEW_MAX_LENGTH = 1000`
- Truncamento condicional correto: `text[:1000] + ('...' if len(text) > 1000 else '')`
- Formato de data padronizado: DD/MM/YYYY
- Métrica renomeada: "Números encontrados" → "Dígitos" (mais preciso)
- 51 testes automatizados passando
- Zero novas dependências (usa stdlib: datetime, json, re, difflib)

### 📝 Documentação

- README.md atualizado com todas as funcionalidades
- Glossário de termos (ATS, Score, Keywords, STAR, Reality Check)
- Reposicionamento: ferramenta universal (não apenas executivos)
- Changelog criado
- Tela de boas-vindas com explicações

### 🎯 Reposicionamento

- Removida limitação "executivos e estratégicos"
- Agora atende **todos os níveis**: júnior, pleno, sênior, gerente, diretor, C-level
- Suporta **todas as áreas**: Tech, Vendas, Marketing, RH, Financeiro, Operações, Design, etc.
- Prompts atualizados para adaptar linguagem ao nível do cargo
- Explicações de termos técnicos adicionadas em todas as telas

---

## [1.0.0] - Janeiro 2026

### 🎉 Lançamento Inicial

- Upload de CV em texto
- Briefing inicial (cargo-alvo, objetivos)
- Score ATS (0-100)
- Reality Check (análise crítica com GPT)
- Chat interativo para otimização
- Sistema de fases progressivo
- Sidebar com navegação
