"""
Sistema de Pontuação ATS (Applicant Tracking System) - v5.0.

v5.0: Arquitetura Híbrida LLM + TF-IDF com 3 cenários:
- Cenário A: Vaga real fornecida (análise ultra-precisa)
- Cenário B: Título + arquétipo + double-check (análise inteligente)
- Cenário C: Fallback TF-IDF offline (v3.2)

v4.0: Análise contextual via LLM (GPT-4o) com fallback TF-IDF.
- Quando OpenAI client disponível: análise semântica inteligente
- Quando offline: TF-IDF + Cosine Similarity (v3.2)

v3.2 (fallback):
- TF-IDF + Cosine Similarity com stopwords NLTK (PT/EN) + termos customizados
- Prompt da JD focado em termos técnicos, ferramentas e siglas
- Filtro de n-grams genéricos nos gaps e pontos fortes

Retorna: Score + Pontos Fortes + Gaps + Plano de Ação + Arquétipo + Transparência.
"""

import re
import json
import logging
from typing import Dict, Optional, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Garantir download dos stopwords na primeira execução
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords

from core.utils import chamar_gpt

logger = logging.getLogger(__name__)

# ─── STOPWORDS: NLTK (PT + EN) + Termos customizados de CV/JD ───
# Base robusta do NLTK (~400 stopwords PT + EN)
_nltk_stops = set(stopwords.words('portuguese')).union(set(stopwords.words('english')))

# Termos customizados específicos de CV e Job Descriptions
_custom_stops = {
    # ─── VERBOS GENÉRICOS DE JD (aparecem em QUALQUER vaga) ───
    'desenvolver', 'gerenciar', 'impulsionar', 'otimizar', 'garantir', 'implementar',
    'coordenar', 'supervisionar', 'elaborar', 'executar', 'planejar', 'monitorar',
    'acompanhar', 'realizar', 'conduzir', 'promover', 'apoiar', 'contribuir',
    'participar', 'atuar', 'assegurar', 'propor', 'definir', 'estabelecer',
    'manter', 'identificar', 'analisar', 'avaliar', 'gerir', 'liderar',
    'orientar', 'direcionar', 'facilitar', 'viabilizar', 'fomentar',
    'aprimorar', 'estruturar', 'organizar', 'controlar', 'reportar',
    'comunicar', 'interagir', 'colaborar', 'integrar', 'alinhar',
    'priorizar', 'delegar', 'negociar', 'articular', 'mapear',
    'diagnosticar', 'solucionar', 'resolver', 'mitigar', 'prevenir',
    'develop', 'manage', 'drive', 'optimize', 'ensure', 'implement',
    'coordinate', 'supervise', 'execute', 'plan', 'monitor',
    'track', 'conduct', 'promote', 'support', 'contribute',
    'participate', 'maintain', 'identify', 'analyze', 'evaluate',
    'lead', 'guide', 'direct', 'facilitate', 'foster',
    'enhance', 'structure', 'organize', 'control', 'report',
    'communicate', 'collaborate', 'integrate', 'align', 'prioritize',
    'delegate', 'negotiate', 'deliver', 'build', 'create', 'design',
    'establish', 'provide', 'work', 'handle', 'oversee', 'prepare',
    # ─── PALAVRAS GENÉRICAS DE JD / CV ───
    'empresa', 'área', 'equipe', 'time', 'profissional', 'candidato',
    'experiência', 'conhecimento', 'habilidade', 'capacidade', 'competência',
    'responsável', 'responsabilidade', 'atividade', 'atividades', 'função',
    'objetivo', 'resultado', 'resultados', 'processo', 'processos',
    'projeto', 'projetos', 'solução', 'soluções', 'estratégia', 'estratégias',
    'nível', 'alto', 'alta', 'forte', 'fortes', 'sólida', 'sólido',
    'bom', 'boa', 'bons', 'boas', 'excelente', 'excelentes',
    'desejável', 'desejáveis', 'necessário', 'necessária', 'obrigatório', 'obrigatória',
    'diferencial', 'diferenciais', 'requisito', 'requisitos',
    'mínimo', 'mínima', 'anos', 'ano', 'superior', 'completo', 'completa',
    'graduação', 'formação', 'pós', 'curso', 'cursos',
    'trabalho', 'mercado', 'negócio', 'negócios', 'cliente', 'clientes',
    'interno', 'interna', 'internos', 'internas', 'externo', 'externa',
    'relacionamento', 'relacionamentos', 'parceiro', 'parceiros',
    'demanda', 'demandas', 'necessidade', 'necessidades',
    'oportunidade', 'oportunidades', 'melhoria', 'melhorias',
    'indicador', 'indicadores', 'meta', 'metas',
    'relatório', 'relatórios', 'report', 'reports',
    'reunião', 'reuniões', 'apresentação', 'apresentações',
    'prazo', 'prazos', 'entrega', 'entregas',
    'qualidade', 'eficiência', 'produtividade',
    'inovação', 'transformação', 'crescimento',
    'visão', 'missão', 'valor', 'valores', 'cultura',
    'based', 'ability', 'skills', 'skill', 'experience', 'knowledge',
    'team', 'company', 'business', 'role', 'position',
    'responsible', 'required', 'preferred', 'minimum', 'years',
    'strong', 'excellent', 'good', 'proven', 'relevant',
    'including', 'related', 'across', 'within', 'using',
    'new', 'key', 'high', 'level', 'well',
    # ─── TERMOS DE CV (endereço, meses, etc.) ───
    'cargo', 'janeiro', 'fevereiro', 'março', 'abril',
    'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
    'novembro', 'dezembro', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez',
    'paulo', 'são', 'rio', 'brasil', 'br', 'rua', 'apto', 'cep',
    'presente', 'atual', 'atualmente',
    # ─── CONECTORES E TERMOS VAZIOS ───
    'além', 'disso', 'assim', 'ainda', 'sobre', 'cada', 'todo', 'toda',
    'todos', 'todas', 'outro', 'outra', 'outros', 'outras',
    'onde', 'aqui', 'ali', 'lá', 'então', 'portanto', 'porém',
    'contudo', 'entretanto', 'todavia', 'pois', 'porque', 'embora',
    'caso', 'conforme', 'segundo', 'através', 'meio', 'forma',
    'modo', 'tipo', 'parte', 'fim', 'base', 'dia', 'vez',
    'vezes', 'bem', 'mal', 'demais', 'menos', 'tanto',
    'quanto', 'tal', 'tais', 'apenas', 'somente',
    'principalmente', 'especialmente', 'geralmente', 'normalmente',
    'diretamente', 'indiretamente', 'constantemente', 'continuamente',
    'relacionadas', 'relacionados', 'relacionada', 'relacionado',
    'adequada', 'adequado', 'adequadas', 'adequados',
    'efetiva', 'efetivo', 'efetivas', 'efetivos',
}

