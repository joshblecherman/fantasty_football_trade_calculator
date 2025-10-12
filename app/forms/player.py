from nicegui import ui
from schemas import Player


@ui.refreshable
def player_form(form_state):
    player = Player()

    # Years kept
    with ui.row().classes('items-center gap-2').bind_visibility(form_state, 'player'):
        ui.label(text='Trade Side')
        ui.radio(['A', 'B']).props('inline') \
            .bind_value_to(player, 'side')

    with ui.column().classes('items-stretch gap-4').bind_visibility(player, 'side') as row:
        ui.button(icon='delete', on_click=form_state.cancel_player_form) \
            .props('flat fab-mini color=grey')

        # Player name input
        ui.input(label="Player Name").bind_value_to(player, 'name')

        # Projected points
        ui.number(label='Projected Points', precision=1).props('clearable') \
            .bind_value_to(player, 'projected_points')

        # Games Remaining
        ui.number(label='Games Remaining', precision=0).props('clearable') \
            .bind_value_to(player, 'games_remaining')

        # Years kept
        with ui.row().classes('items-center gap-2'):
            ui.label(text='Years kept')
            ui.radio([0, 1, 2, 3, 4]).props('inline') \
                .bind_value_to(player, 'years_kept')

        ui.button(text='Submit', on_click=lambda: form_state.submit(player))

    return row
