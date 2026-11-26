from __future__ import annotations

from typing import Any

from .constants import STATUS_DONE, STATUS_TODO

Task = dict[str, Any]


def next_free_id(tasks: list[Task]) -> int:
    used_ids = {task["id"] for task in tasks}
    candidate = 1
    while candidate in used_ids:
        candidate += 1
    return candidate


def add_task(tasks: list[Task], title: str, priority: int) -> Task:
    task: Task = {
        "id": next_free_id(tasks),
        "title": title,
        "priority": priority,
        "status": STATUS_TODO,
    }
    tasks.append(task)
    return task


def find_task(tasks: list[Task], task_id: int) -> Task | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def toggle_status(task: Task) -> str:
    task["status"] = STATUS_DONE if task["status"] == STATUS_TODO else STATUS_TODO
    return task["status"]


def delete_task(tasks: list[Task], task_id: int) -> Task | None:
    task = find_task(tasks, task_id)
    if task is None:
        return None
    tasks.remove(task)
    return task


def get_statistics(tasks: list[Task]) -> tuple[int, int, int]:
    total = len(tasks)
    done = sum(1 for task in tasks if task["status"] == STATUS_DONE)
    return total, done, total - done
