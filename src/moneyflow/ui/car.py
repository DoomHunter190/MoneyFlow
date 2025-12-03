import flet as ft

class CarView(ft.Container):
    def __init__(self, page): super().__init__(ft.Text("Авто — скоро!", size=30), expand=True, alignment=ft.alignment.center)
