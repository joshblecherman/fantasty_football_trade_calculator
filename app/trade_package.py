from nicegui import ui
from schemas import Player


@ui.refreshable
def trade_package(trade_package_state):
    tree_nodes = list()
    for asset in trade_package_state.trade_package:
        if type(asset) == Player:
            tree_nodes.append(player_as_tree_obj(asset))

    tree = ui.tree(tree_nodes, label_key='id')
    tree.add_slot('default-body', '''
        <span :props="props">{{ props.node.description }}</span>
    ''')
    return tree


def player_as_tree_obj(player: Player) -> dict:
    return {
        'id': player.name, 'children': [
            {'id': 'Projected Points', 'description': player.projected_points},
            {'id': 'Years Kept', 'description': player.years_kept},
            {'id': 'Games Remaining', 'description': player.games_remaining},
        ]
    }
