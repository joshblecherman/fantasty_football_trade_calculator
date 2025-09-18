from nicegui import ui


@ui.refreshable
def form(asset_selection):
    with ui.row().classes('items-center').bind_visibility(asset_selection, 'player') as row:
        ui.input(value=str("Enter a player")).classes('flex-grow')
        ui.button(icon='delete', on_click=asset_selection.remove_player).props('flat fab-mini color=grey')

    return row
