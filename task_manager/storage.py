from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import DEFAULT_DATA_FILE, STATUS_TODO, VALID_PRIORITIES, VALID_STATUSES


def load_tasks(path: Path | str = DEFAULT_DATA_FILE) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Предупреждение: не удалось прочитать {file_path.name} ({error}).")
        print("Работа продолжается с пустым списком задач.")
        return []

    if not isinstance(raw_data, list):
        print(f"Предупреждение: {file_path.name} должен содержать список задач.")
        print("Работа продолжается с пустым списком задач.")
        return []

    tasks: list[dict[str, Any]] = []
    seen_ids: set[int] = set()
    skipped = 0
    for item in raw_data:
        task = _normalize_task(item)
        if task is None or task["id"] in seen_ids:
            skipped += 1
            continue
        seen_ids.add(task["id"])
        tasks.append(task)

    if skipped:
        print(f"Предупреждение: пропущено некорректных записей в {file_path.name}: {skipped}.")
    return tasks


def save_tasks(tasks: list[dict[str, Any]], path: Path | str = DEFAULT_DATA_FILE) -> bool:
    file_path = Path(path)
    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError as error:
        print(f"Ошибка: не удалось сохранить данные в {file_path.name}: {error}")
        return False
    return True


def _normalize_task(item: Any) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None

    try:
        task_id = int(item["id"])
        priority = int(item["priority"])
    except (KeyError, TypeError, ValueError):
        return None

    title = str(item.get("title", "")).strip()
    if not title or priority not in VALID_PRIORITIES:
        return None

    status = item.get("status")
    if status not in VALID_STATUSES:
        status = STATUS_TODO

    return {"id": task_id, "title": title, "priority": priority, "status": status}
