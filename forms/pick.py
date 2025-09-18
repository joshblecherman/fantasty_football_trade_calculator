from nicegui import ui


@ui.refreshable
def form(asset_selection):
    with ui.row().classes('items-center').bind_visibility(asset_selection, 'pick') as row:
        ui.input(value=str("Enter a pick")).classes('flex-grow')
        ui.button(icon='delete', on_click=asset_selection.remove_pick).props('flat fab-mini color=grey')

    return row
