from weights import *
from schemas import *
from typing import List


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


def get_pick_value(pick: Pick) -> float:
    return decay_future_value(PICK_VALUES[pick.round], 1, asset="pick")


def get_player_value(player: Player) -> float:
    player_value_base = player.projected_points
    player_value_current_season = player_value_base * (player.games_remaining / TOTAL_GAMES)
    if player_value_base <= REPLACEMENT_KEEPER_VALUE:
        return player_value_base  # no keeper value above typical replacement, return only current year value
    player_value = sum(
        [player_value_current_season] +
        [decay_future_value(player_value_base, years_into_future, asset="keeper")
            for years_into_future in range(1, player.years_kept + 1)]
    )
    return player_value


def get_faab_value(faab: FAAB) -> float:
    pass


def get_players_value(player_list: List[Player]):
    return sum([get_player_value(player) for player in player_list])


def get_picks_value(pick_list: List[Pick]):
    return sum([get_pick_value(pick) for pick in pick_list])


def get_asset_value(asset: Asset) -> float:
    if isinstance(asset, FAAB):
        return get_faab_value(asset)
    elif isinstance(asset, Player):
        return get_player_value(asset)
    elif isinstance(asset, Pick):
        return get_pick_value(asset)
