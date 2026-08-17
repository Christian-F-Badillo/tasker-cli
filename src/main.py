import argparse as ap

from .todo import run_app


# Validate the minimum length of a Task
def min_length(min_chars: int):
    def validator(value: str) -> str:
        if len(value) < min_chars:
            raise ap.ArgumentTypeError(
                f"The minimum length of the task is {min_chars} characters."
            )
        return value

    return validator


# Global Parser
global_parser = ap.ArgumentParser(prog="task-cli")

# CLI app version
global_parser.add_argument("--version", action="version", version="%(prog)s 1.0.")

# Subparser
subparser = global_parser.add_subparsers(
    title="subcommands",
    dest="command",
    required=False,
    description="Task Tracker CLI commands",
    help="Available commands",
)

# Add Task Command
# -----------------------------------------------------------------------------------
add_task_parser = subparser.add_parser("add", help="Add a new task.")
add_task_parser.add_argument(
    "task", type=min_length(1), help="Name of the task to add."
)

# List Task Commands
# ------------------------------------------------------------------------------------
list_tasks_parser = subparser.add_parser("list", help="List tasks by status.")
list_tasks_parser.add_argument(
    "status",
    type=str,
    nargs="?",
    default="all",
    choices=["done", "in-progress", "todo", "all"],
    help="List the tasks filter by status (in-progress, done, todo). Usage: list [status].",
)

# Mark Commands
# -------------------------------------------------------------------------------------
mark_inprogress_task_parser = subparser.add_parser(
    "mark-in-progress", help="Mark as in-progress one or more tasks."
)
mark_inprogress_task_parser.add_argument(
    "id",
    type=int,
    nargs="+",
    help="id or id's of the task(s) to mark as in-progress. Usage: mark-in-progress [id] [id] ...",
)

# Mark Done Task
mark_done_task_parser = subparser.add_parser(
    "mark-done", help="Mark as done one or more tasks."
)
mark_done_task_parser.add_argument(
    "id",
    type=int,
    nargs="+",
    help="id or id's of the task(s) to mark as done. Usage: mark-done [id] [id] ...",
)

# Delete Command
# ----------------------------------------------------------------------------------------------------
delet_task_parser_task_parser = subparser.add_parser(
    "delete", help="Delete one or more tasks."
)
delet_task_parser_task_parser.add_argument(
    "id",
    type=int,
    nargs="+",
    help="id or id's of the task(s) to delete. Usage: delete [id] [id] ...",
)

# Update Commands
# --------------------------------------------------------------------------------------------------------
update_task_parser = subparser.add_parser("update", help="Update a task.")
update_task_parser.add_argument(
    "id",
    type=int,
    help="id of the task to update.",
)

update_task_parser.add_argument(
    "task",
    type=min_length(1),
    help="new task.",
)

args = global_parser.parse_args()

# Pass the Namespace to Dict
kargs = vars(args)
# Pop the command
command = kargs.pop("command")


def main():

    run_app(command, kargs)


if __name__ == "__main__":
    main()
