from pathlib import Path

STATUS_TODO = "в работе"
STATUS_DONE = "выполнено"
VALID_STATUSES = (STATUS_TODO, STATUS_DONE)

PRIORITY_NAMES = {1: "низкий", 2: "средний", 3: "высокий"}
VALID_PRIORITIES = tuple(PRIORITY_NAMES)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = PROJECT_ROOT / "tasks.json"
