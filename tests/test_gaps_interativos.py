"""
Testes unitários para a fase de gaps interativos do Protocolo Nóbile.
"""

import pytest
from unittest.mock import Mock, patch
import streamlit as st
from ui.screens.fase_gaps_interativos import preparar_contexto_gaps
from ui.screens.fase_analise_loading import extrair_gaps_da_analise


def test_preparar_contexto_gaps_com_experiencia():
    """Testa preparação de contexto quando usuário tem experiências"""
    st.session_state.gaps_respondidos = {
        'gap_0': {
            'nome': 'Python',
            'resposta': 'Trabalho com Python há 3 anos',
            'tem_experiencia': True,
            'impacto': 'Alto'
        },
        'gap_1': {
            'nome': 'SQL',
            'resposta': '',
            'tem_experiencia': False,
            'impacto': 'Médio'
        }
    }
    
    contexto = preparar_contexto_gaps()
    
    assert 'Python' in contexto
    assert 'Trabalho com Python há 3 anos' in contexto
    assert 'SQL' in contexto
    assert '✅' in contexto
    assert '❌' in contexto


def test_preparar_contexto_gaps_vazio():
    """Testa preparação de contexto sem respostas"""
    st.session_state.gaps_respondidos = {}
    
    contexto = preparar_contexto_gaps()
    
    assert 'RESPOSTAS DO CANDIDATO' in contexto
    assert 'INSTRUÇÕES CRÍTICAS' in contexto


def test_extrair_gaps_formato_padrao():
    """Testa extração de gaps no formato padrão"""
    analise = """
## ⚠️ GAPS IDENTIFICADOS

**Gaps Técnicos:**
1. **Python:** Essencial para análise de dados - **Impacto:** Alto
2. **SQL:** Importante para consultas - **Impacto:** Médio
3. **Git:** Controle de versão - **Impacto:** Baixo
"""
    
    gaps = extrair_gaps_da_analise(analise)
    
    assert len(gaps) == 3
    assert gaps[0]['nome'] == 'Python'
    assert gaps[0]['impacto'] == 'Alto'
    assert gaps[1]['nome'] == 'SQL'
    assert gaps[1]['impacto'] == 'Médio'


def test_extrair_gaps_formato_alternativo():
    """Testa extração com formato sem numeração"""
    analise = """
**Docker:** Containerização de apps - **Impacto:** Alto
**Kubernetes:** Orquestração - **Impacto:** Médio
"""
    
    gaps = extrair_gaps_da_analise(analise)
    
    assert len(gaps) >= 2


def test_extrair_gaps_sem_gaps():
    """Testa quando não há gaps na análise"""
    analise = "Análise sem gaps identificados"
    
    gaps = extrair_gaps_da_analise(analise)
    
    assert len(gaps) == 0


def test_preparar_contexto_gaps_apenas_possui():
    """Testa preparação de contexto quando usuário possui todas as skills"""
    st.session_state.gaps_respondidos = {
        'gap_0': {
            'nome': 'Python',
            'resposta': 'Trabalho com Python há 3 anos',
            'tem_experiencia': True,
            'impacto': 'Alto'
        },
        'gap_1': {
            'nome': 'JavaScript',
            'resposta': 'Uso JavaScript há 2 anos',
            'tem_experiencia': True,
            'impacto': 'Médio'
        }
    }
    
    contexto = preparar_contexto_gaps()
    
    assert 'Python' in contexto
    assert 'JavaScript' in contexto
    assert 'Trabalho com Python há 3 anos' in contexto
    assert '✅' in contexto
    assert 'Skills/Experiências que o candidato POSSUI' in contexto


def test_preparar_contexto_gaps_apenas_nao_possui():
    """Testa preparação de contexto quando usuário não possui nenhuma skill"""
    st.session_state.gaps_respondidos = {
        'gap_0': {
            'nome': 'Python',
            'resposta': '',
            'tem_experiencia': False,
            'impacto': 'Alto'
        },
        'gap_1': {
            'nome': 'JavaScript',
            'resposta': '',
            'tem_experiencia': False,
            'impacto': 'Médio'
        }
    }
    
    contexto = preparar_contexto_gaps()
    
    assert 'Python' in contexto
    assert 'JavaScript' in contexto
    assert '❌' in contexto
    assert 'Skills que o candidato NÃO possui' in contexto


def test_extrair_gaps_case_insensitive():
    """Testa que a extração funciona independente de case"""
    analise = """
1. **Python:** Test - **impacto:** alto
2. **SQL:** Test - **IMPACTO:** MÉDIO
"""
    
    gaps = extrair_gaps_da_analise(analise)
    
    assert len(gaps) == 2
    assert gaps[0]['impacto'] == 'Alto'
    assert gaps[1]['impacto'] == 'Médio'


def test_extrair_gaps_com_colchetes():
    """Testa extração de gaps com formato usando colchetes"""
    analise = """
1. **[Python]:** Linguagem essencial - **Impacto:** Alto
2. **[SQL]:** Banco de dados - **Impacto:** Médio
"""
    
    gaps = extrair_gaps_da_analise(analise)
    
    assert len(gaps) == 2
    assert gaps[0]['nome'] == 'Python'
    assert gaps[1]['nome'] == 'SQL'


def test_preparar_contexto_verifica_instrucoes():
    """Testa que o contexto inclui as instruções críticas"""
    st.session_state.gaps_respondidos = {}
    
    contexto = preparar_contexto_gaps()
    
    assert 'INSTRUÇÕES CRÍTICAS' in contexto
    assert 'Use APENAS' in contexto
    assert 'NÃO invente' in contexto
    assert 'OTIMIZAR' in contexto
