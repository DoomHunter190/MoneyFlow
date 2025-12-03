import flet as ft
from sqlalchemy import text
from moneyflow.db import get_session


async def check_database_connection(page: ft.Page) -> None:
    """
    Проверяет подключение к базе и показывает Snackbar.
    Вызывается один раз при старте приложения.
    """
    try:
        async for session in get_session():
            await session.execute(text('SELECT 1'))
            # complete
            snack = ft.SnackBar(
                content=ft.Text('Подключено к базе! Connected', color=ft.colors.GREEN_100),
                bgcolor=ft.colors.GREEN_800,
                action=ft.TextButton('OK', on_click=lambda e: snack.close()),
            )
    except Exception as exc:
        snack = ft.SnackBar(
            content=ft.Text(f'Нет связи с базой: {exc}', color=ft.colors.RED_100),
            bgcolor=ft.colors.RED_800,
            duration=10000, # 10 секунд
            action=ft.TextButton('Повторить', on_click=lambda e: page.run_task(check_database_connection, page)),

        )
    
    # Показываем SnackBar
    page.snack_bar = snack
    snack.open = True
    page.update()