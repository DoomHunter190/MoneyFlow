import flet as ft


class DashboardView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1a1a2e", "#16213e"],
            ),
        )

        self.content = ft.Column(
            controls=[
                ft.Container(height=80),
                ft.Text(
                    "MoneyFlow",
                    size=42,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.INDIGO_400,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Твой личный финансовый центр",
                    size=18,
                    color=ft.colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=60),
                ft.Icon(ft.icons.AUTO_FIX_HIGH, size=120, color=ft.colors.INDIGO_300),
                ft.Container(height=40),
                ft.Text(
                    "Этап 2 завершён!\nБаза работает · Flet живой",
                    size=16,
                    color=ft.colors.GREEN_400,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
