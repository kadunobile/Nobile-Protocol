import os
import importlib

def setup_environment():
    try:
        cfg = importlib.import_module("config")
        if hasattr(cfg, "OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = cfg.OPENAI_API_KEY
    except Exception:
        pass

    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except Exception:
        pass
