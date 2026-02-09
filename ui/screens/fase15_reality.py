import streamlit as st
import logging
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt, scroll_topo, forcar_topo
from core.ats_scorer import calcular_score_ats, classificar_score

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# GERAÇÃO DO REALITY CHECK (com cache)
# ─────────────────────────────────────────────

def _gerar_reality_check():
    """
    Gera o Reality Check via GPT.
    Usa cache no session_state para evitar re-chamadas a cada rerun.
    """
    if st.session_state.get('reality_check_resultado'):
        return st.session_state.reality_check_resultado

    perfil = st.session_state.get('perfil', {})
    analise_inicial = st.session_state.get('analise_inicial')

    if not perfil.get('cargo_alvo'):
        st.error("⚠️ Dados do briefing incompletos. Volte e preencha o cargo-alvo.")
        return None

    if not analise_inicial:
        st.error("⚠️ Análise inicial não encontrada. Faça upload do CV novamente.")
        return None

    pretensao = perfil.get('pretensao_salarial', 'Não informada')
    cargo = perfil['cargo_alvo']
    local = perfil.get('localizacao', 'Brasil')
    objetivo = perfil.get('objetivo', 'Recolocação')
    remoto = 'Sim' if perfil.get('remoto') else 'Não'

    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT + f"""

INSTRUÇÕES INTERNAS (NÃO MOSTRAR AO USUÁRIO):

⚠️ REGRA CRÍTICA ao mencionar gaps:
- ANTES de marcar algo como gap, busque sinônimos e variações no CV do candidato
  * Ex: "liderança" pode aparecer como "gestão de equipe", "coordenação"
  * Ex: "Python" pode estar em "automação", "scripts", "análise de dados"
- Só mencione como gap se NÃO encontrado em NENHUMA forma (literal ou contextual)
- APENAS mencione gaps diretamente relacionados ao cargo {cargo}
- Gaps devem ser corrigíveis (não invente barreiras inexistentes)
- Relevância para o mercado de {local}

❌ NÃO MENCIONE:
- "Falta experiência internacional" (removido - não é relevante para a maioria dos cargos)
- "Falta conhecimento em [tecnologia X]" (a menos que seja padrão obrigatório no cargo)
- Gaps genéricos de livros de carreira

IMPORTANTE SOBRE NOMENCLATURAS:
- Na seção "NOMENCLATURAS SIMILARES NO MERCADO", liste cargos REAIS usados em vagas reais
- Exemplos concretos de como recrutadores publicam vagas para esse perfil
- Inclua variações em português E inglês
- Inclua o nível (Jr, Pleno, Sr) quando relevante

IMPORTANTE: Seja ESPECÍFICO e REALISTA. Base-se APENAS no CV fornecido e nas expectativas reais do mercado para {cargo} em {local}.

⚠️ NÃO inclua seção "Estratégia" no final. Termine após o "Nível de Desafio" do Veredito do Headhunter.
A seção de análise ATS será adicionada automaticamente pelo sistema.
"""},
        {"role": "user", "content": f"""REALITY CHECK:

P1 Objetivo: {objetivo}
P2 Cargo: {cargo}
P3 Pretensão: {pretensao} mensal
P4 Local: {local}
Remoto: {remoto}

DEEP SCAN:
{analise_inicial}

FORMATO EXATO OBRIGATÓRIO:

🎯 **REALITY CHECK - ANÁLISE ESTRATÉGICA**

**CARGO DESEJADO:** {cargo}

**NOMENCLATURAS SIMILARES NO MERCADO:**
• [Nome REAL de cargo em vaga 1 — ex: "Product Manager Sr" ou "Gerente de Produto Digital"]
• [Nome REAL de cargo em vaga 2 — ex: "Head of Product" ou "PM Lead"]
• [Nome REAL de cargo em vaga 3 — em inglês se aplicável]
• [Nome REAL de cargo em vaga 4 — variação regional]
• [Nome REAL de cargo em vaga 5 — nível diferente]

*(Esses são os nomes que recrutadores REALMENTE usam em vagas. Pesquise no LinkedIn e portais de emprego com essas variações.)*

---

### 📊 ANÁLISE SALARIAL

**Pretensão Informada:** {pretensao} mensal

**Faixa Salarial Geral:** [mínimo] a [máximo]

**Veredito:** [Abaixo/Na Média/Acima]

[Contexto sobre o mercado para esse cargo em {local}]

---

### 🎯 VEREDITO DO HEADHUNTER

**Nível de Desafio:** [Baixo/Médio/Alto]

[Breve explicação do porquê — 1-2 linhas apenas]"""}
    ]

    reality = chamar_gpt(
        st.session_state.openai_client,
        msgs,
        temperature=0.1,
        seed=42
    )

    if reality:
        st.session_state.reality_check_resultado = reality
        logger.info("Reality Check gerado e salvo em cache")

    return reality


