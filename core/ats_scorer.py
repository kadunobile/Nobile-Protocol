"""
Sistema de Pontuação ATS (Applicant Tracking System) - v2.

Usa TF-IDF + Cosine Similarity para calcular compatibilidade real
entre o CV do candidato e uma Job Description gerada por IA.

Substitui o sistema anterior baseado em regex e listas fixas.
"""

import re
import logging
from typing import Dict, Optional

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.utils import chamar_gpt

# Configurar logger
logger = logging.getLogger(__name__)


class ATSEngine:
    """
    Engine de ATS baseada em TF-IDF + Cosine Similarity.
    
    Captura termos compostos (n-grams de 1 a 3 palavras),
    crucial para cargos técnicos e de gestão.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_df=0.85,
            min_df=1
        )
    
    def _clean_text(self, text: str) -> str:
        """Limpeza de texto para padronização."""
        if not text:
            return ""
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def calculate_match(self, cv_text: str, job_description: str) -> float:
        """
        Calcula a nota de compatibilidade (0.0 a 100.0).
        
        Args:
            cv_text: Texto completo do CV
            job_description: Descrição da vaga para comparação
            
        Returns:
            Float com score de 0 a 100
        """
        cv_clean = self._clean_text(cv_text)
        job_clean = self._clean_text(job_description)
        
        if not cv_clean or not job_clean:
            return 0.0
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform([cv_clean, job_clean])
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            match_score = similarity_matrix[0][0]
            return round(match_score * 100, 2)
        except ValueError:
            return 0.0
        except Exception as e:
            logger.error(f"Erro no cálculo ATS: {e}")
            return 0.0


# Instância global reutilizável
_ats_engine = ATSEngine()


def gerar_job_description(client, cargo: str) -> Optional[str]:
    """
    Gera uma Job Description padrão de mercado usando IA.
    
    Args:
        client: Cliente OpenAI inicializado
        cargo: Nome do cargo para gerar a JD
        
    Returns:
        Job Description gerada ou None em caso de erro
    """
    logger.info(f"Gerando Job Description para: {cargo}")
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento. "
            "Gere uma Job Description (descrição de vaga) realista e completa para o cargo informado. "
            "Inclua: responsabilidades, requisitos técnicos, soft skills, ferramentas, "
            "qualificações desejadas e diferenciais. "
            "Use termos que sistemas ATS reais buscam. "
            "Responda APENAS com a Job Description, sem introdução nem comentários. "
            "Escreva em português brasileiro."
        )},
        {"role": "user", "content": f"Gere a Job Description para o cargo: {cargo}"}
    ]
    
    jd = chamar_gpt(
        client,
        msgs,
        temperature=0.3,
        seed=42
    )
    
    if jd:
        logger.info(f"JD gerada com sucesso ({len(jd)} caracteres)")
    else:
        logger.error("Falha ao gerar JD")
    
    return jd


def extrair_cargo_do_cv(client, cv_texto: str) -> Optional[str]:
    """
    Extrai o cargo atual/mais recente do candidato a partir do CV.
    
    Args:
        client: Cliente OpenAI inicializado
        cv_texto: Texto completo do CV
        
    Returns:
        Nome do cargo extraído ou None
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
    
    cargo = chamar_gpt(
        client,
        msgs,
        temperature=0.1,
        seed=42
    )
    
    if cargo:
        cargo = cargo.strip().strip('"').strip("'")
        logger.info(f"Cargo extraído: {cargo}")
    else:
        logger.error("Falha ao extrair cargo do CV")
    
    return cargo


def calcular_score_ats(cv_texto: str, cargo_alvo: str, client=None) -> Dict:
    """
    Calcula Score ATS usando TF-IDF + Cosine Similarity.
    
    Se um client OpenAI for fornecido, gera uma JD real via IA.
    Caso contrário, usa o cargo como JD simplificada.
    
    Args:
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para gerar a Job Description
        client: Cliente OpenAI (opcional, mas recomendado)
        
    Returns:
        Dict com score_total, percentual, nivel e detalhes
    """
    logger.info(f"Calculando score ATS para cargo: {cargo_alvo}")
    
    # Gerar Job Description
    job_description = None
    if client:
        job_description = gerar_job_description(client, cargo_alvo)
    
    # Fallback: usar cargo como texto base
    if not job_description:
        logger.warning("Usando cargo como JD simplificada (sem client OpenAI)")
        job_description = f"""
        Vaga para {cargo_alvo}. 
        Requisitos: experiência na área, habilidades técnicas relevantes, 
        capacidade de trabalho em equipe, boa comunicação, 
        resultados mensuráveis, gestão de projetos.
        """
    
    # Calcular score principal (TF-IDF)
    score_tfidf = _ats_engine.calculate_match(cv_texto, job_description)
    
    # Classificar
    nivel = classificar_score(score_tfidf)
    
    resultado = {
        'score_total': score_tfidf,
        'max_score': 100,
        'percentual': score_tfidf,
        'nivel': nivel,
        'cargo_avaliado': cargo_alvo,
        'jd_gerada': job_description is not None,
        'detalhes': {
            'metodo': 'TF-IDF + Cosine Similarity',
            'ngrams': '1-3',
        }
    }
    
    logger.info(f"Score ATS: {score_tfidf}/100 ({nivel})")
    return resultado


def classificar_score(score: float) -> str:
    """
    Classifica o score ATS em níveis qualitativos.
    
    Args:
        score: Pontuação total (0-100)
        
    Returns:
        Classificação textual do score
    """
    if score >= 70:
        return "Excelente"
    elif score >= 50:
        return "Bom"
    elif score >= 30:
        return "Regular"
    else:
        return "Precisa Melhorar"
