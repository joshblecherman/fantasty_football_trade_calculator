from typing import Iterable, List
from dataclasses import dataclass


@dataclass
class Player:
    name: str
    projected_points: float
    years_kept: int


class Pick:
    round: int
    values: List[int]=[]


def get_player(side) -> Player:
    msg_begin = f"[{side}] "
    name = get_valid_input(msg_begin + "player name > ", str)
    projected_points = get_valid_input(msg_begin + f"{name} projected points (remaining in season) > ", float)
    years_kept = get_valid_input(msg_begin + f"{name} years kept (0-4) > ", int, range(0, 5))
    return Player(name=name, projected_points=projected_points, years_kept=years_kept)


def get_pick():
    pass


def get_players(side) -> List[Player]:
    players = list()
    done = get_valid_input("done inputting players? (y/n) > ", chr, ("y", "Y", "n", "N"))
    while done not in ("y", "Y"):
        player = get_player(side)
        players.append(player)
        done = get_valid_input("done inputting players? (y/n) > ", chr, ("y", "Y", "n", "N"))
    return players


def get_valid_input(msg: str, cast_func: callable, accepted_values: Iterable = None):
    while True:
        try:
            value = cast_func(input(msg))
            if accepted_values is not None:
                assert value in accepted_values
            return value
        except ValueError:
            print(f"enter a valid {cast_func.__name__}")
            continue
        except AssertionError:
            print(f"please enter value in {accepted_values}")
            continue


def get_trade_value(side: str):
    assert side in ("sending", "receiving")
    players = get_players(side)
    # picks = get_picks(side) TODO
    # faab = get_faab(side) TODO


if __name__ == "__main__":
    get_trade_value("sending")
    get_trade_value("receiving")
