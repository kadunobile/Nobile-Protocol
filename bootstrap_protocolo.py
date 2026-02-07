import os

FILES = {
    "app.py": """import streamlit as st
from core.config import setup_environment
from core.state import inicializar_session_state
from ui.sidebar import renderizar_sidebar
from ui.screens.fase0_intro import fase_0_intro
from ui.screens.fase0_upload import fase_0_upload
from ui.screens.fase1_diagnostico import fase_1_diagnostico
from ui.screens.fase1_briefing import fase_1_briefing
from ui.screens.fase15_reality import fase_15_reality_check
from ui.chat import fase_chat

setup_environment()

st.set_page_config(
    page_title="Protocolo Nóbile",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown('''<style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    .stApp {background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%); color: #e0e0e0;} 
    .block-container {max-width: 800px !important; margin: 0 auto !important; padding: 2rem; width: 100%;} 
    h1 {color: #ffffff; text-align: center; font-size: 2rem;} 
    h2 {color: #ffffff; font-size: 1.5rem;} 
    h3 {color: #e0e0e0; font-size: 1.2rem;} 
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #16213e 0%, #0f3460 100%); border-right: 2px solid #e94560;} 
    .stButton > button {width: 100%; background: linear-gradient(90deg, #e94560 0%, #d32f4f 100%); color: white; border: none; padding: 0.75rem; font-weight: 600; border-radius: 8px; transition: all 0.3s; min-height: 48px;} 
    .stButton > button:hover {background: linear-gradient(90deg, #d32f4f 0%, #b71c3c 100%); transform: translateY(-2px);} 
    .stButton > button:disabled {background: #555555; color: #888888; transform: none;}
    
    /* Mobile-specific styles */
    @media screen and (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.25rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        .stButton > button {
            padding: 0.875rem !important;
            font-size: 0.95rem !important;
            min-height: 52px !important;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        /* Stack columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Improve form inputs on mobile */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 0.75rem !important;
        }
        
        /* Better chat input on mobile */
        .stChatInput > div > div > textarea {
            font-size: 16px !important;
            min-height: 56px !important;
        }
        
        /* Improve info/warning boxes on mobile */
        .stInfo, .stWarning, .stSuccess, .stError {
            padding: 0.75rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Better chat messages on mobile */
        [data-testid="stChatMessage"] {
            padding: 0.75rem !important;
        }
        
        /* Better markdown rendering on mobile */
        .stMarkdown {
            font-size: 0.95rem !important;
        }
    }
    
    /* Small mobile devices */
    @media screen and (max-width: 480px) {
        .block-container {
            padding: 0.75rem !important;
        }
        
        h1 {
            font-size: 1.3rem !important;
        }
        
        h2 {
            font-size: 1.1rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
        
        .stButton > button {
            padding: 1rem !important;
            min-height: 56px !important;
        }
        
        .stMarkdown {
            font-size: 0.9rem !important;
        }
    }
    </style>''', unsafe_allow_html=True)

def main():
    inject_custom_css()
    inicializar_session_state()

    if st.session_state.fase not in ['FASE_0_INTRO', 'FASE_0_UPLOAD']:
        renderizar_sidebar()

    fases = {
        'FASE_0_INTRO': fase_0_intro,
        'FASE_0_UPLOAD': fase_0_upload,
        'FASE_1_DIAGNOSTICO': fase_1_diagnostico,
        'FASE_1_BRIEFING': fase_1_briefing,
        'FASE_15_REALITY': fase_15_reality_check,
        'CHAT': fase_chat
    }

    fases[st.session_state.fase]()

if __name__ == "__main__":
    main()
""",
    "core/__init__.py": "",
    "core/config.py": """import os
import importlib

def setup_environment():
    try:
        cfg = importlib.import_module("config")
        if hasattr(cfg, "OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = cfg.OPENAI_API_KEY
    except Exception:
        pass

    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except Exception:
        pass
""",
    "core/data.py": """CIDADES_BRASIL = [
    "São Paulo/SP", "Rio de Janeiro/RJ", "Belo Horizonte/MG", "Brasília/DF",
    "Curitiba/PR", "Fortaleza/CE", "Salvador/BA", "Manaus/AM", "Recife/PE",
    "Porto Alegre/RS", "Goiânia/GO", "Belém/PA", "Florianópolis/SC",
    "Campinas/SP", "Santos/SP", "Ribeirão Preto/SP", "Guarulhos/SP",
    "Sorocaba/SP", "Niterói/RJ", "Joinville/SC", "Londrina/PR",
    "Uberlândia/MG", "Juiz de Fora/MG", "Maringá/PR", "Blumenau/SC",
    "Remoto - Nacional", "Remoto - Internacional", "Híbrido"
]
""",
    "core/prompts.py": """SYSTEM_PROMPT = \"""
# SYSTEM RESET & CONTEXT ISOLATION
CRITICAL: Ignore any previous context. Treat this as a Blank Slate.
Source of Truth: Analysis based EXCLUSIVELY on the PDF/Text provided and user answers.

# ROLE
Você é a IA do Protocolo Nóbile - Headhunter Executivo Sênior, Especialista em ATS, Salários, Carreira e LinkedIn.
Regra de Ouro: Não aceita textos rasos. Constrói perfis de Alta Performance. Pausa, entrevista e valida em cada etapa.

# FORMATAÇÃO OBRIGATÓRIA DE VALORES MONETÁRIOS
- SEMPRE escreva valores assim: R$ 25.000
- O cifrão R$ deve estar COLADO, seguido de ESPAÇO, seguido do NÚMERO com PONTO separador
- NUNCA escreva "R 25.000" (faltando cifrão)
- NUNCA escreva "R$25.000" (faltando espaço)
- NUNCA use parênteses em valores
- Escreva "mensal" como palavra separada

# OUTRAS REGRAS DE FORMATAÇÃO
- Títulos: ### 📊 ANÁLISE SALARIAL (sem asteriscos ao redor)
- NUNCA mostre o CV completo do candidato de volta
- Use emojis estratégicos: 🎯 📊 ⚠️ ✅ 🚀
- Use --- para separar seções
- Labels em negrito: **Pretensão Informada:** R$ 25.000 mensal
\"""",
    "core/state.py": """import streamlit as st

def inicializar_session_state():
    defaults = {
        'fase': 'FASE_0_INTRO',
        'cv_texto': None,
        'perfil': {},
        'mensagens': [],
        'analise_inicial': None,
        'openai_client': None,
        'modulo_ativo': None,
        'etapa_modulo': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
""",
    "core/utils.py": """import re
import streamlit as st
import PyPDF2
import streamlit.components.v1 as components
from openai import OpenAI
from core.data import CIDADES_BRASIL

def corrigir_formatacao(texto):
    if not texto:
        return texto
    texto = re.sub(r'(?<!\\w)R\\s+(\\d[\\d\\.]+)', r'R$ \\1', texto)
    texto = re.sub(r'\\*\\*R\\s+(\\d[\\d\\.]+)', r'**R$ \\1', texto)
    texto = re.sub(r'R\\$(\\d)', r'R$ \\1', texto)
    texto = re.sub(r'R\\$\\s{2,}(\\d)', r'R$ \\1', texto)
    texto = texto.replace('R$ $', 'R$')
    texto = texto.replace('R$  ', 'R$ ')
    return texto

def extrair_texto_pdf(arquivo):
    try:
        pdf_reader = PyPDF2.PdfReader(arquivo)
        return "".join([p.extract_text() for p in pdf_reader.pages])
    except Exception as e:
        st.error(f"Erro ao ler PDF: {e}")
        return None

def inicializar_cliente_openai(key):
    try:
        return OpenAI(api_key=key)
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None

def chamar_gpt(client, msgs):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=msgs,
            temperature=0.7,
            max_tokens=4000
        )
        texto_raw = response.choices[0].message.content
        return corrigir_formatacao(texto_raw)
    except Exception as e:
        st.error(f"Erro GPT: {e}")
        return None

def scroll_topo():
    components.html(\"\"\"
        <script>
            var main = window.parent.document.querySelector('section.main');
            if (main) main.scrollTop = 0;
            setTimeout(function() {
                var main = window.parent.document.querySelector('section.main');
                if (main) main.scrollTop = 0;
            }, 100);
            setTimeout(function() {
                var main = window.parent.document.querySelector('section.main');
                if (main) main.scrollTop = 0;
            }, 300);
            setTimeout(function() {
                var main = window.parent.document.querySelector('section.main');
                if (main) main.scrollTop = 0;
            }, 500);
        </script>
    \"\"\", height=0)

def filtrar_cidades(texto):
    if not texto:
        return CIDADES_BRASIL[:10]
    return [c for c in CIDADES_BRASIL if texto.lower() in c.lower()]
""",
    "ui/__init__.py": "",
    "ui/sidebar.py": """import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt

def renderizar_sidebar():
    with st.sidebar:
        st.markdown("# 🎯 Protocolo Nóbile")
        st.markdown("---")

        if st.session_state.perfil.get('cargo_alvo'):
            st.markdown("### 📋 Seu Perfil")
            st.info(f\"\"\"
**Objetivo:** {st.session_state.perfil.get('objetivo', 'N/A')}
**Cargo:** {st.session_state.perfil['cargo_alvo']}
**Pretensão:** R$ {st.session_state.perfil.get('pretensao_salarial', 'N/A')} mensal
**Local:** {st.session_state.perfil.get('localizacao', 'N/A')}
            \"\"\")
            st.markdown("---")

        st.markdown("### ⚡ Comandos")
        habilitado = st.session_state.fase == 'CHAT'

        if st.button("🔧 Otimizar CV + LinkedIn", disabled=not habilitado, key="b1", use_container_width=True):
            st.session_state.mensagens = []
            st.session_state.modulo_ativo = None
            st.session_state.etapa_modulo = None
            st.session_state.force_scroll_top = True  # Force scroll to top

            cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
            intro = f\"\"\"# 🔧 OTIMIZAÇÃO COMPLETA DE CV
## PROTOCOLO NÓBILE

Vou reescrever seu CV **experiência por experiência** seguindo metodologia de Alta Performance.

---

## 📋 O QUE FAREMOS:

### **ETAPA 1: Mapeamento de SEO**
→ 10 keywords essenciais para **{cargo}**  
→ Comparação com seu CV atual

### **ETAPA 2: Interrogatório Tático**
→ Análise de CADA experiência profissional  
→ Cobrança de dados quantitativos

### **ETAPA 3: Curadoria Estratégica**
→ Projetos divisores de águas  
→ Diferenciais competitivos

### **ETAPA 4: Engenharia de Texto**
→ Reescrita com estruturas otimizadas para ATS

### **ETAPA 5: Validação Final**
→ Revisão e ajustes

### **ETAPA 6: Arquivo Mestre**
→ Compilação completa para exportação

### **ETAPA 7: Instruções de Exportação**
→ Como usar no FlowCV e LinkedIn

---

⏱️ **TEMPO ESTIMADO:** 15-20 minutos  
📋 **VOCÊ PRECISARÁ:** Dados de impacto financeiro, tamanho de equipe, resultados

---

🚀 **Vamos começar pela ETAPA 1.**\"\"\"

            st.session_state.mensagens = [
                {"role": "system", "content": SYSTEM_PROMPT + f\"\\n\\nCV DO CANDIDATO (uso interno - NUNCA mostre de volta): {st.session_state.cv_texto}\\n\\nCARGO-ALVO: {cargo}\"},
                {"role": "assistant", "content": intro}
            ]
            st.session_state.modulo_ativo = "OTIMIZADOR"
            st.session_state.etapa_modulo = "ETAPA_1_SEO"  # Start ETAPA 1 directly
            st.rerun()

        if st.button("🏢 Empresas Discovery", disabled=not habilitado, key="b2", use_container_width=True):
            with st.spinner("🔍 Buscando empresas..."):
                cargo = st.session_state.perfil.get('cargo_alvo', 'seu cargo')
                local = st.session_state.perfil.get('localizacao', 'Brasil')
                st.session_state.mensagens = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f\"\"\"[/empresas_discovery]

Perfil:
- Cargo: {cargo}
- Local: {local}
- Pretensão: R$ {st.session_state.perfil.get('pretensao_salarial', 'N/A')} mensal

Etapa 1: Pergunte sobre fit cultural.
Etapa 2: Liste 5-10 empresas com Match + Localização + Cultura.
Adicione o "Porquê" e Raio-X Salarial.\"\"\"}
                ]
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
                    st.session_state.modulo_ativo = "EMPRESAS"
                    st.rerun()

        if st.button("🎯 Analisar Vaga (Fit)", disabled=not habilitado, key="b3", use_container_width=True):
            st.session_state.aguardando_vaga = True
            st.session_state.modulo_ativo = "FIT"
            st.info("👇 Cole a descrição da vaga no chat")

        if st.button("🎤 Prep. Entrevista", disabled=not habilitado, key="b4", use_container_width=True):
            with st.spinner("📚 Preparando..."):
                cargo = st.session_state.perfil.get('cargo_alvo', 'seu cargo')
                st.session_state.mensagens = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f\"\"\"[/entrevista]

Cargo: {cargo}

Etapa 1: Dossiê + Talking Points
Etapa 2: Simulação STAR com 5 perguntas difíceis + respostas modelo\"\"\"}
                ]
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
                    st.session_state.modulo_ativo = "ENTREVISTA"
                    st.rerun()

        if st.button("📊 Análise Mercado", disabled=not habilitado, key="b5", use_container_width=True):
            with st.spinner("📈 Analisando..."):
                cargo = st.session_state.perfil.get('cargo_alvo', 'seu cargo')
                local = st.session_state.perfil.get('localizacao', 'Brasil')
                st.session_state.mensagens = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f\"\"\"Analise mercado para {cargo} em {local}:
1. Tendências salariais
2. Skills em alta
3. Setores em crescimento
4. Certificações valorizadas\"\"\"}
                ]
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
                    st.session_state.modulo_ativo = "MERCADO"
                    st.rerun()

        st.markdown("---")
        if not habilitado:
            st.warning("⚠️ Complete o briefing para desbloquear")

        st.markdown("---")
        if st.button("🔄 Reiniciar Tudo", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
""",
    "ui/chat.py": """import streamlit as st
from core.utils import chamar_gpt, scroll_topo
from modules.otimizador.processor import processar_modulo_otimizador

def fase_chat():
    st.markdown("# 💬 Sessão Ativa - Protocolo Nóbile")
    st.markdown("---")

    for msg in st.session_state.mensagens:
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
        elif msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])

    scroll_topo()

    if prompt := st.chat_input("Digite sua pergunta ou resposta..."):
        st.session_state.mensagens.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.get('modulo_ativo') == 'OTIMIZADOR':
            prompt_otimizador = processar_modulo_otimizador(prompt)

            if prompt_otimizador:
                st.session_state.mensagens.append({"role": "user", "content": prompt_otimizador})
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Processando etapa..."):
                        resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                        if resp:
                            st.markdown(resp)
                            st.session_state.mensagens.append({"role": "assistant", "content": resp})
                return

        if hasattr(st.session_state, 'aguardando_vaga') and st.session_state.aguardando_vaga:
            cargo = st.session_state.perfil.get('cargo_alvo', 'N/A')
            pretensao = st.session_state.perfil.get('pretensao_salarial', 'N/A')
            prompt_fit = f\"\"\"[/fit_perfil]

**VAGA:**
{prompt}

**CARGO-ALVO:** {cargo}

Etapa 1: Estimativa Salarial da Vaga vs R$ {pretensao}
Etapa 2: Score de Match (0-100%), Pontos de Atenção, Edições no CV
Etapa 3: Veredito Final (APLICAR / NÃO APLICAR)

Use o CV do contexto. NÃO mostre o CV.\"\"\"
            st.session_state.mensagens[-1]["content"] = prompt_fit
            st.session_state.aguardando_vaga = False

        with st.chat_message("assistant"):
            with st.spinner("🤔 Analisando..."):
                resp = chamar_gpt(st.session_state.openai_client, st.session_state.mensagens)
                if resp:
                    st.markdown(resp)
                    st.session_state.mensagens.append({"role": "assistant", "content": resp})
""",
    "ui/screens/__init__.py": "",
    "ui/screens/fase0_intro.py": """import os
import streamlit as st
from core.utils import inicializar_cliente_openai

def fase_0_intro():
    st.markdown("# 🎯 Protocolo Nóbile")
    st.markdown("## Sistema de Inteligência de Carreira Executiva")
    st.markdown("---")

    st.markdown(\"\"\"
### Bem-vindo. Eu sou a Inteligência Artificial do **Protocolo Nóbile**.

Minha função é realizar uma **auditoria completa da sua carreira** e reposicionar seu perfil para o mercado Executivo de Alta Performance, eliminando ruídos e focando em **ROI**.

### O que eu faço por você:

✅ **Otimização de CV e LinkedIn para ATS**  
✅ **SEO de Perfis Profissionais**  
✅ **Análise Estratégica de Carreira**  
✅ **Preparação Tática para Entrevistas**  

### Como Funciona:

**1️⃣ Deep Scan:** Análise completa do CV  
**2️⃣ Briefing:** Seus objetivos (cargo, salário, local)  
**3️⃣ Reality Check:** Cruzamento com mercado  
**4️⃣ Otimização:** Reescrita com dados quantitativos  
**5️⃣ Estratégia:** Empresas, vagas e entrevistas  

---

### 🚀 Requisitos:

- ✅ CV em formato PDF
- ✅ 20-30 minutos disponíveis
- ✅ Dados sobre suas experiências
    \"\"\")

    st.markdown("---")

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        if not st.session_state.openai_client:
            st.session_state.openai_client = inicializar_cliente_openai(api_key)
        st.success("✅ Sistema configurado e pronto!")
    else:
        st.warning("⚠️ Configure sua API Key no arquivo config.py")
        key_input = st.text_input("Ou insira manualmente:", type="password")
        if key_input:
            st.session_state.openai_client = inicializar_cliente_openai(key_input)
            st.success("✅ API Key configurada!")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INICIAR DIAGNÓSTICO", use_container_width=True, type="primary"):
            if st.session_state.openai_client:
                st.session_state.fase = 'FASE_0_UPLOAD'
                st.rerun()
            else:
                st.error("⚠️ Configure a API Key primeiro!")
""",
    "ui/screens/fase0_upload.py": """import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import extrair_texto_pdf, chamar_gpt

def fase_0_upload():
    st.markdown("# 📄 Envie seu Currículo")
    st.markdown("---")
    st.info("📌 Para iniciar o Diagnóstico, **anexe seu CV em PDF** abaixo.")

    arquivo = st.file_uploader("📄 Seu currículo em PDF", type=['pdf'])

    if arquivo:
        with st.spinner("🔍 Varredura Integral (Deep Scan)... Lendo 100% do conteúdo..."):
            texto = extrair_texto_pdf(arquivo)
            if texto:
                st.session_state.cv_texto = texto
                msgs = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f\"\"\"Faça a VARREDURA INTEGRAL deste CV.

Leia 100% do conteúdo. Identifique Senioridade Real, Stack Técnico, Resultados Escondidos e Gaps.

CV COMPLETO:
{texto}

Forneça relatório executivo completo. NÃO mostre o CV de volta.\"\"\"}
                ]
                analise = chamar_gpt(st.session_state.openai_client, msgs)
                if analise:
                    st.session_state.analise_inicial = analise
                    st.session_state.fase = 'FASE_1_DIAGNOSTICO'
                    st.rerun()
""",
    "ui/screens/fase1_diagnostico.py": """import streamlit as st
from core.utils import scroll_topo

def fase_1_diagnostico():
    scroll_topo()
    st.markdown("# 🔍 Diagnóstico Completo")
    st.markdown("---")
    st.markdown(st.session_state.analise_inicial)
    st.markdown("---")
    st.markdown("**Recebido. Li seu perfil completo. Vamos elevar o nível dessa narrativa.**")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ PROSSEGUIR PARA BRIEFING", use_container_width=True, type="primary"):
            st.session_state.fase = 'FASE_1_BRIEFING'
            st.rerun()
""",
    "ui/screens/fase1_briefing.py": """import streamlit as st
from core.utils import scroll_topo, filtrar_cidades

def fase_1_briefing():
    scroll_topo()
    st.markdown("# 🎯 Briefing Estratégico")
    st.markdown("---")
    st.markdown("**Para traçar a estratégia correta, responda apenas:**")

    with st.form("briefing"):
        col1, col2 = st.columns(2)

        with col1:
            p1 = st.selectbox("**P1. Objetivo Principal:**",
                ["", "Recolocação no Mercado", "Transição de Carreira", "Promoção Interna", "Trabalho Internacional"])
            p2 = st.text_input("**P2. Cargo que você procura:**",
                placeholder="Ex: Gerente de Vendas")

        with col2:
            p3 = st.number_input("**P3. Pretensão Salarial (mensal):**",
                min_value=0, step=1000, format="%d",
                help="Apenas números. Valor mensal em R$")
            p4 = st.text_input("**P4. Localização (Cidade/Remoto):**",
                placeholder="Digite a cidade")

            if p4:
                sugestoes = filtrar_cidades(p4)
                if sugestoes:
                    st.info(f"💡 {', '.join(sugestoes[:5])}")

        remoto = st.checkbox("📍 Aceito trabalho 100% remoto")

        if st.form_submit_button("🚀 EXECUTAR REALITY CHECK", use_container_width=True):
            if p1 and p2 and p3 > 0 and p4:
                st.session_state.mensagens = []
                st.session_state.modulo_ativo = None
                st.session_state.etapa_modulo = None

                st.session_state.perfil = {
                    'objetivo': p1,
                    'cargo_alvo': p2,
                    'pretensao_salarial': f"{p3:,}".replace(",", "."),
                    'localizacao': p4,
                    'remoto': remoto
                }
                st.session_state.fase = 'FASE_15_REALITY'
                st.rerun()
            else:
                st.error("⚠️ Preencha todos os campos (P1 a P4)")
""",
    "ui/screens/fase15_reality.py": """import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt, scroll_topo

def fase_15_reality_check():
    scroll_topo()
    st.markdown("# 🧠 Reality Check - Processando...")
    st.markdown("---")

    with st.spinner("🧠 Cruzando CV × Cargo × Salário × Região..."):
        perfil = st.session_state.perfil
        pretensao = perfil['pretensao_salarial']
        cargo = perfil['cargo_alvo']
        local = perfil['localizacao']

        msgs = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f\"\"\"REALITY CHECK:

P1 Objetivo: {perfil['objetivo']}
P2 Cargo: {cargo}
P3 Pretensão: R$ {pretensao} mensal
P4 Local: {local}
Remoto: {'Sim' if perfil.get('remoto') else 'Não'}

DEEP SCAN:
{st.session_state.analise_inicial}

FORMATO EXATO OBRIGATÓRIO:

🎯 **REALITY CHECK - ANÁLISE ESTRATÉGICA**

**CARGO DESEJADO:** {cargo}

**NOMENCLATURAS SIMILARES NO MERCADO:**
• [Variação 1]
• [Variação 2]
• [Variação 3]

*(Recrutadores usam diferentes nomes para a mesma função)*

---

### 📊 ANÁLISE SALARIAL

**Pretensão Informada:** R$ {pretensao} mensal

**Faixa Salarial Geral:** R$ [mínimo] a R$ [máximo]

**Veredito:** [Abaixo/Na Média/Acima]

[Contexto]

---

### ⚠️ ANÁLISE DE GAP

Para conquistar vaga de **{cargo}**, seu CV precisa demonstrar mais [competência]. Hoje ele passa imagem de [cargo percebido].

1. **[Gap 1]:** [falta]
2. **[Gap 2]:** [falta]
3. **[Gap 3]:** [falta]

---

### 🎯 VEREDITO DO HEADHUNTER

**Nível de Desafio:** [Baixo/Médio/Alto]

**Estratégia:** Focar em [ponto forte] para justificar R$ {pretensao}

---

### ✅ PRÓXIMOS PASSOS

Use os **botões na barra lateral** para continuar:

• 🔧 **Otimizar CV + LinkedIn**
• 🏢 **Empresas Discovery**
• 🎯 **Analisar Vaga**
• 🎤 **Prep. Entrevista**
• 📊 **Análise de Mercado**

NÃO mostre CV.\"\"\"}
        ]

        reality = chamar_gpt(st.session_state.openai_client, msgs)

        if reality:
            st.session_state.mensagens = [
                {"role": "system", "content": SYSTEM_PROMPT + f\"\\n\\nCV DO CANDIDATO (uso interno): {st.session_state.cv_texto}\\n\\nCARGO-ALVO: {cargo}\"},
                {"role": "assistant", "content": reality}
            ]
            st.session_state.fase = 'CHAT'
            st.rerun()
""",
    "modules/__init__.py": "",
    "modules/otimizador/__init__.py": "",
    "modules/otimizador/processor.py": """from modules.otimizador.etapa1_seo import prompt_etapa1
from modules.otimizador.etapa2_interrogatorio import prompt_etapa2
from modules.otimizador.etapa3_curadoria import prompt_etapa3
from modules.otimizador.etapa4_engenharia import prompt_etapa4
from modules.otimizador.etapa5_validacao import prompt_etapa5
from modules.otimizador.etapa6_arquivo import prompt_etapa6
from modules.otimizador.etapa7_exportacao import prompt_etapa7
import streamlit as st

def processar_modulo_otimizador(prompt):
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    etapa = st.session_state.get('etapa_modulo')

    if etapa == 'AGUARDANDO_OK':
        if prompt.lower().strip() in ['ok', 'começar', 'comecar', 'iniciar', 'sim', 'vamos', 'start']:
            st.session_state.etapa_modulo = 'ETAPA_1'
            return prompt_etapa1(cargo)
        return None

    if etapa == 'ETAPA_1':
        if len(prompt) > 10:
            st.session_state.etapa_modulo = 'ETAPA_2'
            return prompt_etapa2()
        return None

    if etapa == 'ETAPA_2':
        if len(prompt) > 30:
            st.session_state.etapa_modulo = 'ETAPA_3'
            return prompt_etapa3()
        return None

    if etapa == 'ETAPA_3':
        if len(prompt) > 20:
            st.session_state.etapa_modulo = 'ETAPA_4'
            return prompt_etapa4()
        return None

    if etapa == 'ETAPA_4':
        st.session_state.etapa_modulo = 'ETAPA_5'
        return prompt_etapa5()

    if etapa == 'ETAPA_5':
        if any(word in prompt.lower() for word in ['ok', 'aprovado', 'aprovei', 'sim', 'perfeito', 'ótimo', 'otimo']):
            st.session_state.etapa_modulo = 'ETAPA_6'
            return prompt_etapa6(cargo)
        return None

    if etapa == 'ETAPA_6':
        st.session_state.etapa_modulo = 'ETAPA_7'
        st.session_state.modulo_ativo = None
        return prompt_etapa7()

    return None
""",
    "modules/otimizador/etapa1_seo.py": """def prompt_etapa1(cargo):
    return f\"\"\"Inicie a ETAPA 1 do otimizador de CV.

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

NÃO mostre o CV completo.\"\"\"
""",
    "modules/otimizador/etapa2_interrogatorio.py": """def prompt_etapa2():
    return \"\"\"Ótimo! Recebi suas respostas sobre as keywords. Avançando para ETAPA 2.

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

NÃO mostre o CV completo.\"\"\"
""",
    "modules/otimizador/etapa3_curadoria.py": """def prompt_etapa3():
    return \"\"\"Excelente! Recebi os dados brutos. Avançando para ETAPA 3.

### 💡 ETAPA 3: CURADORIA ESTRATÉGICA

"Além dos números que você acabou de passar, preciso de mais 3 informações:"

**1. PROJETO DIVISOR DE ÁGUAS:**
Existe algum projeto ou iniciativa que você liderou que foi um "game changer" na empresa mas NÃO está explícito no CV? Qual foi o impacto real?

**2. DIFERENCIAL COMPETITIVO:**
O que te diferencia de OUTROS candidatos ao mesmo cargo? Qual sua "arma secreta"?

**3. SOFT SKILL CRÍTICA:**
Qual habilidade de liderança é ESSENCIAL para o cargo e você domina mas não evidenciou no CV?

---

⏸️ **AGUARDO SUAS RESPOSTAS.**

Após receber, farei a Avaliação do Headhunter:
- ✅ Se relevante para o cargo → "INCLUIREMOS estrategicamente"
- ⚠️ Se for ruído → "Sugiro descartar, desvia o foco"
\"\"\"
""",
    "modules/otimizador/etapa4_engenharia.py": """def prompt_etapa4():
    return \"\"\"Perfeito! Com TODOS os dados das Etapas 1, 2 e 3, vou agora reescrever.

### ✍️ ETAPA 4: ENGENHARIA DE TEXTO

Primeiro, avalie cada item da Etapa 3:
- Se relevante → ✅ "INCLUIREMOS isso"
- Se ruído → ⚠️ "Sugiro descartar"

Depois, reescreva seguindo RIGOROSAMENTE estas estruturas:

**A) ESTRUTURA DO RESUMO (LINKEDIN "SOBRE"):**

> **Parágrafo 1 (Hook):** [Identidade Profissional] + [Anos XP] + [Proposta Única de Valor]
> **Parágrafo 2 (Autoridade):** [Core Skills] aplicadas a [Mercado/Nicho]
> **Destaques de Impacto:**
> 🚀 **[CONQUISTA MACRO]:** Contexto + Ação + Resultado Numérico
> 📈 **[LIDERANÇA]:** Tamanho do time + Escopo + Resultado de Gestão
> **Tech Stack & Idiomas:** [Lista Otimizada para ATS]

---

**B) ESTRUTURA DE EXPERIÊNCIA (CV & LINKEDIN):**

Para CADA cargo, use esta estrutura com os dados da Etapa 2:

> **[Nome do Cargo]** | [Empresa] | [Datas]
> *Resumo Estratégico:* [Uma linha definindo escopo principal]
> • **[COMPETÊNCIA CHAVE 1]:** Verbo Forte + Contexto + **Resultado Numérico (Obrigatório)**
> • **[COMPETÊNCIA CHAVE 2]:** Verbo Forte + Ferramenta + **Resultado Numérico (Obrigatório)**
> • **[PROJETO ESPECÍFICO]:** Nome + Problema + Solução + **Ganho Financeiro/Tempo**
> **Competências:** [5-8 Hard Skills desta função]

---

Reescreva TODAS as experiências com dados reais da Etapa 2.

Após reescrever tudo, apresente e pergunte: "O texto está robusto e alinhado? Quer ajustar algo?" (ETAPA 5)\"\"\"
""",
    "modules/otimizador/etapa5_validacao.py": """def prompt_etapa5():
    return \"\"\"### ✅ ETAPA 5: VALIDAÇÃO FINAL

"O texto acima está robusto e alinhado? Quer ajustar algo?"

Revise:
- Os números estão corretos?
- As conquistas refletem a realidade?
- As keywords do cargo estão presentes?

---

**Digite:**
- **"OK"** ou **"APROVADO"** para gerar o Arquivo Mestre (ETAPA 6)
- Ou descreva os ajustes necessários

⏸️ **AGUARDO SEU FEEDBACK.**\"\"\"
""",
    "modules/otimizador/etapa6_arquivo.py": """def prompt_etapa6(cargo):
    return f\"\"\"### 📦 ETAPA 6: ARQUIVO MESTRE (Compilação Final)

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

Após gerar o arquivo completo, avance para ETAPA 7.\"\"\"
""",
    "modules/otimizador/etapa7_exportacao.py": """def prompt_etapa7():
    return \"\"\"### 📤 ETAPA 7: INSTRUÇÕES DE EXPORTAÇÃO

**PARA FLOWCV (Recomendado):**
1. Copie a **SEÇÃO 2** completa acima
2. Salve num arquivo .txt ou Word
3. Vá em **flowcv.com** > "New Resume" > "Import Resume"
4. Faça o upload - preenche automaticamente!
5. Escolha um template e exporte em PDF

---

**PARA LINKEDIN:**
1. Atualize a **Headline** com a da SEÇÃO 1
2. Copie o **SUMMARY** para a seção "Sobre"
3. Atualize cada experiência com os textos da SEÇÃO 2
4. Adicione as **Top Skills** da SEÇÃO 1

---

**PARA WORD/GOOGLE DOCS:**
1. Copie a SEÇÃO 2 inteira
2. Formate com fonte profissional (Calibri/Arial)
3. Exporte como PDF

---

### 💡 PRÓXIMOS PASSOS:

• 🏢 **Empresas** - Descubra onde aplicar
• 🎯 **Analisar Vaga** - Calcule fit com vagas
• 🎤 **Prep. Entrevista** - Simulações e dossiê
• 📊 **Análise de Mercado** - Tendências salariais

---

✅ **OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!**\"\"\"
"""
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    for path, content in FILES.items():
        write_file(path, content)
    print("✅ Estrutura criada com sucesso.")

if __name__ == "__main__":
    main()