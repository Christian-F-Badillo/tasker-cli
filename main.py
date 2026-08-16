import argparse as ap

def min_length(min_chars: int):
    def validator(value: str) -> str:
        if len(value) < min_chars:
            raise ap.ArgumentTypeError(
                f"The minimum length of the task is {min_chars} characters."
            )
        return value
    return validator

global_parser = ap.ArgumentParser()

subparser = global_parser.add_subparsers(
    title="subcommands",
    dest="command",
    required=False,
    description="Task Tracker CLI commands",
    help="Available commands"
)

add_task_parser = subparser.add_parser("add", help="Add a new task")
add_task_parser.add_argument(
                        "task",
                        type=min_length(5),
                        help="Name of the task to add"
                    )

list_tasks_parser = subparser.add_parser("list", help="List tasks by status")
list_tasks_parser.add_argument("status",
                            type=str,
                            choices=["done", "in-progress", "todo"],
                            help="List the tasks filter by status (in-progress, done, todo). Usage: list [status]",
                            )       

global_parser.add_argument("--version", action="version", version="%(prog)s 1.0")

mark_inprogress_task_parser = subparser.add_parser("mark-in-progress", help="Mark as in-progress one or more tasks")
mark_inprogress_task_parser.add_argument("id",
                            type=int,
                            nargs="+",
                            help="id or id's of the task(s) to mark as in-progress. Usage: mark-in-progress [id] [id] ...",
                            )

# Mark Done Task
mark_done_task_parser = subparser.add_parser("mark-done", help="Mark as done one or more tasks")
mark_done_task_parser.add_argument("id",
                            type=int,
                            nargs="+",
                            help="id or id's of the task(s) to mark as done. Usage: mark-done [id] [id] ...",
                            )

mark_done_task_parser = subparser.add_parser("delete", help="Delete one or more tasks")
mark_done_task_parser.add_argument("id",
                            type=int,
                            nargs="+",
                            help="id or id's of the task(s) to delete. Usage: delete [id] [id] ...",
                            )

update_task_parser = subparser.add_parser("update", help="Update a task")
update_task_parser.add_argument("id",
                            type=int,
                            help="Update a task's name based on its ID",
                            )

update_task_parser.add_argument("task",
                            type=min_length(5),
                            help="Update a task's name based on its ID",
                            )

args = global_parser.parse_args()

def main():
    print("Hello from task-tracker!")
    print("Parsed arguments:", args)


if __name__ == "__main__":
    main()