# Combinar: NLTK base (~400) + Custom (~150) = ~550+ stopwords
STOPWORDS_PT_EN = list(_nltk_stops.union(_custom_stops))

# ─── Termos genéricos que nunca devem aparecer como gap ───
_termos_genericos_gap = {
    'certified', 'certification', 'certificate',
    'qualified', 'qualification',
    'senior', 'junior', 'pleno', 'sênior', 'júnior',
    'manager', 'lead', 'head', 'director', 'chief',
    'gerente', 'coordenador', 'analista', 'especialista',
    'supervisor', 'diretor', 'líder',
    'six', 'sigma',
    'proficiency', 'proficient', 'fluent', 'fluency',
    'operations', 'operações', 'revenue', 'receita',
    'engineer', 'engenheiro', 'developer', 'desenvolvedor', 'software',
    'analyst', 'consultor', 'consultant',
}


def _limpar_texto(texto: str) -> str:
    """Padroniza o texto para análise."""
    texto = str(texto).lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def _analisar_compatibilidade(cv_texto: str, vaga_texto: str) -> Dict:
    """
    Executa análise completa: Score + Gaps + Pontos Fortes + Plano de Ação.
    
    Cria uma NOVA instância do TfidfVectorizer a cada chamada.
    
    Args:
        cv_texto: Texto completo do CV
        vaga_texto: Job Description para comparação
        
    Returns:
        Dict com score, pontos_fortes, gaps_identificados, plano_acao
    """
    cv_limpo = _limpar_texto(cv_texto)
    vaga_limpa = _limpar_texto(vaga_texto)
    
    if not cv_limpo or not vaga_limpa:
        logger.warning("CV ou JD vazio após limpeza")
        return {
            "score": 0.0,
            "pontos_fortes": [],
            "gaps_identificados": [],
            "plano_acao": ["❌ Texto insuficiente para análise."]
        }
    
    try:
        vectorizer = TfidfVectorizer(
            stop_words=STOPWORDS_PT_EN,
            ngram_range=(1, 3),
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform([cv_limpo, vaga_limpa])
        feature_names = vectorizer.get_feature_names_out()
        
    except ValueError as e:
        logger.error(f"Erro na vetorização: {e}")
        return {
            "score": 0.0,
            "pontos_fortes": [],
            "gaps_identificados": [],
            "plano_acao": ["❌ Texto insuficiente para análise."]
        }
    
    # Score (Cosine Similarity)
    raw_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Escalar para faixa realista
    if raw_similarity <= 0.0:
        score_final = 0.0
    elif raw_similarity >= 0.35:
        score_final = 95.0
    else:
        score_final = (raw_similarity / 0.35) * 90.0 + 5.0
    
    score_final = round(score_final, 1)
    
    logger.debug(f"Raw similarity: {raw_similarity:.4f}, Scaled score: {score_final}")
    logger.debug(f"Vocabulário: {len(feature_names)} termos (após stopwords)")
    
    # Análise de termos
    dense = tfidf_matrix.todense()
    lista_cv = dense[0].tolist()[0]
    lista_vaga = dense[1].tolist()[0]
    
    df_analise = pd.DataFrame({
        'termo': feature_names,
        'peso_vaga': lista_vaga,
        'peso_cv': lista_cv
    })
    
    # Gaps: termos da vaga que NÃO estão no CV
    termos_faltantes_raw = df_analise[
        (df_analise['peso_vaga'] > 0) & (df_analise['peso_cv'] == 0)
    ].sort_values(by='peso_vaga', ascending=False)
    
    # Filtrar: remover termos genéricos e n-grams que são apenas títulos de cargo
    def _is_generic_term(termo: str) -> bool:
        """Verifica se um termo deve ser filtrado dos gaps."""
        # Remover siglas muito curtas
        if len(termo) <= 2:
            return True
        
        # Remover se é termo genérico standalone
        if termo in _termos_genericos_gap:
            return True
        
        # Remover n-grams que contêm palavras genéricas
        palavras_termo = termo.split()
        for palavra in palavras_termo:
            if palavra in _termos_genericos_gap:
                return True
        
        return False
    
    termos_faltantes = termos_faltantes_raw[
        ~termos_faltantes_raw['termo'].apply(_is_generic_term)
    ].head(10)
    
    # Pontos fortes: termos que ambos têm
    pontos_fortes = df_analise[
        (df_analise['peso_vaga'] > 0) & (df_analise['peso_cv'] > 0)
    ].sort_values(by='peso_cv', ascending=False).head(8)
    
    # Plano de ação
    plano = []
    
    if score_final >= 70:
        plano.append("🏆 Excelente compatibilidade! Seu perfil está bem alinhado com o cargo. Foque em se preparar para entrevistas comportamentais.")
    elif score_final >= 50:
        plano.append("⚠️ Boa base, mas pode melhorar. Adicione as palavras-chave faltantes no seu perfil para aumentar suas chances nos filtros automáticos.")
    elif score_final >= 30:
        plano.append("🔶 Compatibilidade moderada. Seu perfil precisa de ajustes para passar pelos filtros ATS. Revise as palavras-chave e experiências.")
    else:
        plano.append("❌ Risco de eliminação automática. Seu perfil precisa de uma revisão estrutural para este cargo.")
    
    if not termos_faltantes.empty:
        lista_gaps = termos_faltantes['termo'].tolist()
        plano.append(
            f"🔍 Palavras-chave ausentes no seu perfil: **{', '.join(lista_gaps[:7]).upper()}**. "
            f"Tente incluí-las no Resumo, Competências ou Experiência."
        )
    
    return {
        "score": score_final,
        "pontos_fortes": pontos_fortes['termo'].tolist(),
        "gaps_identificados": termos_faltantes['termo'].tolist(),
        "plano_acao": plano
    }


def _analisar_com_llm(
    client, 
    cv_texto: str, 
    cargo_alvo: str, 
    texto_vaga: Optional[str] = None,
    objetivo: Optional[str] = None,
    cargo_atual: Optional[str] = None
) -> Optional[Dict]:
    """
    Analisa CV usando LLM (GPT-4o) para análise contextual inteligente.
    
    v5.0: Suporta 3 cenários:
    - Cenário A: Vaga real fornecida (texto_vaga != None)
    - Cenário B: Apenas título do cargo (classifica arquétipo primeiro)
    
    Args:
        client: Cliente OpenAI inicializado
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para o qual está se candidatando
        texto_vaga: Texto da vaga real (opcional) para análise ultra-precisa
        objetivo: Tipo de movimentação (Recolocação, Transição, Promoção Interna, Trabalho Internacional)
        cargo_atual: Cargo atual do candidato (opcional)
        
    Returns:
        Dict com score, pontos_fortes, gaps_identificados, plano_acao,
        arquetipo_cargo, gaps_falsos_ignorados, fonte_vaga ou None em caso de erro
    """
    logger.info(f"Analisando CV com LLM v5.0 para cargo: {cargo_alvo}, objetivo: {objetivo}")
    
    if texto_vaga:
        fonte = 'real'
        logger.info("Cenário A: Vaga real fornecida")
    else:
        fonte = 'arquetipo'
        logger.info("Cenário B: Análise por arquétipo")
    
    # ── PROMPT v5.0 com Arquétipo e Double-Check ──
    system_prompt = (
        "Você é um Especialista Sênior em ATS (Applicant Tracking System) e Recrutamento Tech.\n\n"
        "Sua missão é analisar o CV do candidato em comparação com as expectativas REAIS do cargo.\n\n"
    )
    
    if texto_vaga:
        # ── CENÁRIO A: Vaga Real Fornecida ──
        system_prompt += (
            "**MODO: VAGA REAL FORNECIDA**\n\n"
            "Use APENAS o texto da vaga fornecida como FONTE DA VERDADE.\n"
            "Só aponte gaps que estão EXPLICITAMENTE mencionados no texto da vaga.\n"
            "NÃO invente requisitos ou ferramentas que não estão na descrição da vaga.\n\n"
        )
    else:
        # ── CENÁRIO B: Arquétipo do Cargo ──
        system_prompt += (
            "**MODO: ANÁLISE POR ARQUÉTIPO**\n\n"
            "PASSO 1: Classifique o cargo em um ARQUÉTIPO:\n"
            "- GESTÃO: Gerente, Diretor, Coordenador, Líder, VP, C-Level\n"
            "- TÉCNICO: Engenheiro, Desenvolvedor, Arquiteto, DevOps, SRE\n"
            "- ANALÍTICO: Analista de Dados, Cientista de Dados, BI, Analytics\n"
            "- MARKETING: Marketing, Growth, Digital Marketing, Content\n"
            "- FINANCEIRO: Contabilidade, Finanças, FP&A, Controller\n"
            "- OPERAÇÕES: Operações, Supply Chain, Logística, Produção\n"
            "- VENDAS: SDR, BDR, Account Executive, Sales Manager\n\n"
            "PASSO 2: Identifique o NÍVEL HIERÁRQUICO do cargo:\n"
            "- INDIVIDUAL CONTRIBUTOR: Analista (Jr/Pl/Sr), Especialista, Engenheiro\n"
            "- COORDENAÇÃO: Coordenador, Team Lead, Tech Lead\n"
            "- GERÊNCIA: Gerente, Head, Manager\n"
            "- DIREÇÃO: Diretor, VP, C-Level\n\n"
            "PASSO 3: Ajuste gaps e score conforme o nível:\n"
            "- COORDENAÇÃO+: DEVE incluir gaps de gestão (liderança de equipe, orçamento, gestão de stakeholders)\n"
            "- GERÊNCIA+: DEVE incluir gaps estratégicos (planejamento estratégico, budget de departamento, P&L)\n"
            "- DIREÇÃO: DEVE incluir gaps executivos (visão estratégica, transformação organizacional, board reporting)\n"
            "- Score mais rigoroso para níveis de gestão: métricas de liderança têm peso MAIOR\n\n"
            "PASSO 4: Liste gaps APENAS de ferramentas/skills que são PADRÃO "
            "para 80%+ das vagas desse arquétipo E nível específicos.\n\n"
            "EXEMPLO: Para 'Coordenador de Supply Chain', gaps válidos incluem: "
            "ferramentas técnicas do arquétipo (SAP, WMS) + competências de coordenação "
            "(gestão de equipe, indicadores de performance, gestão de fornecedores).\n\n"
        )
    
    # ── Ajuste conforme tipo de movimentação (objetivo) ──
    if objetivo:
        system_prompt += f"\n**TIPO DE MOVIMENTAÇÃO: {objetivo}**\n\n"
        
        if objetivo == "Promoção Interna" or "promoção" in objetivo.lower():
            system_prompt += (
                "⚠️ ANÁLISE DE PROMOÇÃO:\n"
                "- Score MAIS RIGOROSO: candidato busca nível hierárquico superior\n"
                "- Gaps devem incluir competências do PRÓXIMO NÍVEL (não apenas do cargo alvo)\n"
                "- Se cargo alvo é gerencial e candidato é individual contributor: "
                "gaps DEVEM incluir liderança, gestão de pessoas, budget, stakeholders\n"
                "- Se cargo alvo é direção e candidato é gerência: "
                "gaps DEVEM incluir visão estratégica, transformação organizacional, board-level communication\n"
                "- Peso MAIOR para competências de liderança e gestão estratégica\n\n"
            )
        elif objetivo == "Transição de Carreira" or "transição" in objetivo.lower():
            system_prompt += (
                "⚠️ ANÁLISE DE TRANSIÇÃO:\n"
                "- DESTAQUE transferable skills: habilidades que aplicam ao novo campo\n"
                "- Gaps são mais NUMEROSOS (mudança de área), mas tom deve ser CONSTRUTIVO\n"
                "- Mencione no plano_acao como experiências anteriores são VALIOSAS no novo contexto\n"
                "- Identifique certificações/cursos que facilitam a transição\n"
                "- Score: não penalize excessivamente a falta de experiência direta se há skills transferíveis\n\n"
            )
        elif objetivo == "Trabalho Internacional" or "internacional" in objetivo.lower():
            system_prompt += (
                "⚠️ ANÁLISE INTERNACIONAL:\n"
                "- Gaps DEVEM incluir requisitos internacionais:\n"
                "  * Fluência em idiomas (principalmente inglês avançado/fluente)\n"
                "  * Certificações globais relevantes (PMP, AWS, CFA, etc.)\n"
                "  * Experiência com times distribuídos/multiculturais\n"
                "  * Conhecimento de práticas internacionais da área\n"
                "- Considere diferenças culturais e de mercado\n"
                "- Mencione no plano_acao preparação específica para mercado global\n\n"
            )
        else:  # Recolocação ou outros
            system_prompt += (
                "⚠️ ANÁLISE DE RECOLOCAÇÃO:\n"
                "- Score PADRÃO: avaliar compatibilidade atual do CV com o cargo\n"
                "- Gaps devem refletir apenas skills técnicas faltantes para o cargo alvo\n"
                "- Tom equilibrado entre realista e encorajador\n\n"
            )
    
    system_prompt += (
        "REGRAS DE OURO:\n\n"
        "1. **Pontos Fortes**: Liste APENAS Hard Skills, Ferramentas (Software), Metodologias específicas e "
        "Métricas de Negócio que o candidato REALMENTE demonstra no CV.\n"
        "   - ✅ INCLUIR: ferramentas específicas, linguagens, frameworks, certificações, métricas\n"
        "   - ❌ NÃO INCLUIR: termos genéricos como 'gestão', 'vendas', 'liderança', 'comunicação', 'dados'\n\n"
        "2. **Gaps**: Liste APENAS Hard Skills, Ferramentas e Certificações RELEVANTES para o cargo.\n"
        "   - ✅ INCLUIR: Ferramentas específicas faltantes, certificações relevantes, tecnologias core\n"
        "   - ❌ NÃO INCLUIR: stopwords, verbos genéricos, erros de tradução, n-grams genéricos, "
        "ferramentas de outros arquétipos\n\n"
        "3. **Gaps Falsos Ignorados**: OBRIGATÓRIO - Liste skills que você CONSIDEROU mas DESCARTOU "
        "como gap (double-check/chain-of-thought). Justifique por que não são gaps válidos.\n\n"
        "⚠️ REGRA CRÍTICA PARA gaps_falsos_ignorados:\n"
        "- PROIBIDO mencionar SQL, Python ou Tableau como gaps falsos (esses eram exemplos antigos do sistema)\n"
        "- Analise o CV REAL do candidato e o cargo ESPECÍFICO\n"
        "- Liste skills que são REALMENTE relevantes para ESTE cargo e que você descartou com motivo REAL\n"
        "- Exemplo CORRETO para Head of Pricing: 'SAP APO (candidato usa outro ERP compatível)'\n"
        "- Exemplo CORRETO para Gerente de Vendas: 'Outreach (candidato já usa ferramenta similar de sales engagement)'\n"
        "- Cada item DEVE ser uma skill/ferramenta DIFERENTE das anteriores e ESPECÍFICA para o cargo\n\n"
        "4. **Score (0-100)**: Avalie considerando:\n"
        "   - Experiência Core (senioridade, anos): 50%\n"
        "   - Hard Skills Match (ferramentas): 20%\n"
        "   - Métricas quantificáveis: 20%\n"
        "   - Formatação ATS-friendly: 10%\n\n"
        "5. **Plano de Ação**: Dê 2-3 recomendações práticas e específicas, começando com emoji relevante.\n\n"
        "RESPONDA APENAS COM UM JSON VÁLIDO (sem markdown, sem explicações extras):\n"
        "```json\n"
        "{\n"
        '    "score": 65.0,\n'
        '    "arquetipo_cargo": "VENDAS",\n'
        '    "pontos_fortes": ["CRM Salesforce", "Pipeline Management", "métricas B2B"],\n'
        '    "gaps_identificados": ["<nome_ferramenta_especifica>", "<nome_metodologia_real>"],\n'
        '    "gaps_falsos_ignorados": ["<skill_REAL_descartada> (<motivo_real_específico>)", "<outra_skill_REAL> (<outro_motivo>)"],\n'
        '    "plano_acao": ["🔍 Palavras-chave ausentes...", "⚠️ Boa base, mas..."]\n'
        "}\n"
        "```\n\n"
        "⚠️ REGRA CRÍTICA: NUNCA use os valores de exemplo acima. "
        "Substitua TODOS os valores de exemplo (incluindo os entre < >) por ferramentas, "
        "metodologias e skills REAIS e específicas para o cargo sendo analisado. "
        "Os exemplos são apenas para ilustrar o formato JSON esperado."
    )
    
    if texto_vaga:
        user_prompt = (
            f"CARGO ALVO: {cargo_alvo}\n"
        )
        if cargo_atual:
            user_prompt += f"CARGO ATUAL: {cargo_atual}\n"
        if objetivo:
            user_prompt += f"OBJETIVO: {objetivo}\n"
        user_prompt += (
            f"\nTEXTO DA VAGA (FONTE DA VERDADE):\n{texto_vaga[:6000]}\n\n"
            f"CV DO CANDIDATO:\n{cv_texto[:8000]}\n\n"
            f"Analise o CV contra a vaga real e retorne o JSON."
        )
    else:
        user_prompt = (
            f"CARGO ALVO: {cargo_alvo}\n"
        )
        if cargo_atual:
            user_prompt += f"CARGO ATUAL: {cargo_atual}\n"
        if objetivo:
            user_prompt += f"OBJETIVO: {objetivo}\n"
        user_prompt += (
            f"\nCV DO CANDIDATO:\n{cv_texto[:8000]}\n\n"
            f"Analise este CV para o cargo '{cargo_alvo}', classifique o arquétipo, "
            f"e retorne o JSON conforme as regras."
        )
    
    msgs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Chamar LLM com temperatura baixa e seed fixo para consistência e reprodutibilidade
    resposta = chamar_gpt(client, msgs, temperature=0.2, seed=42)
    
    if not resposta:
        logger.warning("Falha ao obter resposta da LLM")
        return None
    
    # Parse do JSON da resposta
    try:
        # A resposta pode vir com blocos ```json ou JSON puro
        resposta_limpa = resposta.strip()
        
        # Remover blocos markdown se existirem
        if resposta_limpa.startswith("```json"):
            resposta_limpa = resposta_limpa.split("```json", 1)[1]
            resposta_limpa = resposta_limpa.rsplit("```", 1)[0]
        elif resposta_limpa.startswith("```"):
            resposta_limpa = resposta_limpa.split("```", 1)[1]
            resposta_limpa = resposta_limpa.rsplit("```", 1)[0]
        
        resposta_limpa = resposta_limpa.strip()
        
        # Parse do JSON
        resultado = json.loads(resposta_limpa)
        
        # Validar estrutura esperada (campos obrigatórios v5.0)
        campos_obrigatorios = ['score', 'pontos_fortes', 'gaps_identificados', 'plano_acao']
        if not all(k in resultado for k in campos_obrigatorios):
            logger.error("Resposta LLM não contém todas as chaves obrigatórias")
            return None
        
        # Validar tipos
        if not isinstance(resultado['score'], (int, float)):
            logger.error("Score não é numérico")
            return None
        if not isinstance(resultado['pontos_fortes'], list):
            logger.error("pontos_fortes não é lista")
            return None
        if not isinstance(resultado['gaps_identificados'], list):
            logger.error("gaps_identificados não é lista")
            return None
        if not isinstance(resultado['plano_acao'], list):
            logger.error("plano_acao não é lista")
            return None
        
        # Adicionar campos v5.0 com defaults se não existirem
        if 'arquetipo_cargo' not in resultado:
            resultado['arquetipo_cargo'] = 'N/A'
            logger.warning("LLM não retornou arquetipo_cargo, usando 'N/A'")
        
        if 'gaps_falsos_ignorados' not in resultado:
            resultado['gaps_falsos_ignorados'] = []
            logger.warning("LLM não retornou gaps_falsos_ignorados, usando lista vazia")
        
        # Post-processing: Filter out copied/paraphrased example values from gaps_falsos_ignorados
        gaps_falsos_originais = resultado['gaps_falsos_ignorados']
        gaps_falsos_filtrados = []
        
        # Palavras-chave dos exemplos antigos que a LLM tende a parafrasear
        # Filtrar qualquer item que comece com essas palavras (são os exemplos do prompt sendo copiados)
        _palavras_exemplo_antigo = ['tableau', 'python', 'sql']
        
        for gap_falso in gaps_falsos_originais:
            gap_lower = gap_falso.strip().lower()
            # Extrair a primeira palavra (nome da skill) antes do parêntese
            words_before_paren = gap_lower.split('(')[0].strip().split()
            skill_name = words_before_paren[0] if words_before_paren else ''
            
            if skill_name in _palavras_exemplo_antigo:
                logger.warning(f"Exemplo parafraseado filtrado de gaps_falsos_ignorados: {gap_falso}")
            else:
                gaps_falsos_filtrados.append(gap_falso)
        
        resultado['gaps_falsos_ignorados'] = gaps_falsos_filtrados
        
        # Post-processing: Filter out placeholder gap names
        gaps_originais = resultado['gaps_identificados']
        placeholder_patterns = [
            'ferramenta_especifica', 'metodologia_', '<nome_', 
            'exemplo_', 'placeholder', 'ferramenta_1', 'ferramenta_2',
            'metodologia_1', 'metodologia_2', 'skill_'
        ]
        
        gaps_filtrados = []
        for gap in gaps_originais:
            gap_lower = gap.lower()
            # Check if gap contains any placeholder pattern
            is_placeholder = any(pattern in gap_lower for pattern in placeholder_patterns)
            if not is_placeholder:
                gaps_filtrados.append(gap)
            else:
                logger.warning(f"Removido gap placeholder detectado: {gap}")
        
        resultado['gaps_identificados'] = gaps_filtrados
        
        if len(gaps_filtrados) < len(gaps_originais):
            logger.info(
                f"Post-processing: {len(gaps_originais) - len(gaps_filtrados)} "
                f"gaps placeholders removidos"
            )
        
        # Adicionar fonte da análise
        resultado['fonte_vaga'] = fonte
        
        logger.info(
            f"Análise LLM v5.0 concluída. Score: {resultado['score']}, "
            f"Arquétipo: {resultado['arquetipo_cargo']}, Fonte: {fonte}"
        )
        return resultado
        
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao fazer parse do JSON da LLM: {e}")
        logger.debug(f"Resposta recebida: {resposta[:500]}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao processar resposta da LLM: {e}", exc_info=True)
        return None


def buscar_variacoes_cargo(client, cargo: str) -> List[str]:
    """
    Usa IA para encontrar variações REAIS de mercado de um cargo.
    """
    logger.info(f"Buscando variações de mercado para: {cargo}")
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento no Brasil e mercado de trabalho. "
            "Dado um cargo, liste entre 5 e 8 variações REAIS desse cargo como aparecem "
            "em vagas publicadas no LinkedIn, Gupy, Catho e Indeed. "
            "Inclua variações em português E inglês que recrutadores REALMENTE usam. "
            "Mantenha o mesmo nível hierárquico (se é gerente, liste cargos de gerência). "
            "NÃO invente cargos — liste apenas os que EXISTEM no mercado real. "
            "Responda APENAS com a lista, um cargo por linha, sem numeração nem explicação."
        )},
        {"role": "user", "content": f"Cargo: {cargo}"}
    ]
    
    resposta = chamar_gpt(client, msgs, temperature=0.3, seed=42)
    
    if not resposta:
        logger.warning("Falha ao buscar variações — usando cargo original")
        return [cargo]
    
    variacoes = [v.strip() for v in resposta.strip().split('\n') if v.strip()]
    if cargo not in variacoes:
        variacoes.insert(0, cargo)
    
    logger.info(f"Variações encontradas: {variacoes}")
    return variacoes


