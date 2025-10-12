#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List, Type

from nicegui import ui

from app.forms import pick, faab, player
from app import trade_package
from schemas import FAAB, Pick, Player, Asset


@dataclass
class TradePackageState:
    on_change: Callable

    trade_package: List[Asset] = field(default_factory=list)

    def add_asset(self, asset: Asset):
        self.trade_package.append(asset)
        self.on_change()


@dataclass
class FormState:
    on_change: Callable

    player = False
    pick = False
    faab = False

    def new_player_form(self):
        self.player = True
        self.pick = self.faab = False
        self.on_change()

    def new_pick_form(self):
        self.pick = True
        self.player = self.faab = False
        self.on_change()

    def new_faab_form(self):
        self.faab = True
        self.pick = self.player = False
        self.on_change()

    def cancel_player_form(self):
        self.player = False
        self.on_change()

    def cancel_pick_form(self):
        self.pick = False
        self.on_change()

    def cancel_faab_form(self):
        self.faab = False
        self.on_change()

    def reset(self):
        self.player = False
        self.pick = False
        self.faab = False

    def submit(self, asset: Asset):
        if asset.side == 'A':
            trade_package_state_A.add_asset(asset)
        elif asset.side == 'B':
            trade_package_state_B.add_asset(asset)
        self.reset()
        self.on_change()


@ui.refreshable
def enter_trade_ui():
    with ui.splitter().classes('full-width items-stretch') as splitter:
        with splitter.before:
            with ui.dropdown_button(text='select asset type', auto_close=True):
                ui.item(text='faab', on_click=form_state.new_faab_form)
                ui.item(text='pick', on_click=form_state.new_pick_form)
                ui.item(text='player', on_click=form_state.new_player_form)

            # faab.faab_form(form_state)
            # pick.pick_form(form_state)
            player.player_form(form_state)

        with splitter.after:
            with ui.splitter(horizontal=True).classes('full-width items-stretch') as splitter_trades:
                with splitter_trades.before:
                    with ui.card().classes('full-width items-stretch'):
                        ui.label('Package A')
                        trade_package.trade_package(trade_package_state_A)
                with splitter_trades.after:
                    with ui.card().classes('full-width items-stretch'):
                        ui.label('Package B')
                        trade_package.trade_package(trade_package_state_B)


form_state = FormState(on_change=enter_trade_ui.refresh)
trade_package_state_A = TradePackageState(on_change=enter_trade_ui.refresh)
trade_package_state_B = TradePackageState(on_change=enter_trade_ui.refresh)

with ui.header():
    ui.label('Trade Tool')

enter_trade_ui()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
