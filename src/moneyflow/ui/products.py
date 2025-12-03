# src/moneyflow/ui/products.py — с иконками магазинов!
import flet as ft
from src.moneyflow.repositories.product_repo import get_all_products, get_price_history, add_price_manually
from src.moneyflow.db import get_session


class ProductsView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, padding=10)
        self.page = page

        self.search_field = ft.TextField(
            hint_text="Поиск товара...",
            expand=True,
            on_change=lambda e: page.run_task(self.filter_products),
        )

        self.products_list = ft.ListView(expand=True, spacing=8)

        self.content = ft.Column([
            ft.Row([
                ft.Text("Товары", size=26, weight=ft.FontWeight.BOLD),
                self.search_field
            ]),
            self.products_list,
        ], spacing=15)

        page.run_task(self.load_products)

    async def load_products(self, search: str = ""):
        self.products_list.controls.clear()
        async for session in get_session():
            products = await get_all_products(session)

        for product in products:
            if search and search.lower() not in product.name.lower():
                continue

            self.products_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.LOCAL_GROCERY_STORE, size=32),
                    title=ft.Text(product.name, size=20, weight=ft.FontWeight.W_500),
                    subtitle=ft.Text("Нажмите, чтобы посмотреть цены", color=ft.colors.ON_SURFACE_VARIANT),
                    trailing=ft.Icon(ft.icons.ARROW_FORWARD_IOS),
                    on_click=lambda e, pid=product.id, name=product.name: self.page.run_task(
                        self.open_product_detail, str(pid), name
                    ),
                )
            )
        self.page.update()

    async def filter_products(self):
        await self.load_products(self.search_field.value)

    async def open_product_detail(self, product_id: str, product_name: str):
        history = []
        async for session in get_session():
            history = await get_price_history(session, product_id)

        if not history:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("История цен пуста")))
            return

        # График
        chart_data = ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(x=i + 1, y=float(entry.price))
                for i, (entry, _, _) in enumerate(history)
            ],
            color=ft.colors.BLUE_400,
            stroke_width=4,
        )

        chart = ft.LineChart(
            data_series=[chart_data],
            expand=True,
            min_y=0,
            max_y=None,
            tooltip_bgcolor=ft.colors.with_opacity(0.9, ft.colors.BLUE_900),
            left=ft.ChartAxis(labels=[]),
            bottom=ft.ChartAxis(labels=[
                ft.ChartAxisLabel(value=i + 1, label=ft.Text(entry.date.strftime("%d.%m")))
                for i, (entry, _, _) in enumerate(history[-7:])  # последние 7 точек
            ]),
        )

        # Таблица с иконками!
        rows = []
        for entry, shop_name, shop_icon in history:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Row([
                        ft.Icon(name=shop_icon or "store", size=20),
                        ft.Text(shop_name)
                    ])),
                    ft.DataCell(ft.Text(entry.date.strftime("%d.%m.%Y"))),
                    ft.DataCell(ft.Text(f"{float(entry.price):.2f} ₽", weight=ft.FontWeight.BOLD)),
                ])
            )

        price_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Магазин")),
                ft.DataColumn(ft.Text("Дата")),
                ft.DataColumn(ft.Text("Цена")),
            ],
            rows=rows,
            expand=True,
        )


        # Форма добавления цены
        shop_field = ft.TextField(label="Магазин", hint_text="Пятерочка, Магнит, DNS...")
        price_field = ft.TextField(label="Цена", keyboard_type=ft.KeyboardType.NUMBER)

        dlg = ft.AlertDialog(
            title=ft.Text(product_name, size=24, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Container(chart, height=220, padding=10),
                ft.Container(price_table, expand=True),
                ft.Divider(),
                ft.Text("Добавить цену", size=18, weight=ft.FontWeight.BOLD),
                shop_field,
                price_field,
                ft.ElevatedButton(
                    "Сохранить",
                    icon=ft.icons.SAVE,
                    on_click=lambda e, pid=product_id, name=product_name: self.page.run_task(
                        self.save_new_price, 
                        pid,
                        shop_field.value,
                        price_field.value,
                        dlg,
                        name
                    )
                ),
            ], scroll=ft.ScrollMode.AUTO, expand=True),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: self.page.close(dlg))],
        )
        self.page.open(dlg)

    async def save_new_price(self, product_id: str, shop_name: str, price_str: str, dlg, product_name: str):
        if not shop_name or not price_str:
            return
        try:
            price = float(price_str)
        except ValueError:
            return

        async for session in get_session():
            await add_price_manually(session, product_id, shop_name, price)

        self.page.close(dlg)
        self.page.show_snack_bar(ft.SnackBar(ft.Text("Цена сохранена!"), bgcolor=ft.colors.GREEN))

        # ← Просто переоткрываем с тем же именем — оно у нас уже есть!
        await self.open_product_detail(product_id, product_name)

