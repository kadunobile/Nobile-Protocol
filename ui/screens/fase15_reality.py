import streamlit as st
import logging
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt, scroll_topo, forcar_topo
from core.ats_scorer import calcular_score_ats, classificar_score
from core.ats_constants import SKILL_DESCRIPTIONS
from core.salary_lookup import buscar_salario_real, formatar_dados_salariais_para_prompt

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# VALIDAÇÃO DE SALÁRIO COM SALARY BANDS
# ─────────────────────────────────────────────

def _validar_plausibilidade_salario(pretensao_str, cargo, senioridade):
    """
    DEPRECATED: This function is deprecated. Use validar_salario_banda from core.salary_bands instead.
    
    This legacy function has been simplified to always return a valid result.
    The actual salary validation logic has been moved to core.salary_bands module
    which provides more accurate validation using real market data.
    
    Returns:
        dict: Always returns {'plausivel': True, 'mensagem': '', 'faixa_sugerida': ''}
    """
    return {'plausivel': True, 'mensagem': '', 'faixa_sugerida': ''}


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
    senioridade = perfil.get('senioridade', 'Não identificada')

    # Fetch real salary data from salario.com.br
    # Note: This performs an external HTTP request during page render.
    # The request has a 10-second timeout and uses session_state caching
    # to avoid repeated calls on Streamlit reruns. If the request fails,
    # it gracefully falls back to None and GPT proceeds without salary data.
    dados_salariais = buscar_salario_real(cargo, cache_dict=st.session_state)
    dados_salariais_texto = formatar_dados_salariais_para_prompt(dados_salariais)

    # Build salary instruction based on whether we have real data
    if dados_salariais and dados_salariais_texto.strip():
        instrucao_salarial = f"""
INSTRUÇÕES PARA ANÁLISE SALARIAL — DADOS REAIS DISPONÍVEIS:
{dados_salariais_texto}

⚠️ REGRA ABSOLUTA: Use os dados acima como BASE OBRIGATÓRIA.
- Os percentis P25, P50, P75 DEVEM ser derivados dos dados acima
- NÃO invente valores diferentes dos dados fornecidos
- Você pode contextualizar e explicar os dados, mas NÃO alterar os valores
- Se a pretensão do candidato está fora da faixa dos dados, diga explicitamente
"""
        referencia_texto = f"*Referências: Dados baseados em pesquisas salariais de mercado (Robert Half, Michael Page, Glassdoor, Catho, Gupy Trends) para {cargo} nível {senioridade} em {local}, período 2024-2025.*"
    else:
        instrucao_salarial = f"""
INSTRUÇÕES PARA ANÁLISE SALARIAL — SEM DADOS CONFIRMADOS DE FONTES EXTERNAS:

⚠️ Não foi possível obter dados salariais de fontes externas para o cargo "{cargo}" em "{local}".

REGRAS:
- Você PODE e DEVE dar estimativas de P25, P50 e P75 baseadas no seu conhecimento geral do mercado brasileiro
- As estimativas devem ser REALISTAS para o cargo, senioridade e localidade
- DEIXE CLARO que são estimativas, NÃO dados confirmados
- NÃO cite fontes específicas como se tivesse consultado — diga "estimativas baseadas em conhecimento geral do mercado"
- Considere: cargo "{cargo}", senioridade do candidato, localidade "{local}", mercado 2024-2025
- Para cargos de gerência/direção em SP: P50 geralmente entre R$15.000-R$35.000 dependendo do setor
- Para cargos executivos/C-level em SP: P50 geralmente entre R$25.000-R$50.000+
- Ajuste conforme o setor (tech/SaaS tende a pagar mais)
"""
        referencia_texto = f"*⚠️ Valores estimados com base em conhecimento geral do mercado — para dados atualizados, consulte Glassdoor, Guia Salarial Robert Half 2025, Catho, Levels.fyi.*"
    
    # Build conditional salary template for user message
    if dados_salariais and dados_salariais_texto.strip():
        # Template WITH table (when we have real data)
        secao_salarial_template = f"""### 📊 ANÁLISE SALARIAL

**Pretensão Informada:** {pretensao} mensal

**Faixa Salarial CLT (para este perfil/senioridade em {local}):**

| Percentil | Valor Mensal | Contexto |
|-----------|-------------|----------|
| P25 (Início de faixa) | R$ X.XXX | Empresas menores, interior ou candidatos em transição |
| P50 (Mediana) | R$ X.XXX | Mercado geral para este nível em {local} |
| P75 (Top de faixa) | R$ X.XXX | Multinacionais, grandes empresas, perfis disputados |

**Equivalente PJ estimado:** R$ X.XXX a R$ X.XXX/mês (sem benefícios CLT, ~30-40% acima do CLT)

**Veredito:** [Abaixo do P25 / Entre P25-P50 / Na Mediana (P50) / Entre P50-P75 / Acima do P75]

**Contexto Regional:** [Explicação de 2-3 linhas sobre o mercado para esse cargo específico na região]

{referencia_texto}"""
    else:
        # Template WITHOUT table (when no real data) — GPT gives estimates with disclaimer
        secao_salarial_template = f"""### 📊 ANÁLISE SALARIAL

**Pretensão Informada:** {pretensao} mensal

**Faixa Salarial ESTIMADA CLT (para este perfil/senioridade em {local}):**

⚠️ *Estimativas baseadas em conhecimento geral do mercado — NÃO são dados confirmados de pesquisas salariais.*

| Percentil | Valor Mensal Estimado | Contexto |
|-----------|----------------------|----------|
| P25 (Início de faixa) | R$ X.XXX | Empresas menores, interior ou candidatos em transição |
| P50 (Mediana) | R$ X.XXX | Mercado geral para este nível em {local} |
| P75 (Top de faixa) | R$ X.XXX | Multinacionais, grandes empresas, perfis disputados |

**Equivalente PJ estimado:** R$ X.XXX a R$ X.XXX/mês (sem benefícios CLT, ~30-40% acima do CLT)

**Veredito:** [Abaixo do P25 / Entre P25-P50 / Na Mediana (P50) / Entre P50-P75 / Acima do P75]

**Contexto Regional:** [Explicação de 2-3 linhas sobre o mercado para esse cargo na região]

*⚠️ Valores estimados com base em conhecimento geral. Para dados atualizados, consulte: Glassdoor, Guia Salarial Robert Half 2025, Catho, Levels.fyi.*"""

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

