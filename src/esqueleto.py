try:
    from src.inimigo import Esqueleto
except ModuleNotFoundError:
    from inimigo import Esqueleto

__all__ = ["Esqueleto"]
