"""
Test to verify that chat.py doesn't have local import issues that cause UnboundLocalError.

This test ensures that the fix for the UnboundLocalError in ui/chat.py is working correctly.
The bug was caused by a local import of chamar_gpt_com_telemetria inside the fase_chat function
which shadowed the global import and caused UnboundLocalError on earlier references.
"""

import pytest
import ast
import os


def test_no_local_import_shadowing_in_fase_chat():
    """
    Verify that fase_chat() doesn't have local imports that shadow global imports.
    
    This test checks that chamar_gpt_com_telemetria and CONTEXTO_OUTROS are not
    imported locally inside the fase_chat function, which would cause UnboundLocalError.
    """
    # Read the chat.py file
    chat_file = os.path.join(os.path.dirname(__file__), '..', 'ui', 'chat.py')
    with open(chat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the AST
    tree = ast.parse(content)
    
    # Find the fase_chat function
    fase_chat_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'fase_chat':
            fase_chat_func = node
            break
    
    assert fase_chat_func is not None, "fase_chat function not found in ui/chat.py"
    
    # Check for local imports inside fase_chat
    local_imports = []
    for node in ast.walk(fase_chat_func):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Get the names being imported
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    local_imports.append(alias.name)
    
    # Verify that chamar_gpt_com_telemetria and CONTEXTO_OUTROS are not locally imported
    assert 'chamar_gpt_com_telemetria' not in local_imports, \
        "chamar_gpt_com_telemetria should not be imported locally in fase_chat()"
    assert 'CONTEXTO_OUTROS' not in local_imports, \
        "CONTEXTO_OUTROS should not be imported locally in fase_chat()"


def test_global_imports_exist():
    """
    Verify that chamar_gpt_com_telemetria and CONTEXTO_OUTROS are imported globally.
    """
    # Read the chat.py file
    chat_file = os.path.join(os.path.dirname(__file__), '..', 'ui', 'chat.py')
    with open(chat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the AST
    tree = ast.parse(content)
    
    # Find global imports (before any function definitions)
    global_imports = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            if node.module == 'core.gpt_telemetry':
                for alias in node.names:
                    global_imports.append(alias.name)
        # Stop at the first function definition
        if isinstance(node, ast.FunctionDef):
            break
    
    # Verify that the required imports exist globally
    assert 'chamar_gpt_com_telemetria' in global_imports, \
        "chamar_gpt_com_telemetria should be imported globally"
    assert 'CONTEXTO_OUTROS' in global_imports or 'CONTEXTO_DIAGNOSTICO' in global_imports, \
        "CONTEXTO_* constants should be imported globally"


def test_chat_module_imports_without_error():
    """
    Verify that the chat module can be imported without errors.
    
    This is a basic smoke test to ensure the module doesn't have syntax errors
    or import issues.
    """
    try:
        from ui.chat import fase_chat
        assert callable(fase_chat), "fase_chat should be a callable function"
    except Exception as e:
        pytest.fail(f"Failed to import ui.chat: {e}")
