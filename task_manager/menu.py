from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from . import service, storage, ui, validators
from .constants import DEFAULT_DATA_FILE

Task = dict[str, Any]
Action = Callable[[list[Task]], None]


def add_task_action(tasks: list[Task]) -> None:
    ui.print_section("ДОБАВЛЕНИЕ ЗАДАЧИ")
    title = validators.read_title()
    priority = validators.read_priority()
    task = service.add_task(tasks, title, priority)
    print(
        f"Готово: добавлена задача ID {task['id']} "
        f"(«{task['title']}», приоритет {task['priority']} - "
        f"{validators.priority_label(task['priority'])})."
    )


def show_tasks_action(tasks: list[Task]) -> None:
    ui.print_section("СПИСОК ЗАДАЧ")
    ui.show_tasks(tasks)


def find_task_action(tasks: list[Task]) -> None:
    ui.print_section("ПОИСК ЗАДАЧИ ПО ID")
    task_id = validators.read_id()
    task = service.find_task(tasks, task_id)
    if task is None:
        print(f"Задача с ID {task_id} не найдена.")
        return
    ui.show_task(task)


def change_status_action(tasks: list[Task]) -> None:
    ui.print_section("ИЗМЕНЕНИЕ СТАТУСА")
    task_id = validators.read_id()
    task = service.find_task(tasks, task_id)
    if task is None:
        print(f"Задача с ID {task_id} не найдена.")
        return
    old_status = task["status"]
    new_status = service.toggle_status(task)
    print(f"Задача «{task['title']}»: статус «{old_status}» -> «{new_status}».")


def delete_task_action(tasks: list[Task]) -> None:
    ui.print_section("УДАЛЕНИЕ ЗАДАЧИ")
    task_id = validators.read_id()
    task = service.find_task(tasks, task_id)
    if task is None:
        print(f"Задача с ID {task_id} не найдена.")
        return

    print(f"Вы собираетесь удалить задачу «{task['title']}» (ID {task['id']}).")
    if not validators.read_yes_no("Удалить задачу? (y/n): "):
        print("Удаление отменено.")
        return

    service.delete_task(tasks, task_id)
    print(f"Задача с ID {task_id} удалена.")


def statistics_action(tasks: list[Task]) -> None:
    """Пункт 6. Статистика по задачам."""
    ui.print_section("СТАТИСТИКА")
    total, done, remaining = service.get_statistics(tasks)
    ui.show_statistics(total, done, remaining)


ACTIONS: dict[str, Action] = {
    "1": add_task_action,
    "2": show_tasks_action,
    "3": find_task_action,
    "4": change_status_action,
    "5": delete_task_action,
    "6": statistics_action,
}


def run(data_file: Path | str = DEFAULT_DATA_FILE) -> None:
    file_path = Path(data_file)
    tasks = storage.load_tasks(file_path)

    ui.print_header(len(tasks))

    try:
        while True:
            ui.print_menu()
            try:
                choice = input("Ваш выбор: ").strip()
            except EOFError:
                print("\nВвод завершён. Сохраняем данные и выходим.")
                storage.save_tasks(tasks, file_path)
                return

            if choice == "0":
                if storage.save_tasks(tasks, file_path):
                    print(f"Данные сохранены в {file_path.name}. До встречи!")
                return

            action = ACTIONS.get(choice)
            if action is None:
                print(f"Ошибка: неизвестная команда «{choice}». Введите число от 0 до 6.")
                print()
                continue

            action(tasks)
            print()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота прервана. Сохраняем данные...")
        storage.save_tasks(tasks, file_path)
