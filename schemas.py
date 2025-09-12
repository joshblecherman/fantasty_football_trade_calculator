from dataclasses import dataclass

@dataclass
class Player:
    name: str
    projected_points: float
    years_kept: int
    games_remaining: int


@dataclass
class Pick:
    # round == 1 is picks 1-6, round == 2 is picks 7-12
    # from there, count increases with each round
    round: int
    pick: int = None
