from nicegui import ui


@ui.refreshable
def player_form(asset_selection):
    with ui.row().classes('items-center').bind_visibility(asset_selection, 'player') as row:
        ui.button(icon='delete', on_click=asset_selection.cancel_player).props('fla fab-mini color=grey')

        ui.input(value=str("Enter a player")).classes('flex-grow') \
            .bind_value_to(asset_selection.player_fields, 'projected_points')
        ui.number(label='Projected Points', precision=1).props('clearable') \
            .bind_value_to(asset_selection.player_fields, 'projected_points')
        ui.radio([0, 1, 2, 3, 4], value=1).props('inline') \
            .bind_value_to(asset_selection.player_fields, 'years_kept')

    return row
