from scripts.db import up
import src.moneyflow.main as main
import flet as ft

def start():
    up()
    print('Запускаем приложение...')
    ft.app(target=main)


def dev():
    up()
    print('Режим разработки...')
    ft.app(target=main)