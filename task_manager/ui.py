from __future__ import annotations

from typing import Any

from .constants import PRIORITY_NAMES, STATUS_DONE
from .validators import priority_label

LINE = "-" * 64
DOUBLE_LINE = "=" * 64

TITLE_WIDTH = 30


def print_header(loaded_count: int) -> None:
    print(DOUBLE_LINE)
    print("МЕНЕДЖЕР ЗАДАЧ".center(64))
    print("консольное приложение на Python".center(64))
    print(DOUBLE_LINE)
    if loaded_count:
        print(f"Загружено задач из tasks.json: {loaded_count}.")
    else:
        print("Список задач пуст. Добавьте первую задачу.")
    print()


def print_menu() -> None:
    print(LINE)
    print("ГЛАВНОЕ МЕНЮ")
    print("  1. Добавить задачу")
    print("  2. Показать задачи")
    print("  3. Найти задачу по ID")
    print("  4. Изменить статус")
    print("  5. Удалить задачу")
    print("  6. Статистика")
    print("  0. Сохранить и выйти")
    print(LINE)


def print_section(title: str) -> None:
    print(f"\n--- {title} ---")


def shorten(text: str, width: int = TITLE_WIDTH) -> str:
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def show_tasks(tasks: list[dict[str, Any]]) -> None:
    if not tasks:
        print("Список задач пуст.")
        return

    header = (
        f"{'ID':>3}  {'НАЗВАНИЕ':<{TITLE_WIDTH}}  "
        f"{'ПРИОРИТЕТ':<10}  {'СТАТУС':<10}"
    )
    print(header)
    print(LINE)
    for task in tasks:
        priority = PRIORITY_NAMES.get(task["priority"], str(task["priority"]))
        print(
            f"{task['id']:>3}  {shorten(task['title']):<{TITLE_WIDTH}}  "
            f"{priority:<10}  {task['status']:<10}"
        )

    done = sum(1 for task in tasks if task["status"] == STATUS_DONE)
    print(LINE)
    print(f"Всего: {len(tasks)} | Выполнено: {done} | Осталось: {len(tasks) - done}")


def show_task(task: dict[str, Any]) -> None:
    print("Найдена задача:")
    print(f"  ID: {task['id']}")
    print(f"  Название: {task['title']}")
    print(f"  Приоритет: {task['priority']} ({priority_label(task['priority'])})")
    print(f"  Статус: {task['status']}")


def show_statistics(total: int, done: int, remaining: int) -> None:
    print(f"Всего задач:   {total}")
    print(f"Выполнено:     {done}")
    print(f"Осталось:      {remaining}")