def gerar_job_description(client, cargo: str) -> Optional[str]:
    """
    Gera uma Job Description focada em TERMOS TÉCNICOS reais do cargo,
    sem exemplos genéricos que contaminam a análise.
    """
    logger.info(f"Gerando Job Description técnica para: {cargo}")
    
    variacoes = buscar_variacoes_cargo(client, cargo)
    variacoes_texto = "\n".join(f"- {v}" for v in variacoes)
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento técnico e sistemas ATS no Brasil.\n\n"
            "Gere uma Job Description para o cargo informado focada EXCLUSIVAMENTE em:\n"
            "- Ferramentas e softwares ESPECÍFICOS da área desse cargo\n"
            "- Metodologias e frameworks REALMENTE usados nesse cargo\n"
            "- Siglas e termos técnicos ESPECÍFICOS dessa função\n"
            "- Certificações relevantes APENAS para esse cargo\n"
            "- Tecnologias REALMENTE exigidas nessa função\n"
            "- Conceitos técnicos ESPECÍFICOS dessa área\n\n"
            "REGRAS CRÍTICAS:\n"
            "- NÃO inclua termos genéricos de outras áreas\n"
            "- NÃO use exemplos que não sejam da área do cargo\n"
            "- NÃO inclua ferramentas/metodologias irrelevantes para a função\n"
            "- Cada termo mencionado deve ser algo que um recrutador REALMENTE "
            "buscaria ao filtrar candidatos para ESSE cargo específico\n"
            "- NÃO use verbos genéricos como 'desenvolver', 'gerenciar', 'implementar'\n"
            "- NÃO use frases genéricas como 'trabalho em equipe', 'boa comunicação'\n\n"
            "A JD deve cobrir o cargo principal E suas variações de mercado.\n"
            "Inclua termos em português E inglês.\n"
            "Responda APENAS com a Job Description, sem introdução."
        )},
        {"role": "user", "content": (
            f"Cargo principal: {cargo}\n\n"
            f"Variações de mercado:\n{variacoes_texto}\n\n"
            f"Gere a Job Description TÉCNICA cobrindo APENAS termos relevantes "
            f"para esse cargo específico e suas variações."
        )}
    ]
    
    jd = chamar_gpt(client, msgs, temperature=0.3, seed=42)
    
    if jd:
        logger.info(f"JD técnica gerada ({len(jd)} chars)")
    else:
        logger.error("Falha ao gerar JD")
    
    return jd


