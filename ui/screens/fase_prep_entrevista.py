import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt
import json

def fase_prep_entrevista():
    st.markdown("# 🎤 Preparação para Entrevista")
    st.markdown("---")
    
    st.info("🎯 Prepare-se com perguntas personalizadas baseadas no seu perfil e na vaga")
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV não encontrado. Faça upload primeiro.")
        return
    
    # Selecionar tipo de entrevista
    tipo_entrevista = st.selectbox(
        "**Tipo de Entrevista:**",
        [
            "Entrevista Inicial com RH",
            "Entrevista Técnica",
            "Entrevista com Gestor",
            "Painel com Múltiplos Entrevistadores",
            "Case de Negócio"
        ]
    )
    
    cargo = st.session_state.perfil.get('cargo_alvo', 'Cargo não definido')
    
    if st.button("🎯 Gerar Perguntas Personalizadas", use_container_width=True, type="primary"):
        with st.spinner("🧠 Analisando seu perfil e gerando perguntas..."):
            prompt_perguntas = f"""
Você é um especialista em preparação para entrevistas executivas.

**CONTEXTO:**
- Candidato com CV abaixo
- Cargo-alvo: {cargo}
- Tipo de entrevista: {tipo_entrevista}

**CV RESUMIDO:**
{st.session_state.cv_texto[:2000]}

**ANÁLISE DO CV (se disponível):**
{st.session_state.get('analise_inicial', 'Não disponível')[:1000]}

**TAREFA:**
Gere 10 perguntas que o candidato PROVAVELMENTE receberá nesta entrevista.

**CRITÉRIOS:**
1. Baseie-se em GAPS e PONTOS FORTES do CV
2. Inclua perguntas sobre experiências específicas mencionadas no CV
3. Inclua perguntas comportamentais (método STAR)
4. Inclua perguntas técnicas relevantes ao cargo
5. Para cada pergunta, forneça:
   - A pergunta
   - Por que ela pode ser feita (contexto)
   - Sugestão de estrutura de resposta (tópicos, não resposta pronta)

**FORMATO JSON:**
```json
{{
  "perguntas": [
    {{
      "numero": 1,
      "pergunta": "...",
      "contexto": "Por que perguntam isso: ...",
      "dicas_resposta": [
        "Mencione experiência X do seu CV",
        "Enfatize resultado Y",
        "Conecte com requisito Z da vaga"
      ],
      "tipo": "Comportamental/Técnica/Situacional"
    }}
  ]
}}
```

RETORNE APENAS O JSON, SEM MARKDOWN.
"""
            
            msgs = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_perguntas}
            ]
            
            resposta = chamar_gpt(st.session_state.openai_client, msgs)
            
            if resposta:
                try:
                    # Extrai JSON da resposta
                    json_start = resposta.find('{')
                    json_end = resposta.rfind('}') + 1
                    json_str = resposta[json_start:json_end]
                    
                    perguntas_data = json.loads(json_str)
                    
                    st.success(f"✅ {len(perguntas_data['perguntas'])} perguntas geradas!")
                    st.markdown("---")
                    
                    # Exibe cada pergunta em um expander
                    for p in perguntas_data['perguntas']:
                        with st.expander(f"❓ Pergunta {p['numero']}: {p['tipo']}", expanded=False):
                            st.markdown(f"### {p['pergunta']}")
                            
                            st.markdown(f"**💡 Por que perguntam isso:**")
                            st.info(p['contexto'])
                            
                            st.markdown(f"**📝 Como estruturar sua resposta:**")
                            for dica in p['dicas_resposta']:
                                st.markdown(f"- {dica}")
                            
                            # Campo para o candidato escrever resposta
                            st.markdown("**✍️ Rascunhe sua resposta (opcional):**")
                            st.text_area(
                                "Sua resposta:",
                                placeholder="Use o método STAR: Situação, Tarefa, Ação, Resultado",
                                height=150,
                                key=f"resposta_{p['numero']}"
                            )
                    
                    # Botão para baixar todas as perguntas
                    st.markdown("---")
                    texto_completo = "\n\n".join([
                        f"PERGUNTA {p['numero']}: {p['pergunta']}\n\n"
                        f"Contexto: {p['contexto']}\n\n"
                        f"Dicas de resposta:\n" + "\n".join([f"- {d}" for d in p['dicas_resposta']])
                        for p in perguntas_data['perguntas']
                    ])
                    
                    st.download_button(
                        "📥 Baixar Todas as Perguntas",
                        data=texto_completo,
                        file_name=f"prep_entrevista_{cargo.replace(' ', '_').lower()}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                except json.JSONDecodeError:
                    st.error("❌ Erro ao processar resposta. Tente novamente.")
                    st.code(resposta)
    
    st.markdown("---")
    
    # Dicas gerais
    with st.expander("💡 Dicas Gerais para Entrevistas"):
        st.markdown("""
### 📋 Antes da Entrevista
- ✅ Pesquise a empresa (site, LinkedIn, notícias recentes)
- ✅ Releia a descrição da vaga e seu CV
- ✅ Prepare 3-5 perguntas para fazer ao entrevistador
- ✅ Teste sua câmera/microfone (se virtual)
- ✅ Vista-se adequadamente

### 🎯 Durante a Entrevista
- ✅ Use o método STAR (Situação, Tarefa, Ação, Resultado)
- ✅ Seja específico: números, datas, empresas reais
- ✅ Mostre entusiasmo genuíno
- ✅ Faça perguntas inteligentes ao final
- ✅ Anote pontos importantes

### 📧 Depois da Entrevista
- ✅ Envie email de agradecimento em até 24h
- ✅ Reforce seu interesse na vaga
- ✅ Mencione algo específico da conversa
        """)
    
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
