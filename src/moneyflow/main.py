import flet as ft
from moneyflow.config import settings
from moneyflow.db_check import check_database_connection
from moneyflow.ui.dashboard import DashboardView
from moneyflow.ui.purchases import PurchasesView
from moneyflow.ui.subscriptions import SubscriptionsView
from moneyflow.ui.car import CarView
from moneyflow.ui.settings import SettingsView
from moneyflow.ui.products import ProductsView



def main(page: ft.Page):
    page.title = settings.APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 420 
    page.window.height = 840 
    page.padding = 0

    # --- Нижняя навигация ---
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.with_opacity(0.95, ft.colors.SURFACE_VARIANT),
        height=60,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(icon=ft.icons.HOME, selected=True, on_click=lambda e: change_tab(0)),
                ft.IconButton(icon=ft.icons.SHOPPING_CART, selected=False, on_click=lambda e: change_tab(1)),
                ft.IconButton(icon=ft.icons.STORE_MALL_DIRECTORY, selected=False, on_click=lambda e: change_tab(2)),
                ft.IconButton(icon=ft.icons.SUBSCRIPTIONS, selected=False, on_click=lambda e: change_tab(3)),
                ft.IconButton(icon=ft.icons.DIRECTIONS_CAR, selected=False, on_click=lambda e: change_tab(4)),
                ft.IconButton(icon=ft.icons.SETTINGS, selected=False, on_click=lambda e: change_tab(5)),
            ],
        ),
    )

    # Список экранов
    views = [
        DashboardView(page),
        PurchasesView(page),
        ProductsView(page),
        SubscriptionsView(page),
        CarView(page),
        SettingsView(page),
    ]

    current_index = 0

    def change_tab(index: int):
        nonlocal current_index
        if current_index == index:
            return
        current_index = index

        # Подсвечиваем активную иконку
        for i, btn in enumerate(page.bottom_appbar.content.controls):
            btn.selected = (i == index)
            btn.update()

        # Меняем контент
        page.controls.clear() 
        page.add(views[index])
        page.update()

    # Первый запуск
    change_tab(0)

    # Запускаем проверку подключения к БД
    page.run_task(check_database_connection, page)
