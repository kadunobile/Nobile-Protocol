import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import extrair_texto_universal, chamar_gpt

def fase_0_upload():
    st.markdown("# 📄 Envie seu Currículo")
    st.markdown("---")
    st.info("📌 Para iniciar o Diagnóstico, **anexe seu CV** abaixo.")
    
    st.markdown("""
    **Formatos aceitos:**
    - 📕 PDF (.pdf)
    - 📘 Word (.docx) - recomendado
    - 📝 Texto (.txt)
    
    *Nota: Arquivos .doc antigos devem ser convertidos para .docx*
    """)

    arquivo = st.file_uploader(
        "📄 Seu currículo", 
        type=['pdf', 'docx', 'doc', 'txt'],
        help="Arraste seu arquivo ou clique para selecionar"
    )

    if arquivo:
        # Detecta tipo de arquivo
        tipo_arquivo = arquivo.name.split('.')[-1].lower()
        
        # Mensagem customizada por tipo
        mensagens_spinner = {
            'pdf': '🔍 Varredura Integral de PDF... Lendo 100% do conteúdo...',
            'docx': '📘 Processando Word... Extraindo texto e tabelas...',
            'doc': '📘 Processando Word... Extraindo texto e tabelas...',
            'txt': '📝 Lendo arquivo de texto...'
        }
        
        with st.spinner(mensagens_spinner.get(tipo_arquivo, '🔍 Processando arquivo...')):
            texto = extrair_texto_universal(arquivo, tipo_arquivo)
            
            if texto:
                st.session_state.cv_texto = texto
                
                # Mostrar preview
                with st.expander("👁️ Preview do texto extraído (primeiras 500 caracteres)"):
                    st.text(texto[:500] + "...")
                
                msgs = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"""Faça a VARREDURA INTEGRAL deste CV.

Leia 100% do conteúdo. Identifique Senioridade Real, Stack Técnico, Resultados Escondidos e Gaps.

CV COMPLETO:
{texto}

Forneça relatório executivo completo. NÃO mostre o CV de volta."""}
                ]
                
                with st.spinner("🧠 Analisando perfil com IA..."):
                    analise = chamar_gpt(
                        st.session_state.openai_client, 
                        msgs,
                        temperature=0.3,  # Consistência na análise inicial
                        seed=42           # Determinístico
                    )
                    
                if analise:
                    st.success(f"✅ CV {tipo_arquivo.upper()} processado com sucesso!")
                    st.session_state.analise_inicial = analise
                    st.session_state.fase = 'FASE_1_DIAGNOSTICO'
                    st.rerun()
