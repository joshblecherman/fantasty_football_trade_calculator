from nicegui import ui


@ui.refreshable
def faab_form(asset_selection):
    with ui.row().classes('items-center').bind_visibility(asset_selection, 'faab') as row:
        ui.input(value=str("Enter a faab value")).classes('flex-grow')
        ui.button(icon='delete', on_click=asset_selection.cancel_faab).props('flat fab-mini color=grey')

    return row
