#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List, Type

from nicegui import ui

from forms import faab, pick, player
from schemas import FAAB, Pick, Player, Asset


@dataclass
class FormState:
    player = False
    pick = False
    faab = False

    on_change: Callable

    player_fields = Player()
    pick_fields = Pick()
    faab_fields = FAAB()

    assets: List[Asset] = field(default_factory=list)

    def reset_form(self, asset_type: Type[Asset]):
        if asset_type == Player:
            self.player = False
            self.player_fields = Player()
        if asset_type == Pick:
            self.pick = False
            self.pick_fields = Pick()
        if asset_type == FAAB:
            self.faab = False
            self.faab_fields = FAAB()

    def new_player_form(self):
        self.player = True
        self.reset_form(Pick)
        self.reset_form(FAAB)
        self.on_change()

    def new_pick_form(self):
        self.pick = True
        self.reset_form(Player)
        self.reset_form(FAAB)
        self.on_change()

    def new_faab_form(self):
        self.faab = True
        self.reset_form(Pick)
        self.reset_form(Player)
        self.on_change()

    def cancel_player_form(self):
        self.reset_form(Player)
        self.on_change()

    def cancel_pick_form(self):
        self.reset_form(Pick)
        self.on_change()

    def cancel_faab_form(self):
        self.reset_form(FAAB)
        self.on_change()

    def assets_add_player(self):
        self.assets.append(self.player_fields)
        self.reset_form(type(self.player_fields))
        self.on_change()


@ui.refreshable
def enter_trade_ui():
    ui.label('Enter a trade asset.').classes('mx-auto')
    with ui.dropdown_button(text='select asset type', auto_close=True):
        ui.item(text='faab', on_click=form_state.new_faab_form)
        ui.item(text='pick', on_click=form_state.new_pick_form)
        ui.item(text='player', on_click=form_state.new_player_form)

    faab.faab_form(form_state)
    pick.pick_form(form_state)
    player.player_form(form_state)


form_state = FormState(on_change=enter_trade_ui.refresh)

with ui.card().classes('w-80 items-stretch'):
    ui.label(text='Trade Package Builder').classes('text-semibold text-2xl')
    enter_trade_ui()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
