from nicegui import ui


@ui.refreshable
def player_form(asset_selection):
    with ui.row().classes('flex-center').bind_visibility(asset_selection, 'player') as row:
        with ui.column().classes('items-start gap-4'):  # main vertical layout
            ui.button(icon='delete', on_click=asset_selection.cancel_player) \
                .props('flat fab-mini color=grey')

            # Player name input
            ui.input(value="Enter a player") \
                .bind_value_to(asset_selection.player_fields, 'name')

            # Projected points
            ui.number(label='Projected Points', precision=1).props('clearable') \
                .bind_value_to(asset_selection.player_fields, 'projected_points')

            # Years kept
            with ui.row().classes('items-center gap-2'):
                ui.label(text='Years kept')
                ui.radio([0, 1, 2, 3, 4]).props('inline') \
                    .bind_value_to(asset_selection.player_fields, 'years_kept')

    return row
