"""
Sistema de Pontuação ATS (Applicant Tracking System).

Este módulo simula como sistemas automatizados de recrutamento avaliam currículos,
fornecendo pontuação detalhada e recomendações de melhoria.
"""

import re
import logging
from typing import Dict, List

# Configurar logger
logger = logging.getLogger(__name__)


def calcular_score_ats(cv_texto: str, cargo_alvo: str) -> Dict:
    """
    Simula score de ATS (Applicant Tracking System).
    
    Analisa o currículo em 5 dimensões principais:
    1. Presença de seções essenciais (20 pontos)
    2. Densidade de palavras-chave relevantes (30 pontos)
    3. Métricas quantificáveis (20 pontos)
    4. Formatação adequada (15 pontos)
    5. Tamanho apropriado (15 pontos)
    
    Args:
        cv_texto: Texto completo do currículo
        cargo_alvo: Cargo desejado para otimização de keywords
    
    Returns:
        Dict com score total, breakdown detalhado e recomendações
        
    Examples:
        >>> resultado = calcular_score_ats("CV texto...", "Gerente de Projetos")
        >>> print(resultado['score_total'])
        75.5
    """
    logger.info(f"Iniciando cálculo de score ATS para cargo: {cargo_alvo}")
    
    score = 0
    max_score = 100
    detalhes = {}
    
    # 1. Presença de seções essenciais (20 pontos)
    secoes_encontradas = 0
    secoes = {
        'experiência': r'(experiência|professional experience|trabalho|exp\.)',
        'educação': r'(educação|formação|education|academic)',
        'habilidades': r'(habilidades|skills|competências|conhecimentos)',
        'contato': r'(email|telefone|linkedin|phone|celular)'
    }
    
    for nome, pattern in secoes.items():
        if re.search(pattern, cv_texto, re.IGNORECASE):
            secoes_encontradas += 1
            logger.debug(f"Seção '{nome}' encontrada")
    
    score_secoes = (secoes_encontradas / len(secoes)) * 20
    score += score_secoes
    detalhes['secoes'] = {
        'score': score_secoes,
        'encontradas': secoes_encontradas,
        'total': len(secoes)
    }
    
    # 2. Densidade de palavras-chave (30 pontos)
    keywords_cargo = extrair_keywords_cargo(cargo_alvo)
    keywords_encontradas = sum(1 for kw in keywords_cargo if kw.lower() in cv_texto.lower())
    
    score_keywords = (keywords_encontradas / max(len(keywords_cargo), 1)) * 30
    score += score_keywords
    detalhes['keywords'] = {
        'score': score_keywords,
        'encontradas': keywords_encontradas,
        'total': len(keywords_cargo),
        'faltando': [kw for kw in keywords_cargo if kw.lower() not in cv_texto.lower()][:5]
    }
    logger.debug(f"Keywords: {keywords_encontradas}/{len(keywords_cargo)} encontradas")
    
    # 3. Métricas quantificáveis (20 pontos)
    numeros = re.findall(r'\d+[%]?', cv_texto)
    score_metricas = min(len(numeros) / 10, 1) * 20  # Máximo com 10+ números
    score += score_metricas
    detalhes['metricas'] = {
        'score': score_metricas,
        'quantidade': len(numeros)
    }
    logger.debug(f"Métricas: {len(numeros)} números encontrados")
    
    # 4. Formatação (15 pontos)
    # Verifica bullets, datas, consistência
    bullets = len(re.findall(r'^[\•\-\*]', cv_texto, re.MULTILINE))
    datas = len(re.findall(r'\b(19|20)\d{2}\b', cv_texto))
    
    score_formatacao = min((bullets / 10 + datas / 5) / 2, 1) * 15
    score += score_formatacao
    detalhes['formatacao'] = {
        'score': score_formatacao,
        'bullets': bullets,
        'datas': datas
    }
    logger.debug(f"Formatação: {bullets} bullets, {datas} datas")
    
    # 5. Tamanho adequado (15 pontos)
    palavras = len(cv_texto.split())
    if 300 <= palavras <= 800:  # Ideal
        score_tamanho = 15
    elif 200 <= palavras < 300 or 800 < palavras <= 1200:
        score_tamanho = 10
    else:
        score_tamanho = 5
    
    score += score_tamanho
    detalhes['tamanho'] = {
        'score': score_tamanho,
        'palavras': palavras,
        'ideal': '300-800 palavras'
    }
    logger.debug(f"Tamanho: {palavras} palavras")
    
    resultado = {
        'score_total': round(score, 1),
        'max_score': max_score,
        'percentual': round((score / max_score) * 100, 1),
        'nivel': classificar_score(score),
        'detalhes': detalhes
    }
    
    logger.info(f"Score ATS calculado: {resultado['score_total']}/{max_score} ({resultado['percentual']}%)")
    return resultado


