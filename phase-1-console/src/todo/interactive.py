"""
Interactive mode for the In-Memory Todo Console Application
Provides a menu-driven interface that reuses existing logic
"""

from .manager import TaskManager
from typing import Optional
import os


class InteractiveTodo:
    """
    Interactive menu-driven interface for the Todo application
    """

    def __init__(self):
        self.task_manager = TaskManager()
        self.running = True

    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "="*50)
        print("           TODO APPLICATION - INTERACTIVE MODE")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Uncomplete Task")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. Export Tasks")
        print("8. Import Tasks")
        print("9. Cleanup All Tasks")
        print("0. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get and validate user choice from menu"""
        while True:
            try:
                choice = input("Enter your choice (0-9): ").strip()
                if choice.isdigit() and 0 <= int(choice) <= 9:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 0 and 9.")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                return "0"

    def handle_add_task(self):
        """Handle adding a new task"""
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty!")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()
            if not description:
                description = None

            task = self.task_manager.add_task(title, description)
            print(f"Task added with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error adding task: {e}")

    def handle_view_tasks(self):
        """Handle viewing all tasks"""
        try:
            tasks = self.task_manager.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nYour Tasks:")
                print("-" * 60)
                for task in tasks:
                    status = "X" if task.completed else "O"
                    print(f"[{status}] [{task.id}] {task.title}")
                    if task.description:
                        print(f"    Description: {task.description}")
                    print()
        except Exception as e:
            print(f"Error viewing tasks: {e}")

    def handle_complete_task(self):
        """Handle marking a task as complete"""
        try:
            task_id = self._get_task_id("complete")
            if task_id is None:
                return

            result = self.task_manager.toggle_completion(task_id, True)
            if result:
                print(f"Task {task_id} marked as complete")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except Exception as e:
            print(f"Error completing task: {e}")

    def handle_uncomplete_task(self):
        """Handle marking a task as pending"""
        try:
            task_id = self._get_task_id("uncomplete")
            if task_id is None:
                return

            result = self.task_manager.toggle_completion(task_id, False)
            if result:
                print(f"Task {task_id} marked as pending")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except Exception as e:
            print(f"Error uncompleting task: {e}")

    def handle_update_task(self):
        """Handle updating a task"""
        try:
            task_id = self._get_task_id("update")
            if task_id is None:
                return

            # Get current task to show existing values
            current_task = self.task_manager.get_task(task_id)
            if not current_task:
                print(f"Error: Task with ID {task_id} not found")
                return

            print(f"Current title: {current_task.title}")
            new_title = input("Enter new title (press Enter to keep current): ").strip()
            if not new_title:
                new_title = None

            print(f"Current description: {current_task.description or 'None'}")
            new_description = input("Enter new description (press Enter to keep current): ").strip()
            if not new_description:
                new_description = None

            updated_task = self.task_manager.update_task(task_id, new_title, new_description)
            if updated_task:
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error updating task: {e}")

    def handle_delete_task(self):
        """Handle deleting a task"""
        try:
            task_id = self._get_task_id("delete")
            if task_id is None:
                return

            result = self.task_manager.delete_task(task_id)
            if result:
                print(f"Task {task_id} deleted successfully")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def handle_export_tasks(self):
        """Handle exporting tasks to JSON"""
        try:
            tasks_json = self.task_manager.export_tasks()
            print("Exported Tasks:")
            print("-" * 40)
            print(tasks_json)
            print("-" * 40)
        except Exception as e:
            print(f"Error exporting tasks: {e}")

    def handle_import_tasks(self):
        """Handle importing tasks from JSON file"""
        try:
            file_path = input("Enter path to JSON file: ").strip()
            if not file_path:
                print("File path cannot be empty!")
                return

            # Verify file exists
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' does not exist")
                return

            self.task_manager.import_tasks(file_path)
            print(f"Tasks imported from {file_path}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error importing tasks: {e}")

    def handle_cleanup_tasks(self):
        """Handle cleaning up all tasks"""
        try:
            confirm = input("Are you sure you want to delete ALL tasks? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                result = self.task_manager.cleanup_data_file()
                if result:
                    print("All tasks data has been cleaned up")
                    # Create a new task manager to reset the in-memory state
                    self.task_manager = TaskManager()
                else:
                    print("No data file found or cleanup failed")
            else:
                print("Cleanup cancelled.")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def _get_task_id(self, action: str) -> Optional[int]:
        """Helper method to get and validate a task ID from user"""
        try:
            task_id_str = input(f"Enter task ID to {action}: ").strip()
            if not task_id_str:
                print("Task ID cannot be empty!")
                return None

            task_id = int(task_id_str)
            return task_id
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return None

    def run(self):
        """Main loop for the interactive mode"""
        print("Welcome to the Interactive Todo Application!")
        print("Type '0' or 'Ctrl+C' at any time to exit.")

        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "0":
                print("Thank you for using the Todo Application. Goodbye!")
                self.running = False
            elif choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_tasks()
            elif choice == "3":
                self.handle_complete_task()
            elif choice == "4":
                self.handle_uncomplete_task()
            elif choice == "5":
                self.handle_update_task()
            elif choice == "6":
                self.handle_delete_task()
            elif choice == "7":
                self.handle_export_tasks()
            elif choice == "8":
                self.handle_import_tasks()
            elif choice == "9":
                self.handle_cleanup_tasks()

            # Pause to let user see the result before showing menu again
            if self.running and choice != "0":
                input("\nPress Enter to continue...")


def main():
    """Entry point for interactive mode"""
    app = InteractiveTodo()
    app.run()


if __name__ == "__main__":
    main()