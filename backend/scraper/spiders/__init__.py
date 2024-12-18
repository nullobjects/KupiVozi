from .pazar3spider import Pazar3Spider
from .reklama5spider import Reklama5Spider
from .autoweltspider import AutoweltSpider
from .toyotaspider import ToyotaSpider
from .vozispider import VoziSpider
__all__ = ["Pazar3Spider", "Reklama5Spider", "VoziSpider"]
AVAILABLE_MODELS = [Pazar3Spider, Reklama5Spider, VoziSpider]