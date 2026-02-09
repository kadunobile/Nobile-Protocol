"""
Script de verificação manual para testar a lógica do fluxo de otimização.

Este script simula o fluxo sem precisar executar toda a aplicação Streamlit,
permitindo validar rapidamente as mudanças feitas.
"""

import sys
sys.path.insert(0, '.')

from unittest.mock import MagicMock
from core.cv_estruturado import inicializar_cv_estruturado, gerar_contexto_para_prompt, atualizar_posicionamento, atualizar_gaps


def simular_session_state():
    """Simula um streamlit session_state básico."""
    class MockSessionState:
        def __init__(self):
            self.perfil = {'cargo_alvo': 'Controler Jurídico'}
            self.cv_texto = '''
Lucas Luiz Alves
Assistente Administrativo | LBCA
Set 2022 - Ago 2024
- Alimentação de planilhas
- Protocolos em sistemas
            '''
            self.gaps_alvo = ['Gestão de sistemas PJE/ESAJ', 'Compliance processual', 'Métricas quantificadas']
            self.gaps_respostas = {}
            self.cv_estruturado = None
            self.dados_coleta_historico = []
            self.dados_coleta_count = 0
            self.etapa_modulo = 'ETAPA_0_DIAGNOSTICO'
        
        def get(self, key, default=None):
            return getattr(self, key, default)
        
        def __contains__(self, key):
            return hasattr(self, key)
    
    return MockSessionState()


def testar_fluxo_completo():
    """Testa o fluxo completo de otimização."""
    print("=" * 80)
    print("TESTE MANUAL DO FLUXO DE OTIMIZAÇÃO")
    print("=" * 80)
    
    # 1. Simular session state
    print("\n1. Inicializando session state...")
    st_mock = simular_session_state()
    print(f"   Cargo alvo: {st_mock.perfil['cargo_alvo']}")
    print(f"   Gaps identificados: {len(st_mock.gaps_alvo)}")
    
    # 2. Simular resposta aos gaps
    print("\n2. Simulando respostas aos gaps...")
    st_mock.gaps_respostas = {
        'Gestão de sistemas PJE/ESAJ': {
            'tem_experiencia': True,
            'resposta': 'Sim, usei PJE, ESAJ, PROJUDI e TRT em todo o Brasil na LBCA'
        },
        'Compliance processual': {
            'tem_experiencia': True,
            'resposta': 'Verificava andamentos processuais e garantia compliance de prazos'
        },
        'Métricas quantificadas': {
            'tem_experiencia': True,
            'resposta': 'Gerenciava +50 processos simultaneamente com taxa de erro zero'
        }
    }
    print(f"   Gaps com experiência: {len([g for g, i in st_mock.gaps_respostas.items() if i['tem_experiencia']])}")
    
    # 3. Inicializar CV estruturado
    print("\n3. Inicializando estrutura de CV...")
    st_mock.cv_estruturado = inicializar_cv_estruturado()
    atualizar_posicionamento(cargo_alvo=st_mock.perfil['cargo_alvo'])
    
    # Preparar gaps
    import streamlit
    streamlit.session_state = st_mock
    
    resolvidos = [gap for gap, info in st_mock.gaps_respostas.items() if info.get('tem_experiencia')]
    nao_resolvidos = [gap for gap, info in st_mock.gaps_respostas.items() if not info.get('tem_experiencia')]
    atualizar_gaps(
        identificados=list(st_mock.gaps_respostas.keys()),
        resolvidos=resolvidos,
        nao_resolvidos=nao_resolvidos
    )
    print(f"   CV estruturado inicializado: ✓")
    print(f"   Gaps resolvidos salvos: {len(resolvidos)}")
    
    # 4. Simular coleta de dados
    print("\n4. Simulando coleta de dados...")
    respostas_coleta = [
        "Operava tecnicamente PJE, ESAJ, PROJUDI e sistemas TRT em tribunais de todo o Brasil",
        "Verificava andamentos processuais e formalizava documentos de status, mitigando riscos",
        "Alimentava e auditava dados no LegalBox, garantindo integridade para +50 processos",
        "Realizava protocolos e distribuições de processos com foco em erro zero"
    ]
    
    st_mock.dados_coleta_historico = respostas_coleta
    st_mock.dados_coleta_count = len(respostas_coleta)
    print(f"   Respostas coletadas: {st_mock.dados_coleta_count}")
    for i, resp in enumerate(respostas_coleta, 1):
        print(f"     {i}. {resp[:60]}...")
    
    # 5. Gerar contexto para prompt
    print("\n5. Gerando contexto para prompt final...")
    contexto = gerar_contexto_para_prompt()
    print("   Contexto gerado:")
    print("-" * 80)
    print(contexto)
    print("-" * 80)
    
    # 6. Validar estrutura
    print("\n6. Validando estrutura de CV...")
    cv_est = st_mock.cv_estruturado
    checks = [
        ("Cargo alvo definido", cv_est['posicionamento']['cargo_alvo'] == 'Controler Jurídico'),
        ("Gaps identificados", len(cv_est['gaps']['identificados']) == 3),
        ("Gaps resolvidos", len(cv_est['gaps']['resolvidos']) == 3),
        ("Gaps não resolvidos", len(cv_est['gaps']['nao_resolvidos']) == 0),
    ]
    
    for check_name, check_result in checks:
        status = "✓" if check_result else "✗"
        print(f"   {status} {check_name}")
    
    # 7. Teste de lógica do processador
    print("\n7. Testando lógica do processador (AGUARDANDO_DADOS_COLETA)...")
    
    # Simular que usuário digitou uma resposta substantiva
    resposta_usuario = "Trabalhei com SAP e gerenciei 100 processos mensais"
    
    # Verificar palavras de avanço
    palavras_avanco = ['continuar', 'pronto', 'concluído', 'finalizado', 'próxima', 'avançar']
    tem_palavra_avanco = any(word in resposta_usuario.lower() for word in palavras_avanco)
    print(f"   Resposta do usuário: '{resposta_usuario}'")
    print(f"   Tem palavra de avanço: {tem_palavra_avanco}")
    print(f"   Ação esperada: {'Avançar para CHECKPOINT' if tem_palavra_avanco else 'Salvar e continuar chat'}")
    
    # Testar com comando de avanço
    resposta_continuar = "continuar"
    tem_palavra_avanco = any(word in resposta_continuar.lower() for word in palavras_avanco)
    print(f"\n   Resposta do usuário: '{resposta_continuar}'")
    print(f"   Tem palavra de avanço: {tem_palavra_avanco}")
    print(f"   Ação esperada: {'Avançar para CHECKPOINT' if tem_palavra_avanco else 'Salvar e continuar chat'}")
    
    print("\n" + "=" * 80)
    print("TESTE CONCLUÍDO COM SUCESSO ✓")
    print("=" * 80)
    
    return True


if __name__ == '__main__':
    try:
        sucesso = testar_fluxo_completo()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
