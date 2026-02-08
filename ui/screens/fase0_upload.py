import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import extrair_texto_universal, chamar_gpt


def validar_pdf_linkedin(texto: str) -> dict:
    """
    Validação básica para verificar se o PDF veio do LinkedIn.
    
    Checa padrões típicos do PDF exportado do LinkedIn:
    - Presença de seções conhecidas (Experience, Education, Skills, etc.)
    - Menção a "linkedin" no texto
    - Estrutura de cabeçalho com nome + headline
    
    Returns:
        dict com 'valido' (bool) e 'motivo' (str)
    """
    texto_lower = texto.lower()
    
    # Seções típicas do PDF LinkedIn (PT e EN)
    secoes_linkedin = [
        'experience', 'experiência',
        'education', 'educação', 'formação',
        'skills', 'competências', 'habilidades',
        'languages', 'idiomas',
        'certifications', 'certificações',
        'summary', 'resumo', 'sobre',
    ]
    
    # Contar quantas seções do LinkedIn foram encontradas
    secoes_encontradas = sum(1 for s in secoes_linkedin if s in texto_lower)
    
    # Checar menção ao LinkedIn
    tem_linkedin = 'linkedin' in texto_lower
    
    # Checar se tem estrutura mínima (pelo menos 3 seções típicas)
    tem_estrutura = secoes_encontradas >= 3
    
    # Checar se não é CV genérico/Word (padrões que NÃO são LinkedIn)
    sinais_nao_linkedin = [
        'objetivo profissional',  # CVs BR tradicionais
        'dados pessoais',         # CVs BR tradicionais
        'pretensão salarial',     # CVs BR tradicionais
        'estado civil',           # CVs BR tradicionais
    ]
    tem_sinais_generico = sum(1 for s in sinais_nao_linkedin if s in texto_lower) >= 2
    
    if tem_sinais_generico:
        return {
            'valido': False,
            'motivo': 'Este PDF parece ser um CV tradicional, não o exportado do LinkedIn. '
                      'Por favor, exporte seu perfil diretamente do LinkedIn seguindo o passo a passo acima.'
        }
    
    if tem_linkedin or tem_estrutura:
        return {'valido': True, 'motivo': ''}
    
    # Caso ambíguo - aceitar mas avisar
    if secoes_encontradas >= 2:
        return {
            'valido': True,
            'motivo': 'aviso'  # Flag para mostrar aviso suave
        }
    
    return {
        'valido': False,
        'motivo': 'Não foi possível identificar este PDF como exportação do LinkedIn. '
                  'Certifique-se de seguir o passo a passo acima para exportar corretamente.'
    }


