import PySimpleGUI as sg
from warehouse_system import (
    companies,
    view_all_products_with_detailed_information,
    add_a_new_product,
    sell_product,
    find_the_supplier_with_the_highest_total_quantity_of_goods
)

layout = [...]
window = sg.Window(...)

while True:
    event, values = window.read()

window.close()
