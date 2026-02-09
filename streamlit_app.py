"""
Nobile Protocol — Entry Point Redirect

O entry point principal do Protocolo Nóbile é app.py.
Este arquivo existe apenas para compatibilidade com Streamlit Cloud,
que procura streamlit_app.py por padrão.
"""

import runpy
import sys
import os

# Garantir que o diretório atual está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Executar app.py como módulo principal
runpy.run_path("app.py", run_name="__main__")
