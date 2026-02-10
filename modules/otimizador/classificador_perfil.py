"""
Classificador de Senioridade e Estratégia Dinâmica - Headhunter Elite

Analisa CV e cargo para classificar senioridade e definir estratégia de perguntas.
"""

import re
from modules.otimizador.market_knowledge import detectar_area_por_cargo


def classificar_senioridade_e_estrategia(cv_texto: str, cargo: str) -> dict:
    """
    Analisa CV e cargo para classificar senioridade e definir estratégia de perguntas.
    
    Args:
        cv_texto: Texto completo do CV
        cargo: Cargo-alvo do candidato
        
    Returns:
        dict: {
            'senioridade': 'junior'|'pleno'|'senior'|'executivo',
            'foco_metricas': list,  # Tipos de métricas a buscar
            'modo_interrogatorio': 'operacional'|'estrategico'|'executivo',
            'template_pergunta': str,  # Template de pergunta para essa senioridade
            'area_profissional': str
        }
    """
    if not cargo:
        cargo = ""
    
    if not cv_texto:
        cv_texto = ""
    
    cargo_lower = cargo.lower()
    cv_lower = cv_texto.lower()
    
    # Detectar área profissional
    area_profissional = detectar_area_por_cargo(cargo)
    
    # === CLASSIFICAÇÃO DE SENIORIDADE ===
    
    # 1. EXECUTIVO (mais alto nível)
    executivo_keywords = [
        'ceo', 'cto', 'cfo', 'coo', 'cmo', 'chro', 'cpo', 'ciso',
        'diretor', 'diretora', 'vp', 'vice president', 'vice-president',
        'head of', 'head ', 'c-level', 'presidente', 'country manager'
    ]
    
    # 2. SENIOR (liderança técnica/coordenação)
    senior_keywords = [
        'senior', 'sênior', 'sr.', 'sr ', 'coordenador', 'coordenadora',
        'tech lead', 'lead ', 'principal', 'staff', 'especialista sênior',
        'especialista sr', 'gerente', 'manager'
    ]
    
    # 3. JUNIOR (iniciante)
    junior_keywords = [
        'junior', 'júnior', 'jr.', 'jr ', 'estagiário', 'estagiaria',
        'trainee', 'assistente', 'auxiliar', 'aprendiz'
    ]
    
    # 4. PLENO (default - nível intermediário)
    pleno_keywords = [
        'pleno', 'analista', 'especialista', 'consultor', 'consultora',
        'engenheiro', 'engenheira', 'desenvolvedor', 'desenvolvedora'
    ]
    
    # Classificar baseado no cargo primeiro
    senioridade = 'pleno'  # Default
    
    if any(keyword in cargo_lower for keyword in executivo_keywords):
        senioridade = 'executivo'
    elif any(keyword in cargo_lower for keyword in senior_keywords):
        senioridade = 'senior'
    elif any(keyword in cargo_lower for keyword in junior_keywords):
        senioridade = 'junior'
    elif any(keyword in cargo_lower for keyword in pleno_keywords):
        senioridade = 'pleno'
    
    # Ajustar baseado em evidências no CV (se classificação não foi executivo)
    if senioridade != 'executivo':
        # Evidências de nível executivo no CV
        evidencias_executivo = [
            r'budget.*\d+.*milhões?',
            r'budget.*\d+.*million',
            r'equipe.*\d{2,}',  # Gerenciou 10+ pessoas
            r'time.*\d{2,}',
            r'p&l',
            r'ebitda',
            r'receita.*\d+.*milhões?',
            r'revenue.*\d+.*million'
        ]
        
        if any(re.search(pattern, cv_lower) for pattern in evidencias_executivo):
            senioridade = 'executivo'
        
        # Evidências de senior
        elif senioridade != 'senior':
            evidencias_senior = [
                r'lider.*técnic',
                r'mentoria',
                r'arquitetura',
                r'coordena',
                r'equipe.*\d+',  # Gerenciou equipe com número
                r'time.*\d+'
            ]
            
            if any(re.search(pattern, cv_lower) for pattern in evidencias_senior):
                senioridade = 'senior'
    
    # === DEFINIR ESTRATÉGIA POR SENIORIDADE ===
    
    if senioridade == 'junior':
        foco_metricas = [
            'volume processado',
            'frequência de execução',
            'tarefas completadas',
            'ferramentas utilizadas',
            'eficiência pessoal',
            'tempo de resposta'
        ]
        modo_interrogatorio = 'operacional'
        template_pergunta = (
            "Me conta: quantas {tarefa} você {acao} por {periodo}? "
            "Quais ferramentas específicas você usava no dia a dia?"
        )
    
    elif senioridade == 'pleno':
        foco_metricas = [
            'projetos entregues',
            'otimizações implementadas',
            'iniciativas lideradas',
            'melhorias de processo',
            'resultados de qualidade',
            'impacto em métricas'
        ]
        modo_interrogatorio = 'estrategico'
        template_pergunta = (
            "Me descreve: qual foi o projeto mais importante que você liderou? "
            "Que resultado mensurável você atingiu? Qual ferramenta usou?"
        )
    
    elif senioridade == 'senior':
        foco_metricas = [
            'arquiteturas desenhadas',
            'times liderados (tamanho)',
            'mentorias realizadas',
            'decisões técnicas/estratégicas',
            'transformações conduzidas',
            'impacto no negócio'
        ]
        modo_interrogatorio = 'estrategico'
        template_pergunta = (
            "Me detalha: qual arquitetura/estratégia você definiu? "
            "Quantas pessoas você liderou/mentorou? "
            "Qual foi o impacto no negócio (%, R$)?"
        )
    
    else:  # executivo
        foco_metricas = [
            'P&L gerenciado (R$/US$)',
            'budget sob responsabilidade',
            'crescimento de receita (%)',
            'transformação organizacional',
            'tamanho de equipe',
            'EBITDA / margem',
            'métricas estratégicas (NRR, CAC, LTV)'
        ]
        modo_interrogatorio = 'executivo'
        template_pergunta = (
            "Me conta: qual era o P&L sob sua responsabilidade? "
            "Quantas pessoas você gerenciava? "
            "Qual crescimento/transformação você entregou? "
            "Quais foram as métricas estratégicas impactadas?"
        )
    
    return {
        'senioridade': senioridade,
        'foco_metricas': foco_metricas,
        'modo_interrogatorio': modo_interrogatorio,
        'template_pergunta': template_pergunta,
        'area_profissional': area_profissional
    }