{instrucao_salarial}

- Analise a SENIORIDADE REAL do candidato com base no CV (anos de experiência, cargos ocupados, empresas)
- Considere o CARGO-ALVO específico, não uma faixa genérica do mercado
- Considere a LOCALIDADE e se aceita remoto
- A faixa salarial deve refletir o perfil REAL do candidato (não range genérico de Jr a Sr)
- Se o candidato tem 10+ anos de experiência e cargos de gerência/direção, a faixa deve refletir senioridade alta

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

{secao_salarial_template}

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
        perfil = st.session_state.get('perfil', {})
        resultado = calcular_score_ats(
            cv_texto=cv_texto,
            cargo_alvo=cargo,
            client=st.session_state.openai_client,
            objetivo=perfil.get('objetivo'),
            cargo_atual=perfil.get('cargo_atual')
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

    # Recuperar cargo-alvo do perfil
    perfil = st.session_state.get('perfil', {})
    cargo = perfil.get('cargo_alvo', 'o cargo')

    st.markdown("---")
    st.markdown(f"### 🤖 ANÁLISE DE COMPATIBILIDADE ATS — {cargo.upper()}")
    
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
    <div style="font-size: 0.85rem; color: #888; margin-top: 8px;">Cargo-alvo: {cargo}</div>
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

    # ── Skills que faltam (DETALHADO) ──
    if gaps:
        # Mapeamento de descrições de skills conhecidas
        SKILL_DESCRIPTIONS = {
            'Outreach': 'Plataforma de sales engagement para sequências de e-mails, ligações e follow-ups automatizados',
            'Outreach.io': 'Plataforma de sales engagement para sequências de e-mails, ligações e follow-ups automatizados',
            'Gong': 'Plataforma de análise de conversas e vendas que grava e analisa interações com clientes',
            'Gong.io': 'Plataforma de análise de conversas e vendas que grava e analisa interações com clientes',
            'Salesforce': 'CRM líder de mercado para gestão de relacionamento com clientes e pipeline de vendas',
            'HubSpot': 'Plataforma de marketing, vendas e CRM para gestão integrada do funil comercial',
            'LinkedIn Sales Navigator': 'Ferramenta de prospecção avançada do LinkedIn para identificação de leads',
            'Salesloft': 'Plataforma de sales engagement similar ao Outreach para automação de vendas',
            'ZoomInfo': 'Base de dados B2B para prospecção e enriquecimento de leads',
            'Apollo': 'Plataforma de prospecção e engajamento de vendas com base de dados integrada',
            'Apollo.io': 'Plataforma de prospecção e engajamento de vendas com base de dados integrada',
            'Chorus': 'Plataforma de análise de conversas similar ao Gong',
            'Drift': 'Plataforma de conversational marketing e chatbots para engajamento',
            'Intercom': 'Plataforma de mensagens e suporte ao cliente para engajamento',
        }
        
        st.markdown("**❌ Skills que FALTAM no seu CV (exigidas para o cargo):**")
        st.markdown("")
        for i, termo in enumerate(gaps[:10]):
            # Extrair nome do gap (pode ser string simples ou dict)
            nome_gap = termo if isinstance(termo, str) else termo.get('nome', str(termo))
            
            # Buscar descrição da skill (case-insensitive)
            descricao = None
            for skill_key, skill_desc in SKILL_DESCRIPTIONS.items():
                if skill_key.lower() == nome_gap.lower():
                    descricao = skill_desc
                    break
            
            # Fallback se skill não está no dicionário
            if not descricao:
                descricao = "Competência relevante para o cargo — pesquise mais sobre esta skill para entender como aplicá-la."
            
            st.markdown(f"""
<div style="background:#2a1a1a; border-left:3px solid #f87171; padding:10px 14px; border-radius:6px; margin:6px 0;">
    <div style="color:#f87171; font-weight:bold; font-size:0.95rem;">❌ {nome_gap}</div>
    <div style="color:#ccc; font-size:0.82rem; margin-top:4px;">
        📌 Skill exigida para <strong>{cargo}</strong> — não encontrada no seu CV atual
    </div>
    <div style="color:#888; font-size:0.8rem; margin-top:6px; padding-top:6px; border-top:1px solid #333;">ℹ️ <strong>O que é:</strong> {descricao}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("")
    
    # ── Transparência - Skills DESCARTADAS como gaps (SEMPRE VISÍVEL) ──
    st.markdown("**🔍 Transparência — Skills analisadas e DESCARTADAS como gaps:**")
    if gaps_falsos:
        st.caption("Nosso algoritmo analisou estas skills mas seu CV já as cobre adequadamente:")
        st.markdown("")
        
        # Renderizar como badges amarelos inline
        badges_html = ""
        for item in gaps_falsos[:8]:
            nome = item if isinstance(item, str) else item.get('nome', str(item))
            badges_html += (
                f"<span style='background:#3a3a1a; color:#facc15; padding:5px 12px; "
                f"border-radius:20px; font-size:0.85rem; display:inline-block; margin:4px;'>"
                f"🟡 {nome}</span>"
            )
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.caption(f"Nenhuma skill descartada como gap para este cargo.")
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
                return

            # Ensure all required state variables are set for downstream phases
            if resultado_ats:
                # Set gaps_alvo and gaps_identificados for the optimizer
                # Both variables point to the same gaps list for compatibility with different phases
                # gaps_alvo: used by processor.py for the optimizer flow
                # gaps_identificados: expected by various UI screens for display
                st.session_state.gaps_alvo = resultado_ats.get('gaps_identificados', [])
                st.session_state.gaps_identificados = resultado_ats.get('gaps_identificados', [])

            st.session_state.mensagens = []
            st.session_state.modulo_ativo = None
            st.session_state.etapa_modulo = None
            st.session_state.fase = 'FASE_BRIDGE_OTIMIZACAO'
            st.rerun()