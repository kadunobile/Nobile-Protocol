# 🎯 Protocolo Nóbile

**Inteligência Artificial para Otimização de Currículos e Preparação para Processos Seletivos**

O Protocolo Nóbile é uma plataforma completa que utiliza IA (GPT) para ajudar profissionais de **todos os níveis e áreas** a aprimorarem seus currículos e se prepararem para entrevistas de emprego.

## ✨ Funcionalidades Principais

### 🔍 **Análise e Otimização de CV**
- **Score ATS** - Avaliação de compatibilidade com sistemas de rastreamento (ATS - Applicant Tracking System)
- **Reality Check** - Análise crítica profunda com identificação de gaps e pontos fortes
- **Otimização Inteligente** - Sugestões personalizadas baseadas no cargo-alvo

### 📝 **Geração de Documentos**
- **Carta de Apresentação** - Cartas personalizadas com 4 tons (Formal, Entusiasmado, Técnico, Criativo)
- **Download TXT** - Exportação fácil de documentos gerados

### 🎤 **Preparação para Entrevistas**
- **5 Tipos de Entrevista** - RH, Técnica, Gestor, Painel, Case de Negócio
- **10 Perguntas Personalizadas** - Baseadas no seu CV e cargo-alvo
- **Método STAR** - Guia estruturado para respostas comportamentais
- **Rascunhos de Resposta** - Campos para praticar suas respostas

### 🔄 **Comparador de CVs**
- **Análise Antes/Depois** - Compare CV original com versão otimizada
- **Score ATS Comparativo** - Veja exatamente quanto melhorou
- **5 Categorias** - Seções, Palavras-Chave, Métricas, Formatação, Tamanho
- **Diff Detalhado** - Visualização linha a linha das mudanças

## 🚀 Como Funciona

### Fluxo Completo:
1. **📄 Upload do CV** - Cole seu currículo em texto
2. **🎯 Briefing Inicial** - Defina cargo-alvo e objetivos
3. **📊 Score ATS** - Receba pontuação inicial (0-100)
4. **🔍 Reality Check** - Análise profunda com GPT
5. **💬 Chat Interativo** - Otimize seu CV com IA
6. **📝 Gerar Carta** - Crie carta de apresentação personalizada
7. **🎤 Prep. Entrevista** - Prepare-se com perguntas personalizadas
8. **🔄 Comparar CVs** - Valide suas melhorias

## 📚 Glossário de Termos

### **ATS (Applicant Tracking System)**
Sistema de Rastreamento de Candidatos usado por empresas para filtrar currículos automaticamente antes de chegarem ao recrutador humano. O Protocolo Nóbile otimiza seu CV para passar por esses sistemas.

**Exemplos de ATS**: Workday, Greenhouse, Lever, BambooHR, SAP SuccessFactors

### **Score ATS**
Pontuação de 0 a 100 que indica a probabilidade do seu CV ser aprovado por sistemas automatizados:
- **0-40**: ❌ Baixa chance (precisa melhorias urgentes)
- **41-70**: ⚠️ Média chance (pode ser melhorado)
- **71-100**: ✅ Alta chance (bem otimizado)

### **Palavras-Chave (Keywords)**
Termos técnicos, habilidades e competências que os sistemas ATS procuram. Exemplo: "Python", "Gestão de Projetos", "Excel Avançado".

### **Método STAR**
Técnica para responder perguntas comportamentais em entrevistas:
- **S**ituação: Contexto do desafio
- **T**arefa: Seu papel/objetivo
- **A**ção: O que você fez
- **R**esultado: Impacto mensurável

### **Reality Check**
Análise crítica e honesta do seu CV, identificando:
- ✅ Pontos fortes
- ❌ Gaps (lacunas)
- 💡 Oportunidades de melhoria

## 🛠️ Tecnologias

- **Backend**: Python 3.11+
- **Frontend**: Streamlit
- **IA**: OpenAI GPT-4
- **Análise**: difflib (stdlib), regex
- **Sem dependências externas extras!**

## ⚙️ Instalação

### Pré-requisitos
- Python 3.11+
- Chave API OpenAI

### Passos
```bash
# Clone o repositório
git clone https://github.com/kadunobile/Nobile-Protocol.git
cd Nobile-Protocol

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY

# Execute
streamlit run app.py
```

Acesse: http://localhost:8501

## 📦 Novidades - Versão 2.0

### ✨ Novas Funcionalidades (Fev 2026)

#### 📝 **Gerador de Carta de Apresentação**
- Formulário completo (empresa, cargo, recrutador, tom)
- 4 tons de escrita personalizáveis
- Geração contextualizada usando seu CV
- Editor com download TXT

#### 🎤 **Preparação para Entrevista**
- 5 tipos de entrevista (RH, Técnica, Gestor, Painel, Case)
- 10 perguntas personalizadas geradas por IA
- Contexto de cada pergunta + dicas STAR
- Campos para rascunhar respostas
- Download de todas as perguntas

#### 🔄 **Comparador de CVs**
- Upload de CV otimizado
- Comparação lado a lado com scores ATS
- Breakdown por 5 categorias (Seções, Keywords, Métricas, Formatação, Tamanho)
- 3 visualizações: Resumo, Lado a Lado, Diff Detalhado
- Celebração visual quando score melhora! 🎉

### 🔧 Melhorias Técnicas
- Regex robusto para parse de JSON
- Constantes extraídas (`PREVIEW_MAX_LENGTH`)
- Truncamento condicional correto
- Formato de data DD/MM/YYYY
- 51 testes automatizados passando
