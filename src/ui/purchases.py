import flet as ft

class PurchasesView(ft.Container):
    def __init__(self, page): super().__init__(ft.Text("Покупки — скоро!", size=30), expand=True, alignment=ft.alignment.center)
