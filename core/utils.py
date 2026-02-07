import re
import streamlit as st
import PyPDF2
import streamlit.components.v1 as components
from openai import OpenAI
from core.data import CIDADES_BRASIL

def corrigir_formatacao(texto):
    if not texto:
        return texto

    # Remove qualquer prefixo de moeda (R$ ou R)
    texto = re.sub(r'\bR\$\s*', '', texto)
    texto = re.sub(r'\bR\s+', '', texto)

    # Mantém quebras de linha (não usar \s aqui)
    texto = re.sub(r'[ \t]{2,}', ' ', texto)

    # Normaliza quebras do Windows
    texto = texto.replace('\r\n', '\n')

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
    components.html("""
        <script>
            const scrollToTop = () => {
                const main = window.parent.document.querySelector('section.main');
                if (main) main.scrollTop = 0;
                window.parent.scrollTo(0, 0);
                document.documentElement.scrollTop = 0;
                document.body.scrollTop = 0;
            };
            scrollToTop();
            setTimeout(scrollToTop, 50);
            setTimeout(scrollToTop, 150);
            setTimeout(scrollToTop, 400);
        </script>
    """, height=0)

def filtrar_cidades(texto):
    if not texto:
        return CIDADES_BRASIL[:10]
    return [c for c in CIDADES_BRASIL if texto.lower() in c.lower()]

def forcar_topo():
    components.html("""
        <script>
            const goTop = () => {
                const main = window.parent.document.querySelector('section.main');
                if (main) main.scrollTop = 0;
                window.parent.scrollTo(0, 0);
                document.documentElement.scrollTop = 0;
                document.body.scrollTop = 0;
            };

            const blurInputs = () => {
                const inputs = window.parent.document.querySelectorAll('textarea, input');
                inputs.forEach(i => i.blur());
            };

            goTop();
            blurInputs();

            setTimeout(() => { goTop(); blurInputs(); }, 50);
            setTimeout(() => { goTop(); blurInputs(); }, 150);
            setTimeout(() => { goTop(); blurInputs(); }, 400);
        </script>
    """, height=0)