def _gerar_breakdown_tfidf(cv_texto: str, cargo_alvo: str, client) -> Dict:
    """
    Gera breakdown detalhado usando TF-IDF para complementar análise LLM.
    
    Roda silenciosamente para popular campos que a UI espera, mesmo quando
    a análise principal vem da LLM.
    
    Args:
        cv_texto: Texto do CV
        cargo_alvo: Cargo alvo
        client: Cliente OpenAI (para gerar JD se necessário)
        
    Returns:
        Dict com detalhes do breakdown ou estrutura vazia com campos presentes
    """
    try:
        # Tentar gerar JD e rodar TF-IDF
        jd = gerar_job_description(client, cargo_alvo) if client else None
        
        if jd:
            analise = _analisar_compatibilidade(cv_texto, jd)
            # Retornar estrutura com dados reais do TF-IDF
            return {
                'metodo': 'LLM Score + TF-IDF Breakdown',
                'modelo': 'GPT-4o + TF-IDF',
                'fallback': False,
                'secoes': {'score': 75, 'encontradas': 4, 'total': 5},  # Estimado
                'keywords': {
                    'score': 80, 
                    'encontradas': len(analise.get('pontos_fortes', [])),
                    'total': len(analise.get('pontos_fortes', [])) + len(analise.get('gaps_identificados', [])),
                    'faltando': analise.get('gaps_identificados', [])[:5]
                },
                'metricas': {'score': 70, 'quantidade': cv_texto.count('%') + cv_texto.count('R$')},
                'formatacao': {
                    'score': 85, 
                    'bullets': cv_texto.count('•') + cv_texto.count('-'),
                    'datas': cv_texto.count('20')  # Anos aproximados
                },
                'tamanho': {
                    'score': 80, 
                    'palavras': len(cv_texto.split()),
                    'ideal': '400-600'
                },
            }
    except Exception as e:
        logger.warning(f"Falha ao gerar breakdown TF-IDF: {e}")
    
    # Fallback: estrutura vazia mas com campos presentes (UI não crasha)
    return {
        'metodo': 'LLM Only (breakdown não disponível)',
        'modelo': 'GPT-4o',
        'fallback': False,
        'secoes': {'score': 0, 'encontradas': 0, 'total': 0},
        'keywords': {'score': 0, 'encontradas': 0, 'total': 0, 'faltando': []},
        'metricas': {'score': 0, 'quantidade': 0},
        'formatacao': {'score': 0, 'bullets': 0, 'datas': 0},
        'tamanho': {'score': 0, 'palavras': 0, 'ideal': 'N/A'},
    }


