#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Callable

from nicegui import ui

from forms import faab, pick, player
from schemas import FAAB, Pick, Player


@dataclass
class AssetSelection:
    player = False
    pick = False
    faab = False
    on_change: Callable

    player_fields = Player()
    pick_fields = Pick()
    faab_fields = FAAB()

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

    def cancel_player(self):
        self.player = False
        self.on_change()

    def cancel_pick(self):
        self.pick = False
        self.on_change()

    def cancel_faab(self):
        self.faab = False
        self.on_change()


@ui.refreshable
def enter_trade_ui():
    ui.label('Enter a trade asset.').classes('mx-auto')
    with ui.dropdown_button(text='select asset type', auto_close=True):
        ui.item(text='faab', on_click=asset_selection.new_faab)
        ui.item(text='pick', on_click=asset_selection.new_pick)
        ui.item(text='player', on_click=asset_selection.new_player)

    faab.faab_form(asset_selection)
    pick.pick_form(asset_selection)
    player.player_form(asset_selection)


asset_selection = AssetSelection(on_change=enter_trade_ui.refresh)

with ui.card().classes('w-80 items-stretch'):
    ui.label(text='Trade Package Builder').classes('text-semibold text-2xl')
    enter_trade_ui()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