def fase_0_upload():
    st.markdown("# 📄 Envie seu Perfil do LinkedIn")
    st.markdown("---")
    
    st.info("📌 Para iniciar o Diagnóstico, precisamos do **PDF exportado do seu LinkedIn.**")
    
    # ─── Passo a passo visual ───
    st.markdown("### 📋 Como exportar seu perfil do LinkedIn:")
    
    st.markdown("""
    <div style="background: rgba(233, 69, 96, 0.08); border-left: 4px solid #e94560; 
                padding: 1.2rem; border-radius: 0 8px 8px 0; margin: 1rem 0;">
        <p style="margin: 0.4rem 0;"><strong>1.</strong> Abra seu perfil no <strong>LinkedIn</strong> (pelo computador é mais fácil)</p>
        <p style="margin: 0.4rem 0;"><strong>2.</strong> Clique no botão <strong>"Mais / More"</strong> (abaixo da foto)</p>
        <p style="margin: 0.4rem 0;"><strong>3.</strong> Selecione <strong>"Salvar como PDF / Save to PDF"</strong></p>
        <p style="margin: 0.4rem 0;"><strong>4.</strong> O LinkedIn vai gerar o PDF — <strong>faça o download</strong></p>
        <p style="margin: 0.4rem 0;"><strong>5.</strong> Envie esse arquivo aqui embaixo 👇</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    st.warning(
        "⚠️ **Importante:** Aceitamos **somente o PDF exportado do LinkedIn.** "
        "CVs feitos no Word, Canva ou outros modelos não funcionam corretamente "
        "para otimização ATS."
    )
    
    st.markdown("---")
    
    # ─── Upload (somente PDF) ───
    arquivo = st.file_uploader(
        "📄 PDF do LinkedIn",
        type=['pdf'],
        help="Apenas o PDF exportado diretamente do LinkedIn"
    )
    
    if arquivo:
        # Verificar se já processou este arquivo
        if (not st.session_state.get('cv_texto_temp') 
                or st.session_state.get('cv_arquivo_nome') != arquivo.name):
            
            with st.spinner('🔍 Lendo seu perfil do LinkedIn...'):
                texto = extrair_texto_universal(arquivo, 'pdf')
                
                if texto:
                    st.session_state.cv_texto_temp = texto
                    st.session_state.cv_arquivo_nome = arquivo.name
                    st.rerun()
        
        # Mostrar resultado após processamento
        if st.session_state.get('cv_texto_temp'):
            texto = st.session_state.cv_texto_temp
            
            # ─── Validação LinkedIn ───
            resultado = validar_pdf_linkedin(texto)
            
            if not resultado['valido']:
                st.error(f"❌ {resultado['motivo']}")
                
                if st.button("🔄 Tentar outro arquivo", use_container_width=True):
                    del st.session_state.cv_texto_temp
                    del st.session_state.cv_arquivo_nome
                    st.rerun()
                return
            
            # Aviso suave para caso ambíguo
            if resultado.get('motivo') == 'aviso':
                st.warning(
                    "⚠️ Não temos 100% de certeza que este é o PDF do LinkedIn. "
                    "Se não for, os resultados podem não ser ideais."
                )
            
            st.success("✅ Perfil do LinkedIn carregado com sucesso!")
            
            st.markdown("---")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button("🚀 Continuar com este Perfil", type="primary", use_container_width=True):
                    # Confirmar e salvar CV
                    st.session_state.cv_texto = texto
                    st.session_state.cv_upload_confirmed = True
                    st.session_state.cv_fonte = 'linkedin_pdf'
                    
                    # Limpar estado temporário
                    if 'cv_texto_temp' in st.session_state:
                        del st.session_state.cv_texto_temp
                    if 'cv_arquivo_nome' in st.session_state:
                        del st.session_state.cv_arquivo_nome
                    
                    # Análise inicial com IA
                    msgs = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"""Faça a VARREDURA INTEGRAL deste perfil LinkedIn exportado em PDF.

Leia 100% do conteúdo. Identifique Senioridade Real, Stack Técnico, Resultados Escondidos e Gaps.

PERFIL LINKEDIN COMPLETO:
{texto}

Forneça relatório executivo completo. NÃO mostre o perfil de volta."""}
                    ]
                    
                    with st.spinner("🧠 Analisando seu perfil com IA..."):
                        analise = chamar_gpt(
                            st.session_state.openai_client,
                            msgs,
                            temperature=0.3,
                            seed=42
                        )
                    
                    if analise:
                        st.session_state.analise_inicial = analise
                        st.session_state.fase = 'FASE_1_DIAGNOSTICO'
                        st.rerun()
                    else:
                        st.error(
                            "❌ Não foi possível analisar o perfil. "
                            "Verifique sua conexão e tente novamente."
                        )
            
            with col2:
                if st.button("🔄 Trocar arquivo", use_container_width=True):
                    del st.session_state.cv_texto_temp
                    del st.session_state.cv_arquivo_nome
                    st.rerun()
    
    # ─── Botão de voltar ───
    st.markdown("---")
    if st.button("⬅️ Voltar", use_container_width=True):
        st.session_state.fase = 'FASE_0_INTRO'
        st.rerun()