def extrair_keywords_cargo(cargo: str) -> List[str]:
    """
    Extrai keywords típicas de um cargo.
    
    Mapeia diferentes áreas profissionais para suas palavras-chave características.
    
    Args:
        cargo: Nome do cargo alvo
        
    Returns:
        Lista de palavras-chave relevantes para o cargo
        
    Examples:
        >>> keywords = extrair_keywords_cargo("Gerente de Vendas")
        >>> 'CRM' in keywords
        True
    """
    keywords_por_area = {
        'gerente': ['gestão', 'equipe', 'liderança', 'planejamento', 'estratégia', 'budget', 'KPI'],
        'vendas': ['pipeline', 'CRM', 'negociação', 'prospecção', 'quota', 'vendas', 'clientes'],
        'marketing': ['campanhas', 'digital', 'SEO', 'analytics', 'social media', 'branding'],
        'tech': ['desenvolvimento', 'código', 'API', 'database', 'cloud', 'CI/CD'],
        'desenvolv': ['desenvolvimento', 'código', 'API', 'database', 'cloud', 'CI/CD', 'git'],
        'engenheiro': ['desenvolvimento', 'código', 'API', 'database', 'cloud', 'CI/CD', 'arquitetura'],
        'rh': ['recrutamento', 'seleção', 'cultura', 'people', 'onboarding', 'performance'],
        'recursos humanos': ['recrutamento', 'seleção', 'cultura', 'people', 'onboarding', 'performance'],
        'financ': ['finanças', 'orçamento', 'forecast', 'análise', 'custos', 'ROI'],
        'produto': ['roadmap', 'backlog', 'stakeholders', 'MVP', 'métricas', 'produto'],
        'product': ['roadmap', 'backlog', 'stakeholders', 'MVP', 'métricas', 'produto'],
        'designer': ['UI', 'UX', 'prototipagem', 'design', 'figma', 'usuário'],
        'analista': ['análise', 'dados', 'relatórios', 'métricas', 'dashboard', 'insights']
    }
    
    cargo_lower = cargo.lower()
    keywords = []
    
    # Busca por palavras-chave da área
    for area, kws in keywords_por_area.items():
        if area in cargo_lower:
            keywords.extend(kws)
            break  # Usa apenas a primeira correspondência para evitar duplicatas
    
    # Se não encontrou área específica, usa keywords genéricas
    if not keywords:
        keywords = ['gestão', 'resultados', 'equipe', 'projetos', 'estratégia', 'planejamento']
    
    logger.debug(f"Keywords extraídas para '{cargo}': {keywords}")
    return keywords


def classificar_score(score: float) -> str:
    """
    Classifica o score ATS em níveis qualitativos.
    
    Args:
        score: Pontuação total (0-100)
        
    Returns:
        Classificação textual do score
        
    Examples:
        >>> classificar_score(85)
        'Excelente'
        >>> classificar_score(45)
        'Regular'
    """
    if score >= 80:
        return "Excelente"
    elif score >= 60:
        return "Bom"
    elif score >= 40:
        return "Regular"
    else:
        return "Precisa Melhorar"
