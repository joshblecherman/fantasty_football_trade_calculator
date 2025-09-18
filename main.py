#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List

from nicegui import ui

from forms import faab, pick, player


@dataclass
class AssetSelection:
    player = False
    pick = False
    faab = False
    on_change: Callable

    def new_player(self):
        self.player = True
        self.pick = self.faab = False
        self.on_change()

    def new_pick(self):
        self.pick = True
        self.faab = self.player = False
        self.on_change()

    def new_faab(self):
        self.faab = True
        self.player = self.pick = False
        self.on_change()

    def remove_player(self):
        self.player = False
        self.on_change()

    def remove_pick(self):
        self.pick = False
        self.on_change()

    def remove_faab(self):
        self.faab = False
        self.on_change()


@dataclass
class Player:
    name: str = None
    projected_points: float = None
    years_kept: int = None
    games_remaining: int = None


@dataclass
class Pick:
    # round == 1 is picks 1-6, round == 2 is picks 7-12
    # from there, count increases with each round
    round: int
    pick: int = None


@dataclass
class FAAB:
    pass


Asset = Pick | Player | FAAB


@dataclass
class TradeAssets:
    title: str
    on_change: Callable
    items: List[Asset] = field(default_factory=list)

    def add(self, asset: Asset) -> None:
        self.items.append(asset)
        self.on_change()

    def remove(self, asset: Asset) -> None:
        self.items.remove(asset)
        self.on_change()


@ui.refreshable
def enter_trade_ui():
    ui.label('Enter a trade asset.').classes('mx-auto')
    # TODO, generate a form for each of the below 'assets'
    with ui.dropdown_button(text='select asset type', auto_close=True):
        ui.item(text='faab', on_click=asset_selection.new_faab)
        ui.item(text='pick', on_click=asset_selection.new_pick)
        ui.item(text='player', on_click=asset_selection.new_player)

    faab.form(asset_selection)
    pick.form(asset_selection)
    player.form(asset_selection)

        # ui.item(text='pick', on_click=lambda: trade_assets.add(asset_type=Pick))
        # ui.item(text='player', on_click=lambda: trade_assets.add(asset_type=FAAB))
    # for item in trade_assets.items:
    #     with ui.row().classes('items-center'):
    #         ui.input(value=str("Enter a player")).classes('flex-grow').bind_value(item, 'name')
    #         ui.button(on_click=lambda item=item: trade_assets.remove(item), icon='delete') \
    #             .props('flat fab-mini color=grey')


asset_selection = AssetSelection(on_change=enter_trade_ui.refresh)
trade_assets = TradeAssets('Sending', on_change=enter_trade_ui.refresh)

with ui.card().classes('w-80 items-stretch'):
    ui.label().bind_text_from(trade_assets, 'title').classes('text-semibold text-2xl')
    enter_trade_ui()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
