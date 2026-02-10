"""
Engenheiro de Texto - Templates STAR

Gera bullets otimizados usando método STAR (Situation, Task, Action, Result)
personalizados por senioridade e área profissional.
"""

# Mapeamento de verbos fracos → verbos fortes
VERBOS_UPGRADE = {
    # Verbos passivos/fracos → Verbos de ação forte
    'ajudei': 'Contribuí',
    'ajudava': 'Contribuí',
    'auxiliei': 'Apoiei',
    'auxiliava': 'Apoiei',
    'participei': 'Executei',
    'participava': 'Executei',
    'colaborei': 'Colaborei',  # Mantém mas pode ser melhorado no contexto
    'apoiei': 'Suportei',
    'apoiava': 'Suportei',
    'contribuí': 'Implementei',
    'fazia': 'Gerenciei',
    'fazer': 'Gerenciar',
    'realizava': 'Entreguei',
    'realizar': 'Entregar',
    'atuava': 'Implementei',
    'atuar': 'Implementar',
    'trabalhava com': 'Utilizei',
    'trabalhava': 'Operei',
    'lidava com': 'Gerenciei',
    'lidava': 'Gerenciei',
    'responsável por': 'Liderei',
    'responsável': 'Liderei',
    'encarregado de': 'Coordenei',
    'encarregado': 'Coordenei',
    'estive envolvido': 'Participei',
    'estava envolvido': 'Participei',
    
    # Verbos genéricos → Verbos específicos
    'fiz': 'Implementei',
    'fazia': 'Executei',
    'desenvolvi': 'Construí',
    'desenvolvia': 'Construí',
    'criei': 'Desenhei',
    'criava': 'Desenhei',
    
    # Adicionar mais verbos fortes por contexto
    'implementei': 'Implementei',
    'executei': 'Executei',
    'gerenciei': 'Gerenciei',
    'liderei': 'Liderei',
    'coordenei': 'Coordenei',
    'otimizei': 'Otimizei',
    'automatizei': 'Automatizei',
    'escalei': 'Escalei',
    'estruturei': 'Estruturei',
    'planejei': 'Planejei',
    'conduzi': 'Conduzi',
    'entreguei': 'Entreguei',
    'aumentei': 'Aumentei',
    'reduzi': 'Reduzi',
    'alcancei': 'Atingi',
    'atingi': 'Atingi',
}