# ─────────────────────────────────────────────
# ANÁLISE ATS (CV × Cargo)
# ─────────────────────────────────────────────

def _executar_analise_ats():
    """
    Executa análise ATS real usando TF-IDF do CV contra Job Description do cargo.
    Usa cache no session_state.
    """
    if st.session_state.get('reality_ats_resultado'):
        return st.session_state.reality_ats_resultado

    cv_texto = st.session_state.get('cv_texto')
    cargo = st.session_state.get('perfil', {}).get('cargo_alvo')

    if not cv_texto or not cargo:
        return None

    with st.spinner("🤖 Calculando Score ATS — CV × Skills do Cargo..."):
        resultado = calcular_score_ats(
            cv_texto=cv_texto,
            cargo_alvo=cargo,
            client=st.session_state.openai_client
        )

    if resultado:
        st.session_state.reality_ats_resultado = resultado
        if not st.session_state.get('score_ats_inicial'):
            st.session_state.score_ats_inicial = resultado['score_total']
        logger.info(f"ATS Score calculado: {resultado['score_total']}/100")

    return resultado


def _renderizar_ats(resultado_ats):
    """Renderiza a seção de Análise ATS no Reality Check."""
    if not resultado_ats:
        st.warning("⚠️ Não foi possível calcular o Score ATS.")
        return

    score = resultado_ats['score_total']
    nivel = resultado_ats['nivel']
    pontos_fortes = resultado_ats.get('pontos_fortes', [])
    gaps = resultado_ats.get('gaps_identificados', [])
    plano = resultado_ats.get('plano_acao', [])
    
    # v5.0: novos campos
    arquetipo = resultado_ats.get('arquetipo_cargo', 'N/A')
    metodo = resultado_ats.get('metodo', 'N/A')
    fonte_vaga = resultado_ats.get('fonte_vaga', 'N/A')
    gaps_falsos = resultado_ats.get('gaps_falsos_ignorados', [])

    st.markdown("---")
    st.markdown("### 🤖 ANÁLISE ATS — SEU CV × SKILLS DO CARGO")
    
    # v5.0: User-friendly label instead of technical metadata
    if arquetipo != 'N/A':
        st.caption(f"✨ Análise Inteligente para perfil de {arquetipo}")
    
    st.markdown("")

    # ── Score visual ──
    if score >= 70:
        cor = "#4ade80"
        emoji = "🟢"
    elif score >= 50:
        cor = "#facc15"
        emoji = "🟡"
    elif score >= 30:
        cor = "#fb923c"
        emoji = "🟠"
    else:
        cor = "#f87171"
        emoji = "🔴"

    st.markdown(f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid {cor}; border-radius: 12px; padding: 20px; text-align: center; margin: 10px 0;">
    <div style="font-size: 3rem; font-weight: bold; color: {cor};">{score}/100</div>
    <div style="font-size: 1.1rem; color: #e0e0e0;">{emoji} {nivel} — Compatibilidade ATS</div>
    <div style="font-size: 0.85rem; color: #888; margin-top: 8px;">Análise de Compatibilidade ATS</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("")

    # ── Skills encontradas ──
    if pontos_fortes:
        st.markdown("**✅ Skills encontradas no seu CV:**")
        cols_fortes = st.columns(min(len(pontos_fortes), 4))
        for i, termo in enumerate(pontos_fortes[:8]):
            with cols_fortes[i % min(len(pontos_fortes), 4)]:
                st.markdown(f"<span style='background:#1a472a; color:#4ade80; padding:4px 10px; border-radius:20px; font-size:0.85rem; white-space:nowrap; display:inline-block;'>✅ {termo}</span>", unsafe_allow_html=True)
        st.markdown("")

    # ── Skills que faltam ──
    if gaps:
        st.markdown("**❌ Skills que FALTAM no seu CV (exigidas para o cargo):**")
        cols_gaps = st.columns(min(len(gaps), 4))
        for i, termo in enumerate(gaps[:10]):
            with cols_gaps[i % min(len(gaps), 4)]:
                st.markdown(f"<span style='background:#4a1a1a; color:#f87171; padding:4px 10px; border-radius:20px; font-size:0.85rem; white-space:nowrap; display:inline-block;'>❌ {termo}</span>", unsafe_allow_html=True)
        st.markdown("")
    
    # ── v5.0: Transparência - Skills NÃO consideradas gaps ──
    if gaps_falsos:
        with st.expander("🔍 Transparência: Skills que NÃO foram consideradas gaps"):
            st.caption("Estas skills foram analisadas mas **descartadas** como gaps:")
            for item in gaps_falsos[:8]:
                st.markdown(f"- 🟡 {item}")
        st.markdown("")

    # ── Plano de ação ──
    if plano:
        st.markdown("**📋 Plano de Ação:**")
        for item in plano:
            st.markdown(f"  {item}")
        st.markdown("")


# ─────────────────────────────────────────────
# BARRA DE PROGRESSO
# ─────────────────────────────────────────────

def _renderizar_barra_progresso():
    """Indicador visual de onde o usuário está no fluxo."""
    etapas = [
        ("📄 Upload", True),
        ("🔍 Diagnóstico", True),
        ("📋 Briefing", True),
        ("🧠 Reality Check", True),
        ("🔧 Otimização", False),
        ("📥 Export", False),
    ]

    cols = st.columns(len(etapas))
    for i, (nome, concluida) in enumerate(etapas):
        with cols[i]:
            if concluida:
                st.markdown(
                    f"<div style='text-align:center; padding:4px 2px; background:#1a472a; "
                    f"border-radius:6px; font-size:0.72rem; color:#4ade80;'>✅ {nome}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align:center; padding:4px 2px; background:#2a2a3e; "
                    f"border-radius:6px; font-size:0.72rem; color:#888;'>⬜ {nome}</div>",
                    unsafe_allow_html=True
                )
    st.markdown("")


# ─────────────────────────────────────────────
# FUNÇÃO PRINCIPAL
# ─────────────────────────────────────────────

def fase_15_reality_check():
    """
    Reality Check — Análise Estratégica + Score ATS integrado.

    Fluxo:
    1. Gera Reality Check via GPT (cargo, salário, mercado, veredito)
    2. Executa análise ATS real (TF-IDF CV × JD do cargo)
    3. Exibe Score + Skills encontradas + Skills faltantes + Plano de ação
    4. Botão único de avançar para otimização
    """
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    scroll_topo()

    st.markdown("# 🧠 Reality Check - Análise Crítica")
    st.markdown("---")

    _renderizar_barra_progresso()

    st.info("""
    **O que é Reality Check?**  
    Uma análise honesta e detalhada do seu CV, identificando:
    - ✅ Pontos fortes que você deve enfatizar
    - ❌ Gaps (lacunas) que precisam ser corrigidos
    - 💡 Oportunidades de melhoria
    - 🤖 Score ATS real do seu CV para o cargo desejado
    
    Esta análise funciona para **qualquer cargo**: júnior, pleno, sênior, gerente, diretor, etc.
    """)

    # ── 1) Reality Check (GPT) ──
    reality = _gerar_reality_check()

    if not reality:
        st.error("❌ Não foi possível gerar o Reality Check. Tente novamente.")
        if st.button("🔄 Tentar Novamente"):
            st.session_state.reality_check_resultado = None
            st.rerun()
        return

    # Preparar mensagens para uso no chat
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    st.session_state.mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\n\nCV DO CANDIDATO (uso interno): {st.session_state.cv_texto}\n\nCARGO-ALVO: {cargo}"},
        {"role": "assistant", "content": reality}
    ]
    st.session_state.force_scroll_top = True

    # Exibir resultado do Reality Check
    st.markdown(reality)

    # ── 2) Análise ATS (TF-IDF real) ──
    resultado_ats = _executar_analise_ats()
    _renderizar_ats(resultado_ats)

    # ── 3) Botão único: Avançar ──
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 AVANÇAR — OTIMIZAR CV + LINKEDIN", use_container_width=True, type="primary"):
            if not st.session_state.get('cv_texto'):
                st.error("⚠️ CV não encontrado. Faça upload novamente.")
                st.session_state.fase = 'FASE_0_UPLOAD'
                st.rerun()

            st.session_state.mensagens = []
            st.session_state.modulo_ativo = None
            st.session_state.etapa_modulo = None
            st.session_state.fase = 'FASE_BRIDGE_OTIMIZACAO'
            forcar_topo()
            st.rerun()