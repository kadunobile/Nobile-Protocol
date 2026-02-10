"""
Demo visual do badge de telemetria GPT.

Este arquivo demonstra como o badge aparecerá na interface do usuário.
Execute com: streamlit run docs/badge_demo.py
"""

import streamlit as st

st.set_page_config(page_title="Badge Demo", page_icon="🔍", layout="wide")

st.title("🎯 Demo: Badge de Telemetria GPT")
st.markdown("---")

st.markdown("""
### Como o badge aparecerá no Headhunter Elite:

O badge é exibido no **topo do chat**, logo abaixo do título "Headhunter Elite — Otimização Ativa".

Ele muda de cor conforme o número de chamadas GPT aumenta:
""")

# Simular diferentes estados do badge
estados = [
    (0, "#888888", "⚪", "Cinza - Nenhuma chamada ainda"),
    (3, "#4CAF50", "🟢", "Verde - Uso leve (1-5 chamadas)"),
    (10, "#FFC107", "🟡", "Amarelo - Uso moderado (6-15 chamadas)"),
    (20, "#FF9800", "🟠", "Laranja - Uso elevado (16-30 chamadas)"),
    (35, "#F44336", "🔴", "Vermelho - Uso intenso (31+ chamadas)"),
]

for count, color, emoji, descricao in estados:
    st.markdown(f"**{descricao}**")
    
    # Renderizar badge
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}22 0%, {color}11 100%);
        border: 2px solid {color};
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        {emoji} <span style="color: {color};">Chamadas GPT nesta sessão:</span> <span style="font-size: 18px; color: {color};">{count}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

st.markdown("""
### Funcionalidade

- **Incremento automático**: Cada chamada para o GPT incrementa o contador
- **Rastreamento por contexto**: Internamente, rastreia por etapa (diagnóstico, coleta, etc.)
- **Visibilidade**: O usuário sempre sabe quantas chamadas foram feitas
- **Transparência**: Ajuda a gerenciar custos e expectativas

### Detalhes Técnicos

```python
# Exemplo de uso no código
from core.gpt_telemetry import chamar_gpt_com_telemetria, CONTEXTO_COLETA

resp = chamar_gpt_com_telemetria(
    client,
    msgs,
    contexto=CONTEXTO_COLETA,
    temperature=0.3
)
# Contador incrementa automaticamente
```

### Estatísticas Detalhadas

Você também pode expandir detalhes para ver breakdown por etapa:
""")

# Simular estatísticas expandidas
with st.expander("📊 Detalhes de Uso da API", expanded=False):
    st.markdown("**Chamadas GPT por etapa:**")
    
    stats = {
        "🔍 Diagnóstico": 3,
        "📝 Coleta Focada": 8,
        "✍️ Reescrita": 2,
        "🔵 LinkedIn": 1,
        "✅ Validação": 1,
        "💬 Outros": 0,
    }
    
    for label, count in stats.items():
        st.text(f"{label}: {count}")
    
    st.markdown("---")
    st.markdown(f"**Total Geral:** {sum(stats.values())}")

st.markdown("---")
st.success("✅ Badge implementado e funcional no PR!")
