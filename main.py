from typing import Iterable, List
from dataclasses import dataclass
from weights import *


@dataclass
class Player:
    name: str
    projected_points: float
    years_kept: int


@dataclass
class Pick:
    # round == 1 is picks 1-6, round == 2 is picks 7-12
    # from there, count increases with each round
    round: int
    pick: int = None


def get_player(side) -> Player:
    msg_begin = f"[{side}] "
    name = get_valid_input(msg_begin + "player name > ", str)
    projected_points = get_valid_input(msg_begin + f"{name} projected points (remaining in season) > ", float)
    years_kept = get_valid_input(msg_begin + f"{name} years kept (0-4) > ", int, range(0, 5))
    return Player(name=name, projected_points=projected_points, years_kept=years_kept)


def get_pick(side):
    msg_begin = f"[{side}] "
    pick_round = get_valid_input(msg_begin + "round > ", int, range(1, 14))
    if pick_round == 1:
        top_6 = get_valid_input(
            msg_begin + "assume this round 1 pick will be top 6? (Y/n) > ", str, ("y", "Y", "n", "N")
        )
        if top_6 not in ("y", "Y"):
            # For these purposes, only top 6 pick is "round 1", 7-12 is "round 2"
            # Picks 13-24 are "round 3", 25-36 are "round 4", etc..
            pick_round += 1
    return Pick(round=pick_round)


def get_players(side) -> List[Player]:
    players = list()
    done = get_valid_input("done inputting players? (Y/n) > ", str, ("y", "Y", "n", "N"))
    while done not in ("y", "Y"):
        player = get_player(side)
        players.append(player)
        done = get_valid_input("done inputting players? (Y/n) > ", str, ("y", "Y", "n", "N"))
    return players


def get_picks(side) -> List[Pick]:
    picks = list()
    done = get_valid_input("done inputting picks? (Y/n) > ", str, ("y", "Y", "n", "N"))
    while done not in ("y", "Y"):
        pick = get_pick(side)
        picks.append(pick)
        done = get_valid_input("done inputting picks? (Y/n) > ", str, ("y", "Y", "n", "N"))
    return picks


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


def decay_future_value(value, years_into_future, asset: str):
    """
    When we depreciate picks, we apply this formula with no 'replacement_value.'
    With potential keepers, we have to subtract the value of the average 'replacement_keeper'
    """
    assert asset in ("keeper", "pick")
    if asset == "pick":
        return value * DECAY_FACTOR ** years_into_future
    return (
        value * DECAY_FACTOR ** years_into_future -
        REPLACEMENT_KEEPER_VALUE * DECAY_FACTOR ** years_into_future
    )


def get_pick_value(pick: Pick):
    return decay_future_value(PICK_VALUES[pick.round], 1, asset="pick")


def get_player_value(player: Player):
    player_value_base = player.projected_points
    if player_value_base <= REPLACEMENT_KEEPER_VALUE:
        return player_value_base  # no keeper value above typical replacement, return only current year value
    player_value = sum([
        decay_future_value(player_value_base, years_into_future, asset="keeper")
        for years_into_future in range(player.years_kept + 1)
    ])
    return player_value


def get_players_value(player_list: List[Player]):
    return sum([get_player_value(player) for player in player_list])


def get_picks_value(pick_list: List[Pick]):
    return sum([get_pick_value(pick) for pick in pick_list])


def get_trade_value(side: str):
    assert side in ("sending", "receiving")
    players = get_players(side)
    picks = get_picks(side)
    players_value = get_players_value(players)
    picks_value = get_picks_value(picks)
    print(f"players value is {players_value}")
    print(f"picks value is {picks_value}")


if __name__ == "__main__":
    get_trade_value("sending")
    get_trade_value("receiving")
