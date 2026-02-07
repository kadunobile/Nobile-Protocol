"""
Helpers Export - Utilitários para exportação de CV em múltiplos formatos.

Fornece funções para gerar PDF, DOCX e TXT do CV otimizado,
além de preparar dados de analytics.
"""

import io
from typing import Dict, List


def gerar_txt(cv_texto: str) -> bytes:
    """
    Gera arquivo TXT do CV.
    
    Args:
        cv_texto: Texto do CV otimizado
        
    Returns:
        bytes: Conteúdo do arquivo TXT
    """
    return cv_texto.encode('utf-8')


def gerar_analytics_data(score_inicial: Dict, score_final: Dict, gaps_alvo: List[str]) -> Dict:
    """
    Gera dados de analytics da otimização.
    
    Args:
        score_inicial: Resultado do score ATS inicial
        score_final: Resultado do score ATS final
        gaps_alvo: Lista de gaps identificados
        
    Returns:
        Dict com dados de analytics
    """
    # Calcular melhoria percentual considerando caso especial quando score inicial é 0
    if score_inicial['score_total'] > 0:
        melhoria_percentual = ((score_final['score_total'] - score_inicial['score_total']) / 
                               score_inicial['score_total'] * 100)
    else:
        # Se score inicial era 0, mostrar progresso em relação à meta de 80
        melhoria_percentual = (score_final['score_total'] / 80) * 100
    
    analytics = {
        'score_melhoria': score_final['score_total'] - score_inicial['score_total'],
        'score_melhoria_percentual': melhoria_percentual,
        'keywords_adicionadas': (score_final['detalhes']['keywords']['encontradas'] - 
                                 score_inicial['detalhes']['keywords']['encontradas']),
        'metricas_adicionadas': (score_final['detalhes']['metricas']['quantidade'] - 
                                 score_inicial['detalhes']['metricas']['quantidade']),
        'gaps_resolvidos': len(gaps_alvo),
        'nivel_inicial': score_inicial.get('nivel', 'N/A'),
        'nivel_final': score_final.get('nivel', 'N/A'),
        'atingiu_meta': score_final['score_total'] >= 80
    }
    
    return analytics


def formatar_comparacao_antes_depois(score_inicial: Dict, score_final: Dict) -> str:
    """
    Gera texto formatado para comparação antes/depois.
    
    Args:
        score_inicial: Resultado do score ATS inicial
        score_final: Resultado do score ATS final
        
    Returns:
        str: Texto formatado para exibição
    """
    comparacao = f"""
# 📊 COMPARAÇÃO ANTES × DEPOIS

## Score Total
**ANTES:** {score_inicial['score_total']}/100 ({score_inicial['nivel']})  
**DEPOIS:** {score_final['score_total']}/100 ({score_final['nivel']})  
**MELHORIA:** +{score_final['score_total'] - score_inicial['score_total']:.1f} pontos

---

## Breakdown por Categoria

### Seções do CV
**ANTES:** {score_inicial['detalhes']['secoes']['encontradas']}/{score_inicial['detalhes']['secoes']['total']} seções  
**DEPOIS:** {score_final['detalhes']['secoes']['encontradas']}/{score_final['detalhes']['secoes']['total']} seções

### Keywords Relevantes
**ANTES:** {score_inicial['detalhes']['keywords']['encontradas']}/{score_inicial['detalhes']['keywords']['total']} keywords  
**DEPOIS:** {score_final['detalhes']['keywords']['encontradas']}/{score_final['detalhes']['keywords']['total']} keywords  
**ADICIONADAS:** {score_final['detalhes']['keywords']['encontradas'] - score_inicial['detalhes']['keywords']['encontradas']} novas keywords

### Métricas Quantificáveis
**ANTES:** {score_inicial['detalhes']['metricas']['quantidade']} números/métricas  
**DEPOIS:** {score_final['detalhes']['metricas']['quantidade']} números/métricas  
**ADICIONADAS:** {score_final['detalhes']['metricas']['quantidade'] - score_inicial['detalhes']['metricas']['quantidade']} novas métricas

### Formatação
**ANTES:** {score_inicial['detalhes']['formatacao']['bullets']} bullets, {score_inicial['detalhes']['formatacao']['datas']} datas  
**DEPOIS:** {score_final['detalhes']['formatacao']['bullets']} bullets, {score_final['detalhes']['formatacao']['datas']} datas

### Tamanho
**ANTES:** {score_inicial['detalhes']['tamanho']['palavras']} palavras  
**DEPOIS:** {score_final['detalhes']['tamanho']['palavras']} palavras
"""
    
    return comparacao


def formatar_linkedin_ready(linkedin_data: Dict) -> str:
    """
    Formata dados de LinkedIn em formato ready-to-copy.
    
    Args:
        linkedin_data: Dicionário com dados de LinkedIn
        
    Returns:
        str: Texto formatado para copiar/colar
    """
    headline = linkedin_data.get('headline', '')
    skills = linkedin_data.get('skills', [])
    about = linkedin_data.get('about', '')
    
    texto = f"""
# 🔵 LINKEDIN READY-TO-USE

## 🎯 Headline (copie e cole no LinkedIn)
{headline}

---

## 🛠️ Top Skills (adicione nesta ordem)
"""
    
    for i, skill in enumerate(skills[:10], 1):
        texto += f"{i}. {skill}\n"
    
    texto += f"""
---

## 📝 About Section (copie e cole no LinkedIn)
{about}

---

💡 **Dica:** Copie cada seção usando o botão de copiar ao lado direito!
"""
    
    return texto