def gerar_bullet_star(componentes: dict, senioridade: str, area: str) -> str:
    """
    Gera bullet otimizado usando método STAR.
    
    Args:
        componentes: {
            'acao': str,  # Verbo + ação principal
            'contexto': str,  # Situação/contexto
            'ferramenta': str,  # Ferramenta/tecnologia usada
            'resultado_numerico': str,  # Métrica quantificada
            'impacto': str  # Impacto no negócio
        }
        senioridade: 'junior' | 'pleno' | 'senior' | 'executivo'
        area: Área profissional (ex: 'Software Engineer')
        
    Returns:
        str: Bullet formatado com STAR
    """
    # Extrair componentes com fallbacks
    acao = componentes.get('acao', 'Executei')
    contexto = componentes.get('contexto', '')
    ferramenta = componentes.get('ferramenta', '')
    resultado = componentes.get('resultado_numerico', '')
    impacto = componentes.get('impacto', '')
    
    # Upgrade do verbo se for fraco
    acao = _upgrade_verbo(acao)
    
    # Selecionar template baseado em senioridade
    if senioridade == 'junior':
        # Template Junior: Foco em volume, eficiência, ferramentas, frequência
        # • {VERBO} {TAREFA} utilizando {FERRAMENTA}, processando {VOLUME} e alcançando {RESULTADO}
        
        bullet = f"• {acao}"
        
        if contexto:
            bullet += f" {contexto}"
        
        if ferramenta:
            bullet += f" utilizando {ferramenta}"
        
        if resultado:
            bullet += f", processando {resultado}"
        
        if impacto:
            bullet += f" e alcançando {impacto}"
        
        return bullet
    
    elif senioridade == 'pleno':
        # Template Pleno: Foco em projetos, otimizações, iniciativas
        # • {VERBO} {PROJETO} com {FERRAMENTA}, otimizando {METRICA} em {PERCENTUAL}
        
        bullet = f"• {acao}"
        
        if contexto:
            bullet += f" {contexto}"
        
        if ferramenta:
            bullet += f" com {ferramenta}"
        
        if resultado and impacto:
            bullet += f", otimizando {resultado} e atingindo {impacto}"
        elif resultado:
            bullet += f", gerando {resultado}"
        elif impacto:
            bullet += f", resultando em {impacto}"
        
        return bullet
    
    elif senioridade == 'senior':
        # Template Senior: Foco em liderança técnica, arquitetura, mentorias
        # • {VERBO} {INICIATIVA_ESTRATEGICA} liderando {CONTEXTO}, resultando em {IMPACTO_NEGOCIO}
        
        bullet = f"• {acao}"
        
        if contexto:
            bullet += f" {contexto}"
        
        if ferramenta:
            bullet += f" com {ferramenta}"
        
        if resultado:
            bullet += f", liderando entrega de {resultado}"
        
        if impacto:
            bullet += f" e gerando {impacto}"
        
        return bullet
    
    else:  # executivo
        # Template Executivo: Foco em P&L, budget, crescimento, transformação, equipes
        # • {VERBO} {TRANSFORMACAO} gerindo budget de {VALOR}, entregando {RESULTADO} e impactando {METRICA_ESTRATEGICA}
        
        bullet = f"• {acao}"
        
        if contexto:
            bullet += f" {contexto}"
        
        if ferramenta or resultado:
            budget_info = ferramenta if ferramenta else f"operação de {resultado}"
            bullet += f" gerenciando {budget_info}"
        
        if impacto:
            bullet += f", entregando {impacto}"
        elif resultado and not ferramenta:
            bullet += f", atingindo {resultado}"
        
        return bullet


def _upgrade_verbo(acao: str) -> str:
    """
    Faz upgrade de verbo fraco para verbo forte.
    
    Args:
        acao: String com a ação (pode começar com verbo fraco)
        
    Returns:
        str: Ação com verbo forte
    """
    acao_lower = acao.lower()
    
    # Tentar fazer match com verbos fracos e substituir
    for verbo_fraco, verbo_forte in VERBOS_UPGRADE.items():
        if acao_lower.startswith(verbo_fraco):
            # Substituir mantendo o resto da frase
            resto = acao[len(verbo_fraco):].strip()
            return f"{verbo_forte} {resto}" if resto else verbo_forte
    
    # Se não achou verbo fraco, retornar original capitalizado
    return acao.capitalize()


def aplicar_star_method_completo(experiencia: dict, area: str) -> dict:
    """
    Aplica STAR em todos os bullets de uma experiência.
    
    Args:
        experiencia: {
            'cargo': str,
            'empresa': str,
            'periodo': str,
            'bullets': list,  # Lista de strings com bullets originais
            'senioridade': str  # Nível inferido ou fornecido
        }
        area: Área profissional
        
    Returns:
        dict: {
            ...experiencia,
            'bullets_originais': list,
            'bullets_otimizados': list,
            'diferencas_destacadas': list  # Para mostrar o que mudou
        }
    """
    senioridade = experiencia.get('senioridade', 'pleno')
    bullets_originais = experiencia.get('bullets', [])
    
    bullets_otimizados = []
    diferencas = []
    
    for bullet_original in bullets_originais:
        # Extrair componentes do bullet original (análise simples)
        componentes = _extrair_componentes_bullet(bullet_original)
        
        # Gerar bullet otimizado
        bullet_otimizado = gerar_bullet_star(componentes, senioridade, area)
        
        bullets_otimizados.append(bullet_otimizado)
        
        # Destacar diferenças
        diferenca = {
            'original': bullet_original,
            'otimizado': bullet_otimizado,
            'melhorias': _identificar_melhorias(bullet_original, bullet_otimizado)
        }
        diferencas.append(diferenca)
    
    return {
        **experiencia,
        'bullets_originais': bullets_originais,
        'bullets_otimizados': bullets_otimizados,
        'diferencas_destacadas': diferencas
    }


