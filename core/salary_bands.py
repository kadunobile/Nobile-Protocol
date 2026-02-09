"""
Salary banding helper for realistic market salary ranges.

Provides salary bands (min/max/median) per cargo and porte/região.
Used to display realistic salary expectations and warn when user input
is far above market rates.

All values are CLT, BR market, without bonus (2024-2025 data).
"""

from typing import Dict, Tuple, Optional


# ─────────────────────────────────────────────
# SALARY BAND CONFIGURATIONS
# ─────────────────────────────────────────────

SALARY_BANDS = {
    'coordenador de compras': {
        'default': {'min': 14000, 'max': 18000, 'median': 16000},
        'pequena': {'min': 12000, 'max': 15000, 'median': 13500},
        'media': {'min': 14000, 'max': 18000, 'median': 16000},
        'grande': {'min': 16000, 'max': 20000, 'median': 18000},
        'multi': {'min': 16000, 'max': 20000, 'median': 18000},
        'sp_capitais': {'min': 15000, 'max': 19000, 'median': 17000},
    },
    'coordenador(a) de compras': {
        'default': {'min': 14000, 'max': 18000, 'median': 16000},
        'pequena': {'min': 12000, 'max': 15000, 'median': 13500},
        'media': {'min': 14000, 'max': 18000, 'median': 16000},
        'grande': {'min': 16000, 'max': 20000, 'median': 18000},
        'multi': {'min': 16000, 'max': 20000, 'median': 18000},
        'sp_capitais': {'min': 15000, 'max': 19000, 'median': 17000},
    },
    'coordenadora de compras': {
        'default': {'min': 14000, 'max': 18000, 'median': 16000},
        'pequena': {'min': 12000, 'max': 15000, 'median': 13500},
        'media': {'min': 14000, 'max': 18000, 'median': 16000},
        'grande': {'min': 16000, 'max': 20000, 'median': 18000},
        'multi': {'min': 16000, 'max': 20000, 'median': 18000},
        'sp_capitais': {'min': 15000, 'max': 19000, 'median': 17000},
    },
    'gerente de revops': {
        'default': {'min': 18000, 'max': 24000, 'median': 21000},
        'pequena': {'min': 16000, 'max': 20000, 'median': 18000},
        'media': {'min': 18000, 'max': 24000, 'median': 21000},
        'grande': {'min': 20000, 'max': 28000, 'median': 24000},
        'multi': {'min': 20000, 'max': 28000, 'median': 24000},
        'sp_capitais': {'min': 20000, 'max': 26000, 'median': 23000},
    },
}

# Fallback band for unmapped cargos (generic estimation)
FALLBACK_BAND = {
    'default': {'min': 5000, 'max': 25000, 'median': 12000},
}


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def normalizar_cargo(cargo: str) -> str:
    """
    Normalize cargo name for lookup in salary bands.
    
    Args:
        cargo: Raw cargo name from user input
        
    Returns:
        Normalized cargo name (lowercase, stripped)
    """
    if not cargo:
        return ''
    return cargo.strip().lower()


def detectar_porte_regiao(localizacao: str = '', perfil: Dict = None) -> str:
    """
    Detect company size (porte) or region category from location or profile.
    
    Args:
        localizacao: User's target location
        perfil: User profile dict (may contain additional context)
        
    Returns:
        Category key: 'pequena', 'media', 'grande', 'multi', 'sp_capitais', or 'default'
    """
    if not localizacao:
        return 'default'
    
    loc_lower = localizacao.lower()
    
    # Check for SP/capitais indicators
    capitais = [
        'são paulo', 'sp', 'rio de janeiro', 'rj', 'belo horizonte', 
        'brasília', 'curitiba', 'porto alegre', 'recife', 'salvador', 
        'fortaleza', 'manaus', 'belém', 'goiânia'
    ]
    
    for capital in capitais:
        if capital in loc_lower:
            return 'sp_capitais'
    
    # Default if no specific indicator found
    return 'default'


def obter_banda_salarial(cargo: str, porte: str = 'default', regiao: str = 'default') -> Dict:
    """
    Get salary band (min/max/median) for a specific cargo and porte/região.
    
    Args:
        cargo: Target cargo name (will be normalized)
        porte: Company size category ('pequena', 'media', 'grande', 'multi', or 'default')
        regiao: Region category ('sp_capitais' or 'default')
        
    Returns:
        Dict with 'min', 'max', 'median', 'cargo', 'category', 'is_fallback'
    """
    cargo_norm = normalizar_cargo(cargo)
    
    # Try to find cargo in bands
    if cargo_norm in SALARY_BANDS:
        bands = SALARY_BANDS[cargo_norm]
        
        # Priority: specific porte/regiao parameter > default
        # If regiao is explicitly sp_capitais, use it
        # Otherwise prefer porte, then regiao, then default
        if regiao in bands and regiao != 'default':
            category_key = regiao
        elif porte in bands and porte != 'default':
            category_key = porte
        elif regiao in bands:
            category_key = regiao
        elif porte in bands:
            category_key = porte
        else:
            category_key = 'default'
        
        if category_key in bands:
            band = bands[category_key].copy()
            band['cargo'] = cargo
            band['category'] = category_key
            band['is_fallback'] = False
            return band
    
    # Fallback for unmapped cargos
    band = FALLBACK_BAND['default'].copy()
    band['cargo'] = cargo
    band['category'] = 'estimativa'
    band['is_fallback'] = True
    return band


