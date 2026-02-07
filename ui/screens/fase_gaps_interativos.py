import streamlit as st
from core.utils import scroll_topo


def fase_gaps_interativos():
    """
    Tela interativa para o usuário responder sobre gaps identificados.
    Permite que o usuário:
    - Descreva experiências que tem mas não mencionou no CV
    - Marque skills que realmente não possui
    - Veja o impacto de cada gap
    """
    scroll_topo()
    
    st.markdown("# 🎯 Gaps Identificados no Seu CV")
    st.markdown("---")
    
    st.info("""
    💡 **Responda sobre cada skill/experiência abaixo.**
    
    Suas respostas serão usadas para otimizar seu CV de forma precisa.
    Seja honesto - não invente experiências que não tem!
    """)
    
    # Validar dados necessários
    if 'gaps_identificados' not in st.session_state or not st.session_state.gaps_identificados:
        st.warning("⚠️ Nenhum gap identificado. Redirecionando...")
        st.session_state.fase = 'CHAT'
        st.rerun()
        return
    
    gaps = st.session_state.gaps_identificados
    
    # Inicializar respostas se não existir
    if 'gaps_respondidos' not in st.session_state:
        st.session_state.gaps_respondidos = {}
    
    st.markdown(f"### 📊 {len(gaps)} gaps encontrados")
    st.markdown("---")
    
    # Renderizar cada gap em expander
    for idx, gap in enumerate(gaps):
        # Primeiro gap expandido por padrão
        with st.expander(f"📌 {gap['nome']}", expanded=(idx == 0)):
            st.markdown(f"**{gap['descricao']}**")
            
            # Badge de impacto com cores
            impacto_badge = {
                'Alto': '🔴 Alto',
                'Médio': '🟡 Médio',
                'Baixo': '🟢 Baixo'
            }.get(gap.get('impacto', 'Médio'), '🟡 Médio')
            
            st.markdown(f"*Impacto:* {impacto_badge}")
            st.markdown("---")
            
            gap_id = f"gap_{idx}"
            
            # Campo de texto para resposta
            valor_atual = st.session_state.gaps_respondidos.get(gap_id, {}).get('resposta', '')
            
            resposta = st.text_area(
                "Você tem experiência com isso? Descreva:",
                value=valor_atual,
                height=100,
                key=f"textarea_{gap_id}",
                placeholder="Ex: Trabalhei com Python por 2 anos em projetos de automação, criando scripts para processar dados..."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Salvar Resposta", key=f"salvar_{gap_id}", use_container_width=True):
                    if resposta.strip():
                        st.session_state.gaps_respondidos[gap_id] = {
                            'nome': gap['nome'],
                            'resposta': resposta,
                            'tem_experiencia': True,
                            'impacto': gap.get('impacto', 'Médio')
                        }
                        st.success("✅ Resposta salva!")
                        st.rerun()  # Atualizar UI
                    else:
                        st.warning("⚠️ Digite algo antes de salvar")
            
            with col2:
                if st.button("❌ Não Tenho", key=f"nao_tenho_{gap_id}", use_container_width=True):
                    st.session_state.gaps_respondidos[gap_id] = {
                        'nome': gap['nome'],
                        'resposta': '',
                        'tem_experiencia': False,
                        'impacto': gap.get('impacto', 'Médio')
                    }
                    st.info("✅ Marcado como 'não possui'")
                    st.rerun()  # Atualizar UI
            
            # Mostrar status se já respondido
            if gap_id in st.session_state.gaps_respondidos:
                dados = st.session_state.gaps_respondidos[gap_id]
                if dados['tem_experiencia']:
                    st.success(f"✅ Respondido: {dados['resposta'][:100]}...")
                else:
                    st.info("❌ Marcado como não possui")
    
    st.markdown("---")
    
    # Contador de progresso
    total_gaps = len(gaps)
    respondidos = len(st.session_state.gaps_respondidos)
    progresso = (respondidos / total_gaps) * 100 if total_gaps > 0 else 0
    
    st.progress(progresso / 100)
    st.markdown(f"**Progresso:** {respondidos}/{total_gaps} gaps respondidos ({progresso:.0f}%)")
    
    st.markdown("---")
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.fase = 'CHAT'
            st.rerun()
    
    with col2:
        if st.button("🚀 CONTINUAR OTIMIZAÇÃO", use_container_width=True, type="primary"):
            if respondidos == 0:
                st.warning("⚠️ Responda pelo menos 1 gap antes de continuar")
            else:
                # Preparar contexto para a IA
                contexto_gaps = preparar_contexto_gaps()
                st.session_state.contexto_gaps = contexto_gaps
                
                # Ir para chat com módulo otimizador ativo
                st.session_state.fase = 'CHAT'
                st.session_state.modulo_ativo = 'OTIMIZADOR'  # MAIÚSCULA para match no chat
                st.session_state.etapa_modulo = 'AGUARDANDO_OK'  # Começar do OK
                st.rerun()


def preparar_contexto_gaps():
    """
    Prepara contexto estruturado com as respostas dos gaps para a IA.
    
    Returns:
        str: Contexto formatado em markdown para a IA
    """
    gaps_respondidos = st.session_state.gaps_respondidos
    
    contexto = "### 📋 RESPOSTAS DO CANDIDATO SOBRE GAPS:\n\n"
    
    tem_experiencia = []
    nao_tem_experiencia = []
    
    for gap_id, dados in gaps_respondidos.items():
        if dados['tem_experiencia']:
            tem_experiencia.append({
                'nome': dados['nome'],
                'resposta': dados['resposta'],
                'impacto': dados['impacto']
            })
        else:
            nao_tem_experiencia.append({
                'nome': dados['nome'],
                'impacto': dados['impacto']
            })
    
    if tem_experiencia:
        contexto += "#### ✅ Skills/Experiências que o candidato POSSUI:\n\n"
        for item in tem_experiencia:
            contexto += f"• **{item['nome']}** (Impacto: {item['impacto']}): {item['resposta']}\n"
        contexto += "\n"
    
    if nao_tem_experiencia:
        contexto += "#### ❌ Skills que o candidato NÃO possui:\n\n"
        for item in nao_tem_experiencia:
            contexto += f"• {item['nome']} (Impacto: {item['impacto']})\n"
        contexto += "\n"
    
    contexto += """
---

**INSTRUÇÕES CRÍTICAS PARA OTIMIZAÇÃO:**

1. **Use APENAS** as informações fornecidas pelo candidato acima
2. **NÃO invente** experiências que ele não mencionou
3. **Destaque estrategicamente** as skills que ele TEM
4. Para skills que faltam (marcadas com ❌):
   - Sugira como compensar com outras qualidades
   - Foque em transferable skills
   - Não mencione a ausência diretamente no CV
5. Para skills que ele TEM mas estavam implícitas:
   - Adicione ao CV de forma quantificável
   - Use verbos de ação e métricas quando possível

**Lembre-se:** O objetivo é OTIMIZAR o que existe, não criar ficção.
"""
    
    return contexto
