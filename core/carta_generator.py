from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

def gerar_carta_apresentacao(
    dados_candidato: Dict,
    dados_vaga: Dict,
    estilo: str = "formal"
) -> str:
    """
    Gera carta de apresentação personalizada.
    
    Args:
        dados_candidato: Dict com nome, cargo_atual, experiencias, realizacoes
        dados_vaga: Dict com empresa, cargo, descricao, requisitos
        estilo: "formal", "descontraido", ou "tech"
    
    Returns:
        str: Carta formatada em markdown
    """
    logger.info(f"Gerando carta de apresentação - Estilo: {estilo}")
    
    # Template base
    templates = {
        "formal": {
            "abertura": "Prezado(a) Recrutador(a),",
            "apresentacao": "Venho por meio desta candidatar-me à vaga de {cargo} na {empresa}.",
            "conexao": "Com {anos} anos de experiência em {area}, acredito que meu perfil se alinha perfeitamente aos requisitos da posição.",
            "fechamento": "Agradeço pela atenção e coloco-me à disposição para uma entrevista.\n\nAtenciosamente,"
        },
        "descontraido": {
            "abertura": "Olá!",
            "apresentacao": "Vi a vaga para {cargo} na {empresa} e fiquei animado(a) em me candidatar.",
            "conexao": "Nos últimos {anos} anos, tenho trabalhado com {area} e acredito que posso contribuir bastante com o time.",
            "fechamento": "Fico à disposição para conversarmos mais!\n\nAbraço,"
        },
        "tech": {
            "abertura": "Hi there!",
            "apresentacao": "I'm applying for the {cargo} position at {empresa}.",
            "conexao": "With {anos} years building solutions in {area}, I'm confident I can deliver impact from day one.",
            "fechamento": "Looking forward to connecting!\n\nBest regards,"
        }
    }
    
    template = templates.get(estilo, templates["formal"])
    
    # Extrai informações
    nome = dados_candidato.get('nome', '[SEU NOME]')
    cargo_atual = dados_candidato.get('cargo_atual', '')
    anos_exp = dados_candidato.get('anos_experiencia', 'X')
    area = dados_candidato.get('area_atuacao', 'minha área')
    realizacoes = dados_candidato.get('realizacoes', [])
    
    empresa = dados_vaga.get('empresa', '[EMPRESA]')
    cargo = dados_vaga.get('cargo', '[CARGO]')
    requisitos = dados_vaga.get('requisitos', [])
    
    # Monta carta
    carta = f"""# Carta de Apresentação

{template['abertura']}

{template['apresentacao'].format(cargo=cargo, empresa=empresa)}

{template['conexao'].format(anos=anos_exp, area=area)}

## Minhas Principais Realizações

"""
    
    # Adiciona top 3 realizações
    for i, realizacao in enumerate(realizacoes[:3], 1):
        carta += f"{i}. {realizacao}\n"
    
    # Match com requisitos da vaga
    if requisitos:
        carta += f"\n## Por que sou o(a) candidato(a) ideal\n\n"
        for req in requisitos[:3]:
            carta += f"**{req}:** [Explique como você atende este requisito]\n\n"
    
    carta += f"\n{template['fechamento']}\n\n**{nome}**\n"
    
    if cargo_atual:
        carta += f"*{cargo_atual}*\n"
    
    logger.info("Carta de apresentação gerada com sucesso")
    return carta
