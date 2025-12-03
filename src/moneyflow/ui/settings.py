import flet as ft

class SettingsView(ft.Container):
    def __init__(self, page): super().__init__(ft.Text("Настройки — скоро!", size=30), expand=True, alignment=ft.alignment.center)
