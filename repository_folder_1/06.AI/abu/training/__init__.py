"""Training module for data collection and model training"""

from .collector import GameDataCollector
from .trainer import Trainer
from .self_play import SelfPlayGenerator

__all__ = ['GameDataCollector', 'Trainer', 'SelfPlayGenerator']