def _extrair_componentes_bullet(bullet: str) -> dict:
    """
    Extrai componentes STAR de um bullet existente.
    
    Args:
        bullet: Texto do bullet original
        
    Returns:
        dict: Componentes identificados
    """
    import re
    
    componentes = {
        'acao': '',
        'contexto': '',
        'ferramenta': '',
        'resultado_numerico': '',
        'impacto': ''
    }
    
    # Extrair ação (primeiros 1-3 palavras, geralmente verbo + objeto)
    palavras = bullet.split()
    if palavras:
        componentes['acao'] = ' '.join(palavras[:2]) if len(palavras) > 1 else palavras[0]
    
    # Extrair número/métrica
    numeros = re.findall(r'\d+[%\w]*', bullet)
    if numeros:
        componentes['resultado_numerico'] = ', '.join(numeros)
    
    # Tentar identificar ferramenta (palavras capitalizadas, siglas, tecnologias conhecidas)
    ferramentas_pattern = r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b'
    ferramentas_encontradas = re.findall(ferramentas_pattern, bullet)
    if ferramentas_encontradas:
        # Filtrar nomes muito comuns que não são ferramentas
        ferramentas_filtradas = [f for f in ferramentas_encontradas 
                                 if f not in ['I', 'A', 'O', 'E']]
        if ferramentas_filtradas:
            componentes['ferramenta'] = ferramentas_filtradas[0]
    
    # Contexto = o resto do bullet (simplificado)
    if len(palavras) > 3:
        componentes['contexto'] = ' '.join(palavras[2:10])  # Pegar palavras do meio
    
    return componentes


def _identificar_melhorias(bullet_original: str, bullet_otimizado: str) -> list:
    """
    Identifica quais melhorias foram feitas no bullet.
    
    Args:
        bullet_original: Bullet antes da otimização
        bullet_otimizado: Bullet depois da otimização
        
    Returns:
        list: Lista de strings descrevendo as melhorias
    """
    melhorias = []
    
    # Detectar se verbo foi melhorado
    verbos_fracos_encontrados = [v for v in VERBOS_UPGRADE.keys() 
                                  if v in bullet_original.lower()]
    if verbos_fracos_encontrados:
        melhorias.append(f"Verbo melhorado: {verbos_fracos_encontrados[0]} → verbo forte")
    
    # Detectar se métrica foi adicionada/melhorada
    import re
    numeros_original = re.findall(r'\d+', bullet_original)
    numeros_otimizado = re.findall(r'\d+', bullet_otimizado)
    
    if len(numeros_otimizado) > len(numeros_original):
        melhorias.append("Métricas quantificáveis adicionadas")
    
    # Detectar se bullet ficou mais estruturado
    if len(bullet_otimizado) > len(bullet_original):
        melhorias.append("Estrutura STAR aplicada com mais contexto")
    
    # Detectar uso de conectores profissionais
    conectores = ['utilizando', 'com', 'resultando em', 'gerando', 'entregando', 'impactando']
    if any(c in bullet_otimizado.lower() for c in conectores):
        if not any(c in bullet_original.lower() for c in conectores):
            melhorias.append("Conectores profissionais adicionados")
    
    return melhorias if melhorias else ["Bullet otimizado com método STAR"]


def gerar_verbos_fortes_por_area(area: str) -> list:
    """
    Retorna lista de verbos fortes recomendados para uma área específica.
    
    Args:
        area: Área profissional
        
    Returns:
        list: Lista de verbos fortes
    """
    from modules.otimizador.market_knowledge import obter_conhecimento_mercado
    
    conhecimento = obter_conhecimento_mercado(area)
    return conhecimento.get('verbos_fortes', [
        'Implementei', 'Desenvolvi', 'Gerenciei', 'Liderei', 'Otimizei',
        'Estruturei', 'Coordenei', 'Executei'
    ])