def validar_salario_banda(
    pretensao_str: str,
    cargo: str,
    localizacao: str = '',
    perfil: Dict = None
) -> Dict:
    """
    Validate if salary is within reasonable market band and generate warning if needed.
    
    Args:
        pretensao_str: Salary string (e.g., "R$ 25.000,00" or "25000")
        cargo: Target cargo name
        localizacao: User's target location
        perfil: User profile dict (optional)
        
    Returns:
        Dict with:
        - 'valor': float salary value (or None if invalid)
        - 'banda': salary band dict
        - 'dentro_banda': bool (True if within band)
        - 'mensagem': str warning message (empty if OK)
        - 'nivel': str ('ok', 'acima', 'muito_acima', 'invalido')
    """
    # Parse salary value
    try:
        valor_limpo = pretensao_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
        valor = float(valor_limpo)
    except (ValueError, AttributeError):
        return {
            'valor': None,
            'banda': None,
            'dentro_banda': False,
            'mensagem': '',
            'nivel': 'invalido'
        }
    
    # Get appropriate salary band
    porte_regiao = detectar_porte_regiao(localizacao, perfil)
    banda = obter_banda_salarial(cargo, porte=porte_regiao)
    
    # Check if salary is within band
    minimo = banda['min']
    maximo = banda['max']
    mediana = banda['median']
    
    # Determine status and message
    if valor <= maximo:
        # Within or below band - OK
        return {
            'valor': valor,
            'banda': banda,
            'dentro_banda': True,
            'mensagem': '',
            'nivel': 'ok'
        }
    elif valor <= maximo * 1.2:
        # Slightly above band (up to 20% over) - mild warning
        categoria_texto = _formatar_categoria(banda['category'])
        mensagem = (
            f"⚠️ **Valor informado está acima da média de mercado**\n\n"
            f"Valor informado: **R$ {valor:,.2f}**\n\n"
            f"Faixa típica para {cargo} ({categoria_texto}): "
            f"**R$ {minimo:,.2f} - R$ {maximo:,.2f}** (mediana ~R$ {mediana:,.2f})\n\n"
            f"Considere ajustar sua pretensão para alinhar com o mercado."
        )
        if banda['is_fallback']:
            mensagem += "\n\n*Nota: Faixa baseada em estimativa — cargo não mapeado em base de dados.*"
        
        return {
            'valor': valor,
            'banda': banda,
            'dentro_banda': False,
            'mensagem': mensagem,
            'nivel': 'acima'
        }
    else:
        # Well above band (>20% over) - strong warning
        categoria_texto = _formatar_categoria(banda['category'])
        mensagem = (
            f"🚨 **Valor informado está muito acima da média de mercado**\n\n"
            f"Valor informado: **R$ {valor:,.2f}**\n\n"
            f"Faixa típica para {cargo} ({categoria_texto}): "
            f"**R$ {minimo:,.2f} - R$ {maximo:,.2f}** (mediana ~R$ {mediana:,.2f})\n\n"
            f"Este valor pode dificultar significativamente sua recolocação. "
            f"Recomendamos revisar sua pretensão salarial."
        )
        if banda['is_fallback']:
            mensagem += "\n\n*Nota: Faixa baseada em estimativa — cargo não mapeado em base de dados.*"
        
        return {
            'valor': valor,
            'banda': banda,
            'dentro_banda': False,
            'mensagem': mensagem,
            'nivel': 'muito_acima'
        }


def _formatar_categoria(category: str) -> str:
    """
    Format category key to human-readable PT-BR text.
    
    Args:
        category: Category key from band lookup
        
    Returns:
        Human-readable category text
    """
    categorias = {
        'pequena': 'empresas pequenas',
        'media': 'empresas médias',
        'grande': 'grandes empresas',
        'multi': 'multinacionais',
        'sp_capitais': 'SP/capitais/alta complexidade',
        'default': 'mercado geral',
        'estimativa': 'estimativa de mercado'
    }
    return categorias.get(category, category)


def formatar_banda_display(banda: Dict) -> str:
    """
    Format salary band for display in UI (PT-BR).
    
    Args:
        banda: Salary band dict from obter_banda_salarial()
        
    Returns:
        Formatted string like "R$ 14.000 - R$ 18.000 (mediana ~R$ 16.000)"
    """
    minimo = banda['min']
    maximo = banda['max']
    mediana = banda['median']
    
    texto = f"R$ {minimo:,.0f} - R$ {maximo:,.0f} (mediana ~R$ {mediana:,.0f})"
    texto = texto.replace(',', '.')
    
    if banda.get('is_fallback'):
        texto += " *[estimativa]*"
    
    return texto
