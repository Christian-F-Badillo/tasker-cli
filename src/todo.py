from typing import Dict
import sys
import json
from enum import StrEnum
from pathlib import Path

HOME = Path.home()
DEFAULT_DIR_NAME = ".task_tracker"
DEFAULT_DB_NAME = "db.json"
EXPECTED_DB_PATH = HOME/DEFAULT_DIR_NAME/DEFAULT_DB_NAME

class Command(StrEnum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_IN_PROGRESS = "mark-in-progress"
    MARK_DONE = "mark-done"
    LIST = "list"

def create_db(base_dir: Path) ->None:

    app_dir_name = base_dir / DEFAULT_DIR_NAME
    
    if not app_dir_name.exists():
        app_dir_name.mkdir()

    db_path = EXPECTED_DB_PATH

    if not db_path.exists():
        db_path.touch()

def load_db(db_path:Path) -> str:

    with open(db_path, mode="r", encoding="utf-8") as db_file:
        data = json.load(db_file)
    
    return data

def exist_db() -> bool:
    return EXPECTED_DB_PATH.exists()

def run_app(raw_command:str, config:Dict[str, str]) -> None:

    try:
        command = Command(raw_command)
    except ValueError:
        print("Unknow command.")
        sys.exit(1)

    if not exist_db():
        create_db(HOME)

    match command:
        case Command.ADD:
            print(f"adding new task: {config}")
        case Command.MARK_IN_PROGRESS:
            print(f"marking task as `in progress`: {config}")
        case Command.MARK_DONE:
            print(f"marking task as `complete`: {config}")
        case Command.UPDATE:
            print(f"Updating task: {config}")
        case Command.DELETE:
            print(f"Deleting task: {config}")
        case Command.LIST:
            print(f"Listing list: {config}")