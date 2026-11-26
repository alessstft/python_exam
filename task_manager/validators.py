from __future__ import annotations

from .constants import PRIORITY_NAMES

YES_ANSWERS = {"y", "yes", "д", "да"}
NO_ANSWERS = {"n", "no", "н", "нет"}


def read_title(prompt: str = "Название задачи: ") -> str:
    while True:
        title = input(prompt).strip()
        if title:
            return title
        print("Ошибка: название задачи не может быть пустым.")


def read_priority(
    prompt: str = "Приоритет (1 - низкий, 2 - средний, 3 - высокий): ",
) -> int:
    while True:
        raw = input(prompt).strip()
        if raw in {"1", "2", "3"}:
            return int(raw)
        if not raw.isdigit():
            print("Ошибка: приоритет должен быть числом 1, 2 или 3.")
        else:
            print("Ошибка: такого приоритета нет. Допустимо: 1, 2 или 3.")


def read_id(prompt: str = "ID задачи: ") -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: ID должен быть целым числом. Попробуйте ещё раз.")


def read_yes_no(prompt: str = "Подтвердите действие (y/n): ") -> bool:
    while True:
        raw = input(prompt).strip().lower()
        if raw in YES_ANSWERS:
            return True
        if raw in NO_ANSWERS:
            return False
        print("Ошибка: введите 'y' (да) или 'n' (нет).")


def priority_label(priority: int) -> str:
    return PRIORITY_NAMES.get(priority, str(priority))
