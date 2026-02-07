from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

def gerar_perguntas_entrevista(cargo: str, nivel: str, area: str) -> Dict[str, List[str]]:
    """
    Gera perguntas típicas de entrevista por categoria.
    
    Args:
        cargo: Cargo alvo
        nivel: junior, pleno, senior, gerencial
        area: tech, vendas, marketing, rh, etc
    
    Returns:
        Dict com categorias e listas de perguntas
    """
    logger.info(f"Gerando perguntas para {cargo} - {nivel} - {area}")
    
    perguntas = {
        "Comportamentais": [],
        "Técnicas": [],
        "Situacionais": [],
        "Sobre a Empresa": []
    }
    
    # Comportamentais (universais)
    perguntas["Comportamentais"] = [
        "Fale sobre você e sua trajetória profissional",
        "Quais são seus pontos fortes e fracos?",
        "Por que você quer trabalhar aqui?",
        "Onde você se vê em 5 anos?",
        "Conte sobre um desafio que você superou",
        "Como você lida com feedback negativo?",
        "Descreva uma situação de conflito no trabalho e como resolveu"
    ]
    
    # Técnicas por área
    tecnicas_por_area = {
        "tech": [
            "Explique sua experiência com [tecnologia X]",
            "Como você aborda debugging de código complexo?",
            "Descreva sua arquitetura ideal para [tipo de sistema]",
            "Qual foi o projeto técnico mais desafiador que você trabalhou?",
            "Como você se mantém atualizado com novas tecnologias?"
        ],
        "vendas": [
            "Como você aborda um lead frio?",
            "Qual sua estratégia para fechar negócios grandes?",
            "Como você lida com objeções de preço?",
            "Conte sobre sua maior venda",
            "Como você gerencia seu pipeline?"
        ],
        "marketing": [
            "Como você mede ROI de campanhas?",
            "Qual sua experiência com [ferramenta de marketing]?",
            "Descreva uma campanha bem-sucedida que você liderou",
            "Como você segmenta audiências?",
            "Qual sua abordagem para growth hacking?"
        ],
        "gerencial": [
            "Como você motiva equipes desmotivadas?",
            "Qual seu estilo de liderança?",
            "Como você lida com underperformers?",
            "Descreva como você prioriza projetos conflitantes",
            "Como você desenvolve talentos no time?"
        ]
    }
    
    perguntas["Técnicas"] = tecnicas_por_area.get(area, [
        "Quais ferramentas você domina?",
        "Como você resolve problemas complexos?",
        "Conte sobre um projeto que você liderou"
    ])
    
    # Situacionais
    perguntas["Situacionais"] = [
        "Como você reagiria se um projeto seu fosse cancelado de última hora?",
        "Se você discordasse do seu gestor, o que faria?",
        "Como priorizaria tarefas urgentes conflitantes?",
        "O que você faria se descobrisse um erro crítico em produção?",
        "Como lidaria com um colega difícil de trabalhar?"
    ]
    
    # Sobre a empresa
    perguntas["Sobre a Empresa"] = [
        "O que você sabe sobre nossa empresa?",
        "Por que você quer este cargo especificamente?",
        "O que você acha que pode agregar aqui?",
        "Quais são suas expectativas para esta posição?",
        "Você tem alguma pergunta para nós?"
    ]
    
    return perguntas

def gerar_respostas_modelo(pergunta: str, cv_texto: str, cargo: str) -> str:
    """
    Gera resposta modelo baseada no CV do candidato.
    """
    # Implementação via GPT (será chamada pela UI)
    return ""
