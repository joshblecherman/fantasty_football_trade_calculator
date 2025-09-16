#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List

from nicegui import ui

from typing import Type


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


@dataclass
class FAAB:
    pass


assetType = Type[Pick] | Type[Player] | Type[FAAB]


@dataclass
class TradeAssets:
    title: str
    on_change: Callable
    items: List[assetType] = field(default_factory=list)

    def add(self, asset: assetType) -> None:
        self.items.append(asset)
        self.on_change()

    def remove(self, asset: assetType) -> None:
        self.items.remove(asset)
        self.on_change()


@ui.refreshable
def enter_trade_ui():
    ui.label('Enter a trade asset.').classes('mx-auto')
    # TODO, generate a form for each of the below 'assets'
    # with ui.dropdown_button(text='select asset type', auto_close=True):
    #     ui.item(text='player', on_click=lambda: trade_assets.add(asset_type=Player))
    #     ui.item(text='pick', on_click=lambda: trade_assets.add(asset_type=Pick))
    #     ui.item(text='player', on_click=lambda: trade_assets.add(asset_type=FAAB))
    for item in trade_assets.items:
        with ui.row().classes('items-center'):
            ui.input(value=str(item.type)).classes('flex-grow').bind_value(item, 'name')
            ui.button(on_click=lambda item=item: trade_assets.remove(item), icon='delete') \
                .props('flat fab-mini color=grey')


trade_assets = TradeAssets('Sending', on_change=enter_trade_ui.refresh)

with ui.card().classes('w-80 items-stretch'):
    ui.label().bind_text_from(trade_assets, 'title').classes('text-semibold text-2xl')
    enter_trade_ui()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
