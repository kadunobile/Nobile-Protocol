"""
Tests for senior profile context-aware gap detection.

Tests the helper functions that determine whether to skip gaps
for senior profiles based on position level and strategic experience.
"""

import pytest
from core.ats_scorer import (
    _is_senior_position,
    _is_tactical_tool,
    _should_skip_gap_for_senior
)


class TestSeniorPositionDetection:
    """Tests for _is_senior_position helper function."""
    
    def test_senior_titles_pt(self):
        """Testa detecção de cargos sênior em português."""
        assert _is_senior_position("Gerente de Vendas")
        assert _is_senior_position("Diretor de Marketing")
        assert _is_senior_position("Coordenador de TI")
        assert _is_senior_position("Líder Técnico")
        
    def test_senior_titles_en(self):
        """Testa detecção de cargos sênior em inglês."""
        assert _is_senior_position("Senior Software Engineer")
        assert _is_senior_position("Head of Product")
        assert _is_senior_position("VP of Sales")
        assert _is_senior_position("Chief Technology Officer")
        assert _is_senior_position("Engineering Manager")
        
    def test_c_level_titles(self):
        """Testa detecção de cargos C-level."""
        assert _is_senior_position("CTO")
        assert _is_senior_position("CEO")
        assert _is_senior_position("CFO")
        assert _is_senior_position("CMO")
        
    def test_non_senior_titles(self):
        """Testa que cargos júnior/pleno não são detectados como sênior."""
        assert not _is_senior_position("Analista de Dados")
        assert not _is_senior_position("Desenvolvedor Python")
        assert not _is_senior_position("Assistente de Marketing")
        assert not _is_senior_position("Junior Developer")
        assert not _is_senior_position("Intern")
        
    def test_case_insensitive(self):
        """Testa que detecção é case-insensitive."""
        assert _is_senior_position("GERENTE DE VENDAS")
        assert _is_senior_position("senior engineer")
        assert _is_senior_position("Head Of Product")


class TestTacticalToolDetection:
    """Tests for _is_tactical_tool helper function."""
    
    def test_sales_engagement_tools(self):
        """Testa detecção de ferramentas de sales engagement."""
        assert _is_tactical_tool("Outreach")
        assert _is_tactical_tool("Outreach.io")
        assert _is_tactical_tool("Salesloft")
        assert _is_tactical_tool("Apollo")
        assert _is_tactical_tool("Apollo.io")
        
    def test_conversation_intelligence_tools(self):
        """Testa detecção de ferramentas de conversation intelligence."""
        assert _is_tactical_tool("Gong")
        assert _is_tactical_tool("Gong.io")
        assert _is_tactical_tool("Chorus")
        
    def test_engagement_platforms(self):
        """Testa detecção de plataformas de engajamento."""
        assert _is_tactical_tool("Drift")
        assert _is_tactical_tool("Intercom")
        assert _is_tactical_tool("ZoomInfo")
        
    def test_non_tactical_tools(self):
        """Testa que ferramentas estratégicas/CRMs não são marcadas como táticas."""
        assert not _is_tactical_tool("Salesforce")
        assert not _is_tactical_tool("HubSpot")
        assert not _is_tactical_tool("Python")
        assert not _is_tactical_tool("Excel")
        assert not _is_tactical_tool("Power BI")
        
    def test_case_insensitive(self):
        """Testa que detecção é case-insensitive."""
        assert _is_tactical_tool("OUTREACH")
        assert _is_tactical_tool("gong")
        assert _is_tactical_tool("SalesLoft")


