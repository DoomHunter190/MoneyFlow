import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

def run_command(cmd: list[str]):
    result = subprocess.run(cmd,
                            cwd=PROJECT_ROOT,
                            capture_output=True,
                            text=True
                            )
    if result.returncode != 0:
        print(f'Ошибка: {result.stderr.strip()}')
        sys.exit(result.returncode)
    else:
        print(result.stdout.strip())


def up():
    print('Запуск БД...')
    run_command(['docker-compose', 'up', '-d'])


def down():
    print('Останавливаем БД...')
    run_command(['docker-compose', 'down'])

def restart():
    print('Перезапускаем БД...')
    down()
    up()