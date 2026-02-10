"""
Analisador de Bullets - Detector de Verbos Fracos e Análise Sintática

Detecta bullets com verbos fracos e/ou falta de métricas no CV.
"""

import re
from modules.otimizador.market_knowledge import obter_conhecimento_mercado


# Lista de verbos fracos que devem ser evitados em CVs profissionais
VERBOS_FRACOS = [
    'ajudei', 'ajudava', 'ajudar',
    'auxiliei', 'auxiliava', 'auxiliar',
    'participei', 'participava', 'participar',
    'colaborei', 'colaborava', 'colaborar',
    'apoiei', 'apoiava', 'apoiar',
    'contribuí', 'contribuía',  # Pode ser fraco dependendo do contexto
    'responsável por', 'responsável pela', 'responsável pelo',
    'encarregado de', 'encarregado da', 'encarregado do',
    'fazia', 'fazer',
    'realizava', 'realizar',
    'atuava', 'atuar',
    'trabalhava com', 'trabalhar com',
    'lidava com', 'lidar com',
    'estive envolvido', 'estava envolvido',
    'tive contato', 'tinha contato',
    'fui parte', 'era parte',
]


def analisar_bullets_fracos(cv_texto: str, area: str, senioridade: str) -> list:
    """
    Detecta bullets com verbos fracos e/ou falta de métricas.
    
    Args:
        cv_texto: Texto completo do CV
        area: Área profissional (ex: 'Software Engineer')
        senioridade: Nível de senioridade ('junior', 'pleno', 'senior', 'executivo')
        
    Returns:
        list: Lista de dicionários com bullets problemáticos:
        [
            {
                'bullet_original': str,
                'problemas': list,  # ['Verbo fraco: ajudei', 'Falta métrica']
                'pergunta_direcionada': str,
                'metricas_esperadas': list
            }
        ]
    """
    if not cv_texto:
        return []
    
    # Obter conhecimento de mercado para a área
    conhecimento = obter_conhecimento_mercado(area)
    metricas_area = conhecimento.get('metrics', [])
    ferramentas_area = conhecimento.get('ferramentas', [])
    
    # Extrair bullets do CV (linhas que começam com • ou - ou *)
    bullets_pattern = r'^[\s]*[•\-\*]\s*(.+)$'
    bullets = []
    
    for line in cv_texto.split('\n'):
        match = re.match(bullets_pattern, line.strip())
        if match:
            bullets.append(match.group(1).strip())
    
    # Se não encontrou bullets com marcadores, tentar extrair por contexto
    # (frases curtas que parecem descrições de experiência)
    if not bullets:
        # Tentar identificar experiências por padrões comuns
        for line in cv_texto.split('\n'):
            line = line.strip()
            # Linhas que começam com verbo no passado ou presente
            if re.match(r'^[A-Z][a-zá-ú]+ei\s', line) or re.match(r'^[A-Z][a-zá-ú]+o\s', line):
                if len(line) > 20:  # Evitar linhas muito curtas
                    bullets.append(line)
    
    # Analisar cada bullet
    bullets_fracos = []
    
    for bullet in bullets:
        problemas = []
        bullet_lower = bullet.lower()
        
        # 1. Detectar verbos fracos
        verbo_fraco_encontrado = None
        for verbo in VERBOS_FRACOS:
            if verbo in bullet_lower:
                verbo_fraco_encontrado = verbo
                problemas.append(f"Verbo fraco: '{verbo}'")
                break
        
        # 2. Detectar falta de métricas (números)
        tem_numero = bool(re.search(r'\d+', bullet))
        if not tem_numero:
            problemas.append("Falta métrica quantificável")
        
        # 3. Detectar falta de ferramentas/tecnologias específicas
        tem_ferramenta = False
        for ferramenta in ferramentas_area:
            if ferramenta.lower() in bullet_lower:
                tem_ferramenta = True
                break
        
        if not tem_ferramenta and area != 'Generalista':
            problemas.append("Falta menção a ferramenta/tecnologia específica")
        
        # Se há problemas, adicionar à lista
        if problemas:
            # Gerar pergunta direcionada baseada em senioridade e área
            pergunta = _gerar_pergunta_direcionada(
                bullet, 
                problemas, 
                area, 
                senioridade,
                metricas_area
            )
            
            bullets_fracos.append({
                'bullet_original': bullet,
                'problemas': problemas,
                'pergunta_direcionada': pergunta,
                'metricas_esperadas': metricas_area[:3]  # Top 3 métricas esperadas
            })
    
    return bullets_fracos


def _gerar_pergunta_direcionada(bullet: str, problemas: list, area: str, 
                                 senioridade: str, metricas_area: list) -> str:
    """
    Gera pergunta personalizada para coletar informações faltantes do bullet.
    
    Args:
        bullet: Texto original do bullet
        problemas: Lista de problemas identificados
        area: Área profissional
        senioridade: Nível de senioridade
        metricas_area: Métricas esperadas para a área
        
    Returns:
        str: Pergunta direcionada para melhorar o bullet
    """
    # Extrair contexto do bullet (primeiros 50 caracteres)
    contexto = bullet[:50] + '...' if len(bullet) > 50 else bullet
    
    pergunta_base = f"Sobre '{contexto}': "
    
    # Adicionar perguntas específicas baseadas nos problemas
    perguntas_especificas = []
    
    if any('Verbo fraco' in p for p in problemas):
        if senioridade == 'executivo':
            perguntas_especificas.append(
                "Qual foi o resultado estratégico que VOCÊ liderou/implementou/transformou?"
            )
        elif senioridade == 'senior':
            perguntas_especificas.append(
                "Qual arquitetura/solução VOCÊ estruturou/implementou/otimizou?"
            )
        elif senioridade == 'pleno':
            perguntas_especificas.append(
                "Qual projeto/iniciativa VOCÊ executou/desenvolveu/entregou?"
            )
        else:  # junior
            perguntas_especificas.append(
                "Qual tarefa/atividade VOCÊ realizou/processou/executou?"
            )
    
    if any('Falta métrica' in p for p in problemas):
        if metricas_area:
            exemplo_metrica = metricas_area[0] if metricas_area else 'resultado'
            perguntas_especificas.append(
                f"Qual foi o resultado mensurável? (ex: {exemplo_metrica})"
            )
        else:
            perguntas_especificas.append(
                "Qual foi o resultado mensurável? (%, R$, quantidade, tempo?)"
            )
    
    if any('Falta menção a ferramenta' in p for p in problemas):
        conhecimento = obter_conhecimento_mercado(area)
        ferramentas = conhecimento.get('ferramentas', [])
        if ferramentas:
            exemplo_ferramentas = ', '.join(ferramentas[:3])
            perguntas_especificas.append(
                f"Quais ferramentas específicas você usou? (ex: {exemplo_ferramentas})"
            )
        else:
            perguntas_especificas.append(
                "Quais ferramentas/tecnologias específicas você usou?"
            )
    
    # Montar pergunta completa
    if perguntas_especificas:
        pergunta_completa = pergunta_base + " | ".join(perguntas_especificas)
    else:
        pergunta_completa = pergunta_base + "Me dê mais detalhes sobre essa experiência."
    
    return pergunta_completa


def extrair_bullets_cv(cv_texto: str) -> list:
    """
    Extrai todos os bullets/linhas de experiência do CV.
    
    Args:
        cv_texto: Texto completo do CV
        
    Returns:
        list: Lista de strings com os bullets encontrados
    """
    if not cv_texto:
        return []
    
    bullets = []
    
    # Padrão 1: Linhas com marcadores (•, -, *)
    bullets_pattern = r'^[\s]*[•\-\*]\s*(.+)$'
    
    for line in cv_texto.split('\n'):
        match = re.match(bullets_pattern, line.strip())
        if match:
            bullet_text = match.group(1).strip()
            if len(bullet_text) > 10:  # Ignorar bullets muito curtos
                bullets.append(bullet_text)
    
    # Padrão 2: Se não achou bullets com marcadores, 
    # tentar linhas que começam com verbo no passado
    if not bullets:
        for line in cv_texto.split('\n'):
            line = line.strip()
            # Verbos no passado (terminam em -ei, -ou, -iu, etc)
            if re.match(r'^[A-ZÀ-Ú][a-zà-ú]+[ei|ou|iu]\s', line):
                if len(line) > 20:
                    bullets.append(line)
    
    return bullets


def contar_bullets_fracos(cv_texto: str, area: str, senioridade: str) -> int:
    """
    Conta quantos bullets fracos existem no CV.
    
    Args:
        cv_texto: Texto completo do CV
        area: Área profissional
        senioridade: Nível de senioridade
        
    Returns:
        int: Quantidade de bullets com problemas
    """
    bullets_fracos = analisar_bullets_fracos(cv_texto, area, senioridade)
    return len(bullets_fracos)