class TestSeniorGapSkipping:
    """Tests for _should_skip_gap_for_senior helper function."""
    
    def test_skip_tactical_for_senior_with_strategic_exp(self):
        """
        Testa que gap tático é pulado para cargo sênior
        com experiência estratégica.
        """
        cargo = "Gerente de Revenue Operations"
        cv = """
        Experiência em gestão de equipe de vendas, coordenação
        de processos de sales operations, implementação de estratégias
        de crescimento. Liderança de time de 10 SDRs.
        """
        
        should_skip, reason = _should_skip_gap_for_senior("Outreach", cargo, cv)
        assert should_skip is True
        assert "estratégi" in reason.lower() or "gestão" in reason.lower()
        
    def test_skip_gong_for_senior_director(self):
        """Testa que Gong é pulado para diretor com exp estratégica."""
        cargo = "Diretor de Vendas"
        cv = """
        Direção da área comercial, supervisão de equipes de vendas,
        implementação de processos de vendas B2B, coordenação com marketing.
        """
        
        should_skip, reason = _should_skip_gap_for_senior("Gong.io", cargo, cv)
        assert should_skip is True
        
    def test_dont_skip_tactical_for_junior(self):
        """
        Testa que gap tático NÃO é pulado para cargo júnior/pleno,
        mesmo com exp estratégica.
        """
        cargo = "Analista de Vendas"
        cv = """
        Gestão de projetos, coordenação de equipes.
        """
        
        should_skip, reason = _should_skip_gap_for_senior("Outreach", cargo, cv)
        assert should_skip is False
        assert reason == ""
        
    def test_dont_skip_if_no_strategic_exp(self):
        """
        Testa que gap tático NÃO é pulado para cargo sênior
        SEM experiência estratégica.
        """
        cargo = "Senior Sales Development Representative"
        cv = """
        Prospecção de leads, cold calling, email marketing,
        geração de pipeline. Trabalhei com Salesforce.
        """
        
        should_skip, reason = _should_skip_gap_for_senior("Outreach", cargo, cv)
        assert should_skip is False  # Senior mas sem exp estratégica
        
    def test_dont_skip_non_tactical_tools(self):
        """
        Testa que ferramentas não-táticas nunca são puladas,
        independente de senioridade.
        """
        cargo = "Diretor de TI"
        cv = """
        Direção de TI, gestão de equipes, supervisão de projetos.
        """
        
        should_skip, reason = _should_skip_gap_for_senior("Python", cargo, cv)
        assert should_skip is False
        
        should_skip, reason = _should_skip_gap_for_senior("AWS", cargo, cv)
        assert should_skip is False
        
    def test_strategic_indicators_pt(self):
        """Testa detecção de indicadores estratégicos em português."""
        cargo = "Gerente de Marketing"
        
        cvs_estrategicos = [
            "Gestão de equipe de marketing digital",
            "Coordenação de campanhas B2B",
            "Liderança de time de 15 pessoas",
            "Implementação de estratégia de conteúdo",
            "Direção da área de comunicação",
            "Supervisão de agências externas"
        ]
        
        for cv in cvs_estrategicos:
            should_skip, _ = _should_skip_gap_for_senior("Outreach", cargo, cv)
            assert should_skip is True, f"Deveria pular gap para CV: {cv[:50]}..."
            
    def test_strategic_indicators_en(self):
        """Testa detecção de indicadores estratégicos em inglês."""
        cargo = "Head of Sales"
        
        cvs_estrategicos = [
            "Team management and strategy implementation",
            "Sales operations leadership",
            "Revenue operations oversight",
            "Strategic planning and execution"
        ]
        
        for cv in cvs_estrategicos:
            should_skip, _ = _should_skip_gap_for_senior("Gong", cargo, cv)
            assert should_skip is True, f"Deveria pular gap para CV: {cv[:50]}..."


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_empty_inputs(self):
        """Testa comportamento com inputs vazios."""
        should_skip, reason = _should_skip_gap_for_senior("", "Gerente", "CV text")
        assert should_skip is False
        
        should_skip, reason = _should_skip_gap_for_senior("Outreach", "", "CV text")
        assert should_skip is False
        
        should_skip, reason = _should_skip_gap_for_senior("Outreach", "Gerente", "")
        assert should_skip is False
        
    def test_mixed_case_inputs(self):
        """Testa que funções são case-insensitive."""
        cargo = "GERENTE DE VENDAS"
        cv = "GESTÃO DE EQUIPE E COORDENAÇÃO"
        
        should_skip, _ = _should_skip_gap_for_senior("OUTREACH", cargo, cv)
        assert should_skip is True
        
    def test_special_characters(self):
        """Testa que caracteres especiais não quebram a detecção."""
        cargo = "Gerente de Vendas & Marketing"
        cv = "Gestão de equipe, coordenação..."
        
        should_skip, _ = _should_skip_gap_for_senior("Outreach.io", cargo, cv)
        assert should_skip is True
