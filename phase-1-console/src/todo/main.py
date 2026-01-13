"""
In-Memory Todo Console Application
Main entry point for both CLI and Interactive modes
"""

import argparse
import sys
from .models import Task
from .manager import TaskManager
from .interactive import InteractiveTodo


def main():
    """Main entry point for the todo application - CLI or Interactive mode"""

    # Check if no arguments were provided (except the script name)
    if len(sys.argv) == 1:
        # Launch interactive mode
        app = InteractiveTodo()
        app.run()
    else:
        # Launch CLI mode with argparse
        parser = argparse.ArgumentParser(
            description="In-Memory Todo Console Application"
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Task title")
        add_parser.add_argument("description", nargs="?", default="", help="Task description")

        # List command
        list_parser = subparsers.add_parser("list", help="List all tasks")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", type=int, help="Task ID")
        update_parser.add_argument("--title", help="New task title")
        update_parser.add_argument("--description", help="New task description")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
        complete_parser.add_argument("id", type=int, help="Task ID")

        # Uncomplete command
        uncomplete_parser = subparsers.add_parser("uncomplete", help="Mark task as pending")
        uncomplete_parser.add_argument("id", type=int, help="Task ID")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", type=int, help="Task ID")

        # Export command
        export_parser = subparsers.add_parser("export", help="Export tasks to JSON")

        # Import command
        import_parser = subparsers.add_parser("import", help="Import tasks from JSON file")
        import_parser.add_argument("file", help="Path to JSON file")

        # Cleanup command
        cleanup_parser = subparsers.add_parser("cleanup", help="Clean up all tasks data")

        args = parser.parse_args()

        # Initialize task manager
        task_manager = TaskManager()

        try:
            if args.command == "add":
                task = task_manager.add_task(args.title, args.description)
                print(f"Task added with ID: {task.id}")
            elif args.command == "list":
                tasks = task_manager.list_tasks()
                if not tasks:
                    print("No tasks found.")
                else:
                    for task in tasks:
                        status = "X" if task.completed else "O"
                        print(f"{status} [{task.id}] {task.title}")
                        if task.description:
                            print(f"    {task.description}")
            elif args.command == "update":
                updated_task = task_manager.update_task(args.id, args.title, args.description)
                if updated_task:
                    print(f"Task {args.id} updated successfully")
                else:
                    print(f"Error: Task with ID {args.id} not found")
                    sys.exit(1)
            elif args.command == "complete":
                result = task_manager.toggle_completion(args.id, True)
                if result:
                    print(f"Task {args.id} marked as complete")
                else:
                    print(f"Error: Task with ID {args.id} not found")
                    sys.exit(1)
            elif args.command == "uncomplete":
                result = task_manager.toggle_completion(args.id, False)
                if result:
                    print(f"Task {args.id} marked as pending")
                else:
                    print(f"Error: Task with ID {args.id} not found")
                    sys.exit(1)
            elif args.command == "delete":
                result = task_manager.delete_task(args.id)
                if result:
                    print(f"Task {args.id} deleted successfully")
                else:
                    print(f"Error: Task with ID {args.id} not found")
                    sys.exit(1)
            elif args.command == "export":
                tasks_json = task_manager.export_tasks()
                print(tasks_json)
            elif args.command == "import":
                task_manager.import_tasks(args.file)
                print(f"Tasks imported from {args.file}")
            elif args.command == "cleanup":
                result = task_manager.cleanup_data_file()
                if result:
                    print("All tasks data has been cleaned up")
                else:
                    print("No data file found or cleanup failed")
            else:
                parser.print_help()
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()