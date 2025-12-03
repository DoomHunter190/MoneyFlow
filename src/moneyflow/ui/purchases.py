import flet as ft
from src.moneyflow.repositories.purchase_repo import (
    get_planned_purchases, add_planned_purchase,
    toggle_planned, get_last_price_for_product
)
from src.moneyflow.db import get_session


class PurchasesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, padding=ft.padding.symmetric(10, 15))

        self.page = page
        self.textfield = ft.TextField(
            hint_text="Что нужно купить?..",
            expand=True,
            autofocus=True,
            on_submit=lambda e: page.run_task(self.add_item),
        )
        self.add_btn = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE_OUTLINE,
            icon_size=42,
            tooltip="Добавить в список",
            on_click=lambda e: page.run_task(self.add_item),
        )

        self.list_view = ft.ListView(expand=True, spacing=10)
        self.total_text = ft.Text("Итого: 0.00 ₽", size=22, weight=ft.FontWeight.BOLD)

        self.content = ft.Column([
            ft.Row([self.textfield, self.add_btn]),
            self.list_view,
            ft.Container(self.total_text, alignment=ft.alignment.center),
        ])

        self.page.run_task(self.on_mount)

    async def on_mount(self):
        # Загружаем при открытии
        await self.refresh_list()

    async def add_item(self):
        name = self.textfield.value.strip()
        if not name:
            return

        async for session in get_session():
            last_price = await get_last_price_for_product(session, name)

        price = last_price or 0.0
        await self.show_add_dialog(name, price)

    async def show_add_dialog(self, name: str, suggested_price: float):
        price_field = ft.TextField(
            label="Цена", value=str(suggested_price) if suggested_price else "",
            keyboard_type=ft.KeyboardType.NUMBER, width=140
        )
        qty_field = ft.TextField(label="Кол-во", value="1", width=100)

        dlg = ft.AlertDialog(
            title=ft.Text(f"Добавляем: {name}", weight=ft.FontWeight.BOLD),
            content=ft.Column([price_field, qty_field], tight=True),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.page.close(dlg)),
                ft.TextButton("Добавить", on_click=lambda e: self.page.run_task(
                    self.confirm_add, name, price_field.value, qty_field.value, dlg
                )),
            ],
        )
        self.page.open(dlg)

    async def confirm_add(self, name: str, price_str: str, qty_str: str, dlg):
        self.page.close(dlg)
        try:
            price = float(price_str or 0)
            qty = float(qty_str or 1)
        except ValueError:
            return

        async for session in get_session():
            await add_planned_purchase(session, name, price, qty)

        self.textfield.value = ""
        await self.refresh_list()

    async def refresh_list(self):
        self.list_view.controls.clear()
        total = 0.0

        async for session in get_session():
            purchases = await get_planned_purchases(session)

        for purchase, product_name in purchases:
            cost = float(purchase.price_at_purchase) * float(purchase.quantity)
            total += cost
            checkbox = ft.Checkbox(
                value=purchase.is_planned,
                on_change=lambda e, pid=purchase.id: self.page.run_task(
                    self.toggle_item, pid, e.control.value  # ← e.control.value = новое состояние
                ),
            )

            row = ft.ListTile(
                leading=checkbox,
                title=ft.Text(product_name, size=18),
                subtitle=ft.Text(f"{purchase.quantity} × {purchase.price_at_purchase} ₽"),
                trailing=ft.Text(f"{cost:.2f} ₽", weight=ft.FontWeight.BOLD),
            )

            if not purchase.is_planned:
                row.title.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
                row.opacity = 0.6

            self.list_view.controls.append(row)

        self.total_text.value = f"Итого: {total:.2f} ₽"
        self.page.update()

    async def toggle_item(self, purchase_id: int, is_planned: bool):
            async for session in get_session():
                await toggle_planned(session, purchase_id, is_planned)  # снимаем галочку
            await self.refresh_list()

