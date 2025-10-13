from dataclasses import dataclass
from abc import ABC


@dataclass
class Asset(ABC):
    # either 'A' or 'B'
    side: str = None
    value: float = None


@dataclass
class Player(Asset):
    name: str = None
    projected_points: float = None
    years_kept: int = None
    games_remaining: int = None


@dataclass
class Pick(Asset):
    # round == 1 is picks 1-6, round == 2 is picks 7-12
    # from there, count increases with each round
    round: int = None
    pick: int = None


@dataclass
class FAAB(Asset):
    pass
