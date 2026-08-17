import json
import sys
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Dict, List

HOME = Path.home()
DEFAULT_DIR_NAME = ".task_tracker"
DEFAULT_DB_NAME = "db.json"
EXPECTED_DB_PATH = HOME / DEFAULT_DIR_NAME / DEFAULT_DB_NAME


DEFAULT_STATUS = "todo"
INITIAL_ID = 1


class Command(StrEnum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_IN_PROGRESS = "mark-in-progress"
    MARK_DONE = "mark-done"
    LIST = "list"


def create_db(base_dir: Path) -> None:

    app_dir_name = base_dir / DEFAULT_DIR_NAME

    if not app_dir_name.exists():
        app_dir_name.mkdir()

    db_path = EXPECTED_DB_PATH

    if not db_path.exists():
        db_path.touch()


def load_db(db_path: Path) -> dict:

    try:
        with open(db_path, mode="r", encoding="utf-8") as db_file:
            data = json.load(db_file)

    except json.JSONDecodeError:
        return dict()

    return data


def exist_db() -> bool:
    return EXPECTED_DB_PATH.exists()


# ---------------------------------------------------------------------------------
# Command Implementation
# --------------------------------------------------------------------------------


# Add
def add_task(task: str) -> None:

    data = load_db(EXPECTED_DB_PATH)

    task_json = dict(
        description=task,
        status=DEFAULT_STATUS,
        createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updateAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    with open(EXPECTED_DB_PATH, "r+", encoding="utf-8") as db:
        if not data:
            id_task = INITIAL_ID
        else:
            id_task = max([int(key) for key in data.keys()]) + 1

        data[id_task] = task_json

        db.seek(0)

        json.dump(data, db, indent=4, ensure_ascii=False)

        db.truncate()

    print(f"Task created with id={id_task}.")


# Delete
def delete_task(task_ids: List[int]) -> None:

    data = load_db(EXPECTED_DB_PATH)

    if not data:
        print("The todo is already empty.")
        return

    removed_tasks = 0

    for id_task in task_ids:
        if str(id_task) in data.keys():
            data.pop(str(id_task))
            removed_tasks += 1
        else:
            continue

    if removed_tasks == 0:
        print("No coincidence found of id's in database. Tasks deleted: 0.")
        return

    with open(EXPECTED_DB_PATH, "r+", encoding="utf-8") as db:
        db.seek(0)
        json.dump(data, db, ensure_ascii=False, indent=4)
        db.truncate()

    print(f"Tasks deleted: {removed_tasks}")


# Listing
def list_tasks(status: str) -> None:

    data = load_db(EXPECTED_DB_PATH)

    header = (
        "id".center(10, " ")
        + "|"
        + "Task".center(75, " ")
        + "|"
        + "Status".center(15, " ")
        + "|"
        + "Created At".center(24, " ")
        + "|"
        + "Last Update At".center(24, " ")
        + "|"
    )

    if not data:
        print(header)
        return

    printed_task = 0

    if status != "all":
        for id_task in data.keys():
            if status == data[id_task]["status"]:
                if printed_task == 0:
                    print(header)

                desc: str = data[id_task]["description"]
                desc = desc[:71] + "..." if len(desc) > 75 else desc

                status_task: str = data[id_task]["status"]

                created_at: str = data[id_task]["createdAt"]
                last_update: str = data[id_task]["updateAt"]

                content = (
                    f"{id_task}".center(10, " ")
                    + "|"
                    + f" {desc}".ljust(75)
                    + "|"
                    + f" {status_task}".ljust(15)
                    + "|"
                    + f" {created_at}".center(24, " ")
                    + "|"
                    + f" {last_update}".center(24, " ")
                    + "|"
                )

                printed_task += 1
                print(content)
            else:
                continue

        if printed_task == 0:
            print(f"No task found with the status {status}.")

    else:
        print(header)
        for id_task in data.keys():
            desc: str = data[id_task]["description"]
            desc = desc[:71] + "..." if len(desc) > 75 else desc

            status_task: str = data[id_task]["status"]

            created_at: str = data[id_task]["createdAt"]
            last_update: str = data[id_task]["updateAt"]

            content = (
                f"{id_task}".center(10, " ")
                + "|"
                + f" {desc}".ljust(75)
                + "|"
                + f" {status_task}".ljust(15)
                + "|"
                + f" {created_at}".center(24, " ")
                + "|"
                + f" {last_update}".center(24, " ")
                + "|"
            )

            print(content)


# Mark as Done
def mark_as_done(task_ids: List[int]) -> None:

    data = load_db(EXPECTED_DB_PATH)

    if not data:
        print("Todo is empty.")
        return

    n_status_updates = 0

    for task in task_ids:
        if str(task) in data.keys():
            data[str(task)]["status"] = "done"
            data[str(task)]["updateAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            n_status_updates += 1
        else:
            continue

    if n_status_updates == 0:
        print(
            f"No task(s) id(s) found in Todo. Updated status task(s): {n_status_updates}"
        )

        return

    with open(EXPECTED_DB_PATH, "r+", encoding="utf-8") as db:
        db.seek(0)
        json.dump(data, db, indent=4, ensure_ascii=False)
        db.truncate()

    if n_status_updates == len(task_ids):
        print(f"Success in update status for {n_status_updates} task(s).")

    if n_status_updates < len(task_ids):
        print(
            f"Success in update status for {n_status_updates} of {len(task_ids)} task(s) provided. One or more id(s) not found in Todo."
        )


def mark_as_in_progress(task_ids: List[int]) -> None:

    data = load_db(EXPECTED_DB_PATH)

    if not data:
        print("Todo is empty.")
        return

    n_status_updates = 0

    for task in task_ids:
        if str(task) in data.keys():
            data[str(task)]["status"] = "in-progress"
            data[str(task)]["updateAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            n_status_updates += 1
        else:
            continue

    if n_status_updates == 0:
        print(
            f"No task(s) id(s) found in Todo. Updated status task(s): {n_status_updates}"
        )

        return

    with open(EXPECTED_DB_PATH, "r+", encoding="utf-8") as db:
        db.seek(0)
        json.dump(data, db, indent=4, ensure_ascii=False)
        db.truncate()

    if n_status_updates == len(task_ids):
        print(f"Success in update status for {n_status_updates} task(s).")

    if n_status_updates < len(task_ids):
        print(
            f"Success in update status for {n_status_updates} of {len(task_ids)} task(s) provided. One or more id(s) not found in Todo."
        )


def update_task(task_id: int, new_task: str) -> None:

    data = load_db(EXPECTED_DB_PATH)

    if not data:
        print("Todo is empty.")
        return

    if str(task_id) not in data.keys():
        print(
            f"Task with id={task_id} does not exist. Tip: use add to create the task."
        )
        return

    data[str(task_id)]["description"] = new_task
    data[str(task_id)]["updateAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(EXPECTED_DB_PATH, "r+", encoding="utf-8") as db:
        db.seek(0)
        json.dump(data, db, indent=4, ensure_ascii=False)
        db.truncate()

    print(f"Success in update task with id={task_id}.")


def run_app(raw_command: str, config: Dict[str, str]) -> None:

    try:
        command = Command(raw_command)
    except ValueError:
        print("Unknow command.")
        sys.exit(1)

    if not exist_db():
        create_db(HOME)

    match command:
        case Command.ADD:
            add_task(config["task"])
        case Command.MARK_IN_PROGRESS:
            mark_as_in_progress(config["id"])
        case Command.MARK_DONE:
            mark_as_done(config["id"])
        case Command.UPDATE:
            update_task(config["id"], config["task"])
        case Command.DELETE:
            delete_task(config["id"])
        case Command.LIST:
            list_tasks(config["status"])

