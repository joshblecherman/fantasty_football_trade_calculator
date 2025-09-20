from nicegui import ui


@ui.refreshable
def player_form(form_state):
    with ui.column().classes('items-stretch gap-4').bind_visibility(form_state, 'player') as row:
        ui.button(icon='delete', on_click=form_state.cancel_player_form) \
            .props('flat fab-mini color=grey')

        # Player name input
        ui.input(label="Player Name") \
            .bind_value_to(form_state.player_fields, 'name')

        # Projected points
        ui.number(label='Projected Points', precision=1).props('clearable') \
            .bind_value_to(form_state.player_fields, 'projected_points')

        # Games Remaining
        ui.number(label='Games Remaining', precision=0).props('clearable') \
            .bind_value_to(form_state.player_fields, 'games_remaining')

        # Years kept
        with ui.row().classes('items-center gap-2'):
            ui.label(text='Years kept')
            ui.radio([0, 1, 2, 3, 4]).props('inline') \
                .bind_value_to(form_state.player_fields, 'years_kept')

        ui.button(text='Submit', on_click=form_state.assets_add_player)

    return row
