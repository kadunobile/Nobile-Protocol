from typing import Dict, List, Tuple
from difflib import SequenceMatcher
import re

def comparar_cvs(cv_original: str, cv_otimizado: str) -> Dict:
    """
    Compara CV antes e depois da otimização.
    
    Returns:
        Dict com métricas de melhoria
    """
    def contar_palavras(texto):
        return len(texto.split())
    
    def contar_numeros(texto):
        return len(re.findall(r'\d+[%]?', texto))
    
    def contar_verbos_acao(texto):
        verbos = ['liderou', 'desenvolveu', 'implementou', 'gerenciou', 'criou', 
                  'aumentou', 'reduziu', 'otimizou', 'construiu', 'estabeleceu']
        count = sum(texto.lower().count(v) for v in verbos)
        return count
    
    def detectar_secoes(texto):
        secoes_padrao = ['experiência', 'educação', 'habilidades', 'certificações', 
                        'idiomas', 'projetos', 'resumo']
        return sum(1 for s in secoes_padrao if s in texto.lower())
    
    # Métricas
    metricas = {
        "palavras": {
            "antes": contar_palavras(cv_original),
            "depois": contar_palavras(cv_otimizado),
        },
        "numeros": {
            "antes": contar_numeros(cv_original),
            "depois": contar_numeros(cv_otimizado),
        },
        "verbos_acao": {
            "antes": contar_verbos_acao(cv_original),
            "depois": contar_verbos_acao(cv_otimizado),
        },
        "secoes": {
            "antes": detectar_secoes(cv_original),
            "depois": detectar_secoes(cv_otimizado),
        }
    }
    
    # Calcula melhorias
    for categoria in metricas:
        antes = metricas[categoria]["antes"]
        depois = metricas[categoria]["depois"]
        
        if antes > 0:
            melhoria = ((depois - antes) / antes) * 100
        else:
            melhoria = 100 if depois > 0 else 0
        
        metricas[categoria]["melhoria"] = round(melhoria, 1)
    
    # Similaridade textual
    similaridade = SequenceMatcher(None, cv_original, cv_otimizado).ratio()
    metricas["similaridade"] = round(similaridade * 100, 1)
    
    return metricas
