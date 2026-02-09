"""
Salary Lookup - Real salary data scraping from salario.com.br (CAGED/MTE).

This module fetches real Brazilian salary data from salario.com.br,
which provides official CAGED (Cadastro Geral de Empregados e Desempregados)
data from the Ministry of Labor (MTE).

Uses Streamlit session_state caching to avoid repeated lookups on reruns.
"""

import re
import logging
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Request timeout in seconds
REQUEST_TIMEOUT = 10


def _normalizar_cargo_para_slug(cargo: str) -> str:
    """
    Normalize cargo name to URL slug format.
    
    Examples:
        "Coordenador de Compras" -> "coordenador-de-compras"
        "Gerente de RevOps" -> "gerente-de-revops"
    
    Args:
        cargo: Raw cargo name
        
    Returns:
        URL-friendly slug
    """
    if not cargo:
        return ''
    
    # Convert to lowercase
    slug = cargo.lower().strip()
    
    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    
    return slug.strip('-')


def _extrair_valor_salario(texto: str) -> Optional[float]:
    """
    Extract numeric salary value from Portuguese text.
    
    Examples:
        "R$ 8.774,00" -> 8774.0
        "R$ 14.500" -> 14500.0
        "8.774,50" -> 8774.5
    
    Args:
        texto: Salary text with Brazilian formatting
        
    Returns:
        Float value or None if parsing fails
    """
    if not texto:
        return None
    
    try:
        # Remove R$ and whitespace
        valor_limpo = texto.replace('R$', '').strip()
        
        # Convert Brazilian format to standard: remove periods, replace comma with period
        valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
        
        return float(valor_limpo)
    except (ValueError, AttributeError):
        return None


def buscar_salario_real(cargo: str, cache_dict: Optional[Dict] = None) -> Optional[Dict]:
    """
    Fetch real salary data from salario.com.br for a specific cargo.
    
    This function scrapes the official CAGED/MTE salary data from salario.com.br.
    Uses a simple approach: tries to find the cargo page and extract salary values.
    
    Args:
        cargo: Target cargo name (e.g., "Coordenador de Compras")
        cache_dict: Optional dict to use for caching (typically st.session_state)
        
    Returns:
        Dict with 'piso', 'media', 'teto' (all floats) or None if lookup fails
        
    Example:
        {
            'piso': 6500.0,
            'media': 8774.0,
            'teto': 12000.0,
            'fonte': 'salario.com.br (CAGED/MTE)'
        }
    """
    if not cargo:
        return None
    
    # Check cache first (if provided)
    cache_key = f'salary_lookup_{cargo.lower()}'
    if cache_dict and cache_key in cache_dict:
        logger.info(f"Salary data for '{cargo}' found in cache")
        return cache_dict[cache_key]
    
    logger.info(f"Fetching real salary data for cargo: {cargo}")
    
    try:
        # Normalize cargo to slug format
        cargo_slug = _normalizar_cargo_para_slug(cargo)
        
        if not cargo_slug:
            logger.warning(f"Could not normalize cargo '{cargo}' to slug")
            return None
        
        # Try to search for the cargo on salario.com.br
        # The site uses a search mechanism, so we'll try to find a page
        # Note: This is a simplified approach. A more robust implementation
        # would use the site's search API or handle pagination.
        
        # Attempt 1: Try direct cargo page (if CBO code was known, would be ideal)
        # For now, we'll use the site's search functionality
        search_url = f"https://www.salario.com.br/busca/?q={cargo_slug}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find salary data on the page
        # The site structure may vary, so we'll look for common patterns
        # This is a simplified extraction - a production version would be more robust
        
        # Look for salary values (common patterns on Brazilian salary sites)
        # Examples: "Piso salarial", "Média", "Teto"
        
        resultado = None
        
        # Try to find salary table or sections
        # Pattern 1: Look for specific salary indicators
        salario_elements = soup.find_all(['td', 'span', 'div'], 
                                         text=re.compile(r'R\$\s*[\d.,]+'))
        
        if salario_elements:
            # Extract all salary values found
            valores = []
            for elem in salario_elements[:10]:  # Limit to first 10 to avoid noise
                texto = elem.get_text(strip=True)
                valor = _extrair_valor_salario(texto)
                if valor and 1000 <= valor <= 100000:  # Sanity check
                    valores.append(valor)
            
            if len(valores) >= 3:
                # Sort values and take percentiles as piso/media/teto
                valores.sort()
                resultado = {
                    'piso': valores[0],
                    'media': valores[len(valores) // 2],
                    'teto': valores[-1],
                    'fonte': 'salario.com.br (CAGED/MTE)'
                }
                logger.info(f"Salary data extracted for '{cargo}': {resultado}")
        
        # If no results found with simple extraction, return None
        if not resultado:
            logger.warning(f"Could not extract salary data for cargo '{cargo}' from salario.com.br")
            return None
        
        # Cache the result (if cache_dict provided)
        if cache_dict is not None:
            cache_dict[cache_key] = resultado
        
        return resultado
        
    except requests.Timeout:
        logger.warning(f"Timeout fetching salary data for '{cargo}' from salario.com.br")
        return None
    except requests.RequestException as e:
        logger.warning(f"Request error fetching salary data for '{cargo}': {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching salary data for '{cargo}': {e}")
        return None


def formatar_dados_salariais_para_prompt(dados: Optional[Dict]) -> str:
    """
    Format salary data for injection into GPT prompt.
    
    Args:
        dados: Salary data dict from buscar_salario_real()
        
    Returns:
        Formatted string for prompt injection
    """
    if not dados:
        return ""
    
    piso = dados.get('piso', 0)
    media = dados.get('media', 0)
    teto = dados.get('teto', 0)
    fonte = dados.get('fonte', 'salario.com.br')
    
    return f"""
DADOS SALARIAIS REAIS DO MERCADO (fonte: {fonte}):
- Piso: R$ {piso:,.2f}
- Média: R$ {media:,.2f}
- Teto: R$ {teto:,.2f}

Use ESTES dados como base para a análise salarial na tabela de percentis.
NÃO invente outros valores - base sua análise nestes dados oficiais.
Se os dados acima não estiverem disponíveis, informe "Dados salariais não disponíveis para este cargo" na seção de análise salarial.
""".replace(',', 'X').replace('.', ',').replace('X', '.')  # Convert to BR format
