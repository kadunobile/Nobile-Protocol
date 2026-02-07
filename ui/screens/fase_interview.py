import streamlit as st
import json
import re
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt

def fase_prep_entrevista():
    st.markdown("# 🎤 Preparação para Entrevista")
    st.markdown("---")
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV não encontrado. Faça upload primeiro.")
        return
    
    perfil = st.session_state.perfil or {}
    cargo = perfil.get('cargo_alvo', 'cargo desejado')
    
    st.info(f"🎯 Preparação focada para: **{cargo}**")
    
    # Seleção de tipo de entrevista
    st.markdown("### 🎭 Tipo de Entrevista")
    
    tipo_entrevista = st.selectbox(
        "Escolha o tipo de entrevista para se preparar:",
        [
            "Entrevista Inicial com RH",
            "Entrevista Técnica",
            "Entrevista com Gestor",
            "Painel com Múltiplos Entrevistadores",
            "Case de Negócio"
        ],
        help="Selecione o formato da entrevista para receber perguntas personalizadas"
    )
    
    # Descrição da vaga (opcional)
    descricao_vaga = st.text_area(
        "Descrição da Vaga (opcional)",
        height=100,
        placeholder="Cole aqui a descrição da vaga para perguntas mais específicas..."
    )
    
    if st.button("🎯 Gerar Perguntas Personalizadas", type="primary", use_container_width=True):
        with st.spinner("🤔 Gerando perguntas baseadas no seu perfil..."):
            # Prompt para GPT gerar 10 perguntas em JSON
            prompt = f"""Você é um especialista em recrutamento e seleção. 

Gere exatamente 10 perguntas personalizadas para uma **{tipo_entrevista}** para o cargo de **{cargo}**.

**CV DO CANDIDATO (para personalização):**
{st.session_state.cv_texto[:3000]}

**DESCRIÇÃO DA VAGA:**
{descricao_vaga if descricao_vaga else 'Não informada - use perguntas gerais para o cargo'}

**INSTRUÇÕES:**
1. Crie 10 perguntas ESPECÍFICAS baseadas no CV e tipo de entrevista
2. Cada pergunta deve ter contexto explicativo
3. Forneça dicas práticas de resposta conectadas ao CV
4. Identifique o tipo de cada pergunta

**RETORNE APENAS UM JSON VÁLIDO neste formato:**

{{
  "perguntas": [
    {{
      "numero": 1,
      "pergunta": "Texto da pergunta aqui",
      "contexto": "Por que perguntam isso: explicação breve",
      "dicas_resposta": [
        "Mencione experiência X do seu CV",
        "Enfatize resultado Y",
        "Conecte com requisito Z da vaga"
      ],
      "tipo": "Comportamental"
    }}
  ]
}}

**TIPOS VÁLIDOS:** Comportamental, Técnica, Situacional

**IMPORTANTE:** Retorne APENAS o JSON, sem texto adicional antes ou depois."""

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            resposta = chamar_gpt(st.session_state.openai_client, messages)
            
            if resposta:
                try:
                    # Parse do JSON - usa regex para encontrar JSON completo
                    json_pattern = r'\{[\s\S]*"perguntas"[\s\S]*\[[\s\S]*\][\s\S]*\}'
                    json_match = re.search(json_pattern, resposta)
                    
                    if not json_match:
                        st.error("❌ Erro ao gerar perguntas. Tente novamente.")
                        return
                    
                    json_str = json_match.group(0)
                    perguntas_data = json.loads(json_str)
                    
                    # Armazena no session_state
                    st.session_state.perguntas_entrevista = perguntas_data['perguntas']
                    st.success(f"✅ {len(st.session_state.perguntas_entrevista)} perguntas geradas com sucesso!")
                    st.rerun()
                    
                except json.JSONDecodeError as e:
                    st.error(f"❌ Erro ao processar resposta. Tente novamente.")
                    st.caption(f"Detalhes técnicos: {str(e)}")
                except KeyError:
                    st.error("❌ Formato de resposta inválido. Tente novamente.")
    
    # Exibição das perguntas
    if 'perguntas_entrevista' in st.session_state and st.session_state.perguntas_entrevista:
        st.markdown("---")
        st.markdown("## 📝 Suas Perguntas de Entrevista")
        
        perguntas = st.session_state.perguntas_entrevista
        
        # Botão de download
        texto_download = f"PERGUNTAS DE ENTREVISTA - {tipo_entrevista}\n"
        texto_download += f"Cargo: {cargo}\n"
        texto_download += "=" * 80 + "\n\n"
        
        for p in perguntas:
            texto_download += f"PERGUNTA {p['numero']}: {p['pergunta']}\n\n"
            texto_download += f"Por que perguntam: {p['contexto']}\n\n"
            texto_download += "Dicas para responder:\n"
            for dica in p['dicas_resposta']:
                texto_download += f"  - {dica}\n"
            texto_download += f"\nTipo: {p['tipo']}\n"
            texto_download += "\n" + "-" * 80 + "\n\n"
        
        st.download_button(
            "📥 Baixar Todas as Perguntas (TXT)",
            texto_download,
            file_name=f"perguntas_entrevista_{cargo.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Exibe cada pergunta em expander
        for p in perguntas:
            tipo_emoji = {
                'Comportamental': '🗣️',
                'Técnica': '⚙️',
                'Situacional': '🎯'
            }.get(p.get('tipo', 'Comportamental'), '❓')
            
            with st.expander(f"{tipo_emoji} **Pergunta {p['numero']}:** {p['pergunta']}", expanded=False):
                st.markdown(f"**💡 Por que perguntam isso:**")
                st.info(p['contexto'])
                
                st.markdown(f"**✅ Dicas para sua resposta:**")
                for i, dica in enumerate(p['dicas_resposta'], 1):
                    st.markdown(f"{i}. {dica}")
                
                st.markdown(f"**🏷️ Tipo:** {p.get('tipo', 'N/A')}")
                
                st.markdown("---")
                st.markdown("**✍️ Rascunho da sua resposta (opcional):**")
                st.text_area(
                    "Escreva aqui seu rascunho de resposta:",
                    height=150,
                    key=f"resposta_{p['numero']}",
                    placeholder="Use o método STAR: Situação, Tarefa, Ação, Resultado..."
                )
        
        # Dicas gerais
        st.markdown("---")
        with st.expander("💡 **Dicas Gerais de Entrevista**", expanded=False):
            st.markdown("""
            ### ✅ Antes da Entrevista
            
            - [ ] Pesquise a empresa (site, LinkedIn, notícias recentes)
            - [ ] Revise a descrição da vaga e seus requisitos-chave
            - [ ] Prepare 3-5 perguntas inteligentes para fazer ao final
            - [ ] Tenha exemplos STAR prontos para suas principais competências
            - [ ] Teste câmera, áudio e internet se for remoto
            - [ ] Vista-se adequadamente para a cultura da empresa
            
            ### 💬 Durante a Entrevista
            
            - **Método STAR:** Use Situação → Tarefa → Ação → Resultado
            - **Seja específico:** Números e exemplos concretos > Adjetivos genéricos
            - **Escute ativamente:** Entenda a pergunta antes de responder
            - **Faça perguntas:** Demonstra interesse genuíno
            - **Linguagem corporal:** Contato visual, postura confiante
            - **Anote pontos-chave:** Mostra organização e atenção
            
            ### 🚫 Evite
            
            - ❌ Falar mal de empregadores anteriores
            - ❌ Divagar sem estrutura clara
            - ❌ Mentir sobre experiências (facilmente verificável)
            - ❌ Responder "não sei" sem tentar
            - ❌ Não fazer perguntas no final
            - ❌ Chegar atrasado ou muito cedo (ideal: 5-10min antes)
            
            ### 📞 Após a Entrevista
            
            - ✉️ Envie email de agradecimento em 24h
            - 🎯 Reforce 1-2 pontos-chave que discutiu
            - 💼 Reitere seu interesse na posição
            - 📝 Faça anotações sobre a entrevista (perguntas, pontos fortes/fracos)
            """)
        
        # Botão para gerar novas perguntas
        st.markdown("---")
        if st.button("🔄 Gerar Novas Perguntas", use_container_width=True):
            if 'perguntas_entrevista' in st.session_state:
                del st.session_state.perguntas_entrevista
            st.rerun()
    
    st.markdown("---")
    
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