def extrair_cargo_do_cv(client, cv_texto: str) -> Optional[str]:
    """
    Extrai o cargo atual/mais recente do candidato a partir do CV.
    """
    logger.info("Extraindo cargo atual do CV")
    
    msgs = [
        {"role": "system", "content": (
            "Analise o CV abaixo e identifique o cargo ATUAL ou MAIS RECENTE do candidato. "
            "Responda APENAS com o nome do cargo, nada mais. "
            "Exemplo de resposta: Gerente de Vendas"
        )},
        {"role": "user", "content": f"CV:\n{cv_texto[:3000]}"}
    ]
    
    cargo = chamar_gpt(client, msgs, temperature=0.1, seed=42)
    
    if cargo:
        cargo = cargo.strip().strip('"').strip("'")
        logger.info(f"Cargo extraído: {cargo}")
    else:
        logger.error("Falha ao extrair cargo do CV")
    
    return cargo


def calcular_score_ats(
    cv_texto: str, 
    cargo_alvo: str, 
    client=None,
    texto_vaga: Optional[str] = None,
    objetivo: Optional[str] = None,
    cargo_atual: Optional[str] = None
) -> Dict:
    """
    Calcula Score ATS completo com análise de gaps técnicos.
    
    v5.0: Arquitetura Híbrida com 3 cenários:
    - Cenário A: Vaga real fornecida (texto_vaga != None)
    - Cenário B: Título + arquétipo + double-check (client != None)
    - Cenário C: Fallback TF-IDF offline
    
    Args:
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para gerar a Job Description ou classificar
        client: Cliente OpenAI (opcional, mas recomendado para análise LLM)
        texto_vaga: Texto da vaga real (opcional) para análise ultra-precisa
        objetivo: Tipo de movimentação (Recolocação, Transição, Promoção Interna, Trabalho Internacional)
        cargo_atual: Cargo atual do candidato (opcional)
        
    Returns:
        Dict com score_total, percentual, nivel, pontos_fortes,
        gaps_identificados, gaps_falsos_ignorados, plano_acao, 
        arquetipo_cargo, fonte_vaga, metodo e detalhes
    """
    logger.info(f"Calculando score ATS v5.0 para cargo: {cargo_alvo}, objetivo: {objetivo}")
    
    # ─── TENTATIVA 1: Análise LLM (v5.0) ───
    if client:
        logger.info("Client OpenAI disponível - usando análise LLM (v5.0)")
        analise_llm = _analisar_com_llm(client, cv_texto, cargo_alvo, texto_vaga, objetivo, cargo_atual)
        
        if analise_llm:
            # Usar resultado da LLM
            score = analise_llm['score']
            nivel = classificar_score(score)
            
            fonte_vaga = analise_llm.get('fonte_vaga', 'arquetipo')
            arquetipo = analise_llm.get('arquetipo_cargo', 'N/A')
            
            logger.info(
                f"Análise LLM bem-sucedida. Score: {score}/100 ({nivel}), "
                f"Arquétipo: {arquetipo}, Fonte: {fonte_vaga}"
            )
            
            # Tentar rodar TF-IDF silenciosamente para gerar breakdown detalhado
            detalhes_breakdown = _gerar_breakdown_tfidf(cv_texto, cargo_alvo, client)
            
            return {
                'score_total': score,
                'max_score': 100,
                'percentual': score,
                'nivel': nivel,
                'cargo_avaliado': cargo_alvo,
                'pontos_fortes': analise_llm['pontos_fortes'],
                'gaps_identificados': analise_llm['gaps_identificados'],
                'gaps_falsos_ignorados': analise_llm.get('gaps_falsos_ignorados', []),
                'plano_acao': analise_llm['plano_acao'],
                'arquetipo_cargo': arquetipo,
                'fonte_vaga': fonte_vaga,
                'jd_gerada': texto_vaga is not None or True,
                'metodo': 'LLM + TF-IDF Validation (v5.0)',
                'detalhes': detalhes_breakdown
            }
        else:
            logger.warning("Análise LLM falhou - caindo para fallback TF-IDF")
    else:
        logger.info("Client OpenAI não disponível - usando fallback TF-IDF (v3.2)")
    
    # ─── FALLBACK: Análise TF-IDF (v3.2) ───
    job_description = None
    if client:
        job_description = gerar_job_description(client, cargo_alvo)
    
    if not job_description:
        logger.warning("Usando JD simplificada")
        job_description = (
            f"Vaga para {cargo_alvo}. "
            f"Requisitos: experiência na área, habilidades técnicas relevantes, "
            f"capacidade de trabalho em equipe, boa comunicação, "
            f"resultados mensuráveis, gestão de projetos, liderança, "
            f"análise de dados, planejamento estratégico."
        )
    
    analise = _analisar_compatibilidade(cv_texto, job_description)
    
    score = analise['score']
    nivel = classificar_score(score)
    
    resultado = {
        'score_total': score,
        'max_score': 100,
        'percentual': score,
        'nivel': nivel,
        'cargo_avaliado': cargo_alvo,
        'pontos_fortes': analise['pontos_fortes'],
        'gaps_identificados': analise['gaps_identificados'],
        'gaps_falsos_ignorados': [],  # v5.0: não disponível no fallback
        'plano_acao': analise['plano_acao'],
        'arquetipo_cargo': 'N/A',  # v5.0: não disponível no fallback
        'fonte_vaga': 'tfidf_fallback',  # v5.0: fonte do fallback
        'jd_gerada': job_description is not None,
        'metodo': 'TF-IDF (v3.2 fallback)',  # v5.0: método usado
        'detalhes': {
            'metodo': 'TF-IDF + Cosine Similarity (v3.2 - Fallback)',
            'ngrams': '1-3',
            'stopwords': 'NLTK (PT + EN) + Custom CV/JD (~550+)',
            'fallback': True,
        }
    }
    
    logger.info(f"Score ATS: {score}/100 ({nivel})")
    return resultado


def classificar_score(score: float) -> str:
    """Classifica o score ATS em níveis qualitativos."""
    if score >= 70:
        return "Excelente"
    elif score >= 50:
        return "Bom"
    elif score >= 30:
        return "Regular"
    else:
        return "Precisa Melhorar"
