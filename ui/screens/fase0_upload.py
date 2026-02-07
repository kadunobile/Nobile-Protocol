import streamlit as st
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
                    {"role": "user", "content": f"""Faça a VARREDURA INTEGRAL deste CV.

Leia 100% do conteúdo. Identifique Senioridade Real, Stack Técnico, Resultados Escondidos e Gaps.

CV COMPLETO:
{texto}

Forneça relatório executivo completo. NÃO mostre o CV de volta."""}
                ]
                analise = chamar_gpt(st.session_state.openai_client, msgs)
                if analise:
                    st.session_state.analise_inicial = analise
                    st.session_state.fase = 'FASE_1_DIAGNOSTICO'
                    st.rerun()
