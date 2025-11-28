import flet as ft
from src.config import settings
from src.db import get_session  
from src.ui.dashboard import DashboardView
from src.ui.purchases import PurchasesView
from src.ui.subscriptions import SubscriptionsView
from src.ui.car import CarView
from src.ui.settings import SettingsView
from sqlalchemy import text


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
                ft.IconButton(icon=ft.icons.SUBSCRIPTIONS, selected=False, on_click=lambda e: change_tab(2)),
                ft.IconButton(icon=ft.icons.DIRECTIONS_CAR, selected=False, on_click=lambda e: change_tab(3)),
                ft.IconButton(icon=ft.icons.SETTINGS, selected=False, on_click=lambda e: change_tab(4)),
            ],
        ),
    )

    # Список экранов
    views = [
        DashboardView(page),
        PurchasesView(page),
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

    # Проверка подключения к базе
    async def check_db():
        try:
            async for session in get_session():  
                await session.execute(text("SELECT 1"))
                # Создаём Snackbar и добавляем в page (чтобы избежать Offstage ошибки)
                snack = ft.SnackBar(
                    content=ft.Text("Подключено к базе! 🟢", color=ft.colors.GREEN_100),
                    bgcolor=ft.colors.GREEN_800,
                )
                page.snack_bar = snack  
                snack.open = True
                page.update()
        except Exception as exc:
            snack = ft.SnackBar(
                content=ft.Text(f"Нет связи с базой: {exc}", color=ft.colors.RED_100),
                bgcolor=ft.colors.RED_800,
            )
            page.snack_bar = snack
            snack.open = True
            page.update()

    # Запускаем async-задачу
    page.run_task(check_db)


if __name__ == "__main__":
    ft.app(target=main)
