from dataclasses import dataclass


@dataclass
class TradeAsset:
    # either 'A' or 'B'
    side: str = None


@dataclass
class Player(TradeAsset):
    name: str = None
    projected_points: float = None
    years_kept: int = None
    games_remaining: int = None


@dataclass
class Pick(TradeAsset):
    # round == 1 is picks 1-6, round == 2 is picks 7-12
    # from there, count increases with each round
    round: int = None
    pick: int = None


@dataclass
class FAAB(TradeAsset):
    pass


Asset = Pick | Player | FAAB
