# Task Tracker CLI

[Task Tracker](https://github.com/Christian-F-Badillo/tasker-cli) is a lightweight command-line interface (CLI) application to manage tasks, track progress, and organize daily workflows. The application persists state locally in JSON format without external dependencies.

## Features

* Zero External Dependencies: Built using Python's standard library (argparse, json, pathlib, enum, datetime).

* Full Lifecycle Management: Create, update, list, and delete tasks.

* Batch Operations: Support for updating statuses or deleting multiple task IDs in a single command.

* Formatted Tabular Output: Displays tasks in an aligned, easy-to-read terminal table.

## Requirements

* Python 3.11 or higher.

* (Optional) uv package manager for fast environment setup and dependency management.

## Installation & Setup

### Option 1: Using uv (Recommended)

* Clone or download the repository:

```bash
git clone https://github.com/Christian-F-Badillo/tasker-cli.git
cd task-tracker-cli
```

Ensure your pyproject.toml is configured for build-system and entry points:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
package = true

[project]
name = "task-tracker"
version = "0.1.0"
dependencies = [
    "argcomplete>=3.0.0"
]

[project.scripts]
task-cli = "src.main:main"
```

Sync the virtual environment and install the package locally:

```bash
uv sync
```

Run the executable using uv run:

```bash
uv run task-cli --help
```

### Option 2: Using standard Python (pip)

Clone or download the repository:

```bash
git clone https://github.com/Christian-F-Badillo/tasker-cli.git
cd task-tracker-cli
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
```

Install the package in editable mode:

```bash
pip install -e .
```

Verify installation:

```bash
task-cli --help
```

## Data Storage

Task data is stored automatically in the user's home directory:

```bash
~/.task_tracker/db.json
```

If the directory or file does not exist, it is initialized on the first command execution.

### Data Schema

```json
{
  "id": {
    "description": "Lorem Ipsum",
    "status": "todo",
    "createdAt": "2026-08-16 10:00:00",
    "updateAt": "2026-08-16 10:00:00"
  }
}
```

## Usage & Commands

### 1. Add a Task

Add a new task with default status todo.

```bash
task-cli add "Write unit tests for parser"
```

### 2. List Tasks

List all tasks or filter by specific status (todo, in-progress, done, all).

```bash
# List all tasks
task-cli list

# Filter by status
task-cli list todo
task-cli list in-progress
task-cli list done
```

### 3. Update Task Description

Update the description of an existing task by its ID.

```bash
task-cli update 1 "Refactor database access layer"
```

### 4. Mark Task Status

Update the status of one or multiple tasks.

```bash
# Mark one or more tasks as in-progress
task-cli mark-in-progress 1
task-cli mark-in-progress 1 2 3

# Mark one or more tasks as done
task-cli mark-done 1
task-cli mark-done 1 2 3
```

### 5. Delete Tasks

Remove one or multiple tasks by ID.

```bash
task-cli delete 1
task-cli delete 2 3 4
```

### 6. Version & Help

```bash
# Check version
task-cli --version

# Show general help
task-cli --help

# Show command-specific help
task-cli add --help
task-cli list --help
```

## Architecture Overview

```bash
.
├── pyproject.toml # Project definition, build backend, and scripts entry point
├── src
    ├── main.py        # Entry point, argument parsing, and completion hooks
    └── todo.py        # Core business logic, file I/O, and data structures
```

* `pyproject.toml`: Configures package build settings (setuptools), dependencies, and task-cli command script registration.

* `main.py`: Configures CLI subparsers, validates argument constraints, and routes parsed namespaces.

* `todo.py`: Implements JSON database persistence (`load_db`, `create_db`), status mutations, formatting routines, and execution flow.

## License

This project is open source and available under the MIT License.

## Project Idea Disclaimer

* The project is based on the [road.sh](https://roadmap.sh) project:[https://roadmap.sh/projects/task-tracker](https://roadmap.sh/projects/task-tracker)