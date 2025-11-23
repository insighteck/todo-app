#!/usr/bin/env python3
"""
Daily Todo List Manager
A simple command-line application to manage your daily tasks.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# File to store todos
TODO_FILE = Path.home() / ".todo_list.json"


def load_todos():
    """Load todos from the JSON file."""
    if TODO_FILE.exists():
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []


def save_todos(todos):
    """Save todos to the JSON file."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def add_todo(task, priority="medium"):
    """Add a new todo item."""
    todos = load_todos()
    todo = {
        "id": len(todos) + 1,
        "task": task,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    todos.append(todo)
    save_todos(todos)
    print(f"✅ Added: '{task}' (Priority: {priority})")


def list_todos(show_all=False):
    """List all todo items."""
    todos = load_todos()

    if not todos:
        print("📋 No todos yet! Add some tasks to get started.")
        return

    # Filter based on show_all flag
    if not show_all:
        display_todos = [t for t in todos if not t["completed"]]
    else:
        display_todos = todos

    if not display_todos:
        print("🎉 All tasks completed! Great job!")
        return

    # Priority colors/symbols
    priority_symbols = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }

    print("\n" + "=" * 50)
    print("📋 YOUR TODO LIST")
    print("=" * 50)

    for todo in display_todos:
        status = "✅" if todo["completed"] else "⬜"
        priority = priority_symbols.get(todo["priority"], "⚪")
        task_display = todo["task"]
        if todo["completed"]:
            task_display = f"\033[9m{task_display}\033[0m"  # Strikethrough
        print(f"{status} [{todo['id']}] {priority} {task_display}")

    print("=" * 50)

    # Summary
    total = len(todos)
    completed = len([t for t in todos if t["completed"]])
    print(f"📊 Progress: {completed}/{total} tasks completed")
    print()


def complete_todo(todo_id):
    """Mark a todo as completed."""
    todos = load_todos()

    for todo in todos:
        if todo["id"] == todo_id:
            if todo["completed"]:
                print(f"ℹ️  Task '{todo['task']}' is already completed!")
                return
            todo["completed"] = True
            todo["completed_at"] = datetime.now().isoformat()
            save_todos(todos)
            print(f"🎉 Completed: '{todo['task']}'")
            return

    print(f"❌ Todo with ID {todo_id} not found.")


def delete_todo(todo_id):
    """Delete a todo item."""
    todos = load_todos()

    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            # Re-number remaining todos
            for j, t in enumerate(todos):
                t["id"] = j + 1
            save_todos(todos)
            print(f"🗑️  Deleted: '{removed['task']}'")
            return

    print(f"❌ Todo with ID {todo_id} not found.")


def clear_completed():
    """Clear all completed todos."""
    todos = load_todos()
    active_todos = [t for t in todos if not t["completed"]]

    removed_count = len(todos) - len(active_todos)

    if removed_count == 0:
        print("ℹ️  No completed todos to clear.")
        return

    # Re-number remaining todos
    for i, todo in enumerate(active_todos):
        todo["id"] = i + 1

    save_todos(active_todos)
    print(f"🗑️  Cleared {removed_count} completed todo(s).")


def print_help():
    """Print help information."""
    help_text = """
📋 DAILY TODO LIST MANAGER
===========================

Commands:
  add <task> [priority]  - Add a new task (priority: high, medium, low)
  list                   - List active todos
  list all               - List all todos (including completed)
  done <id>              - Mark a todo as completed
  delete <id>            - Delete a todo
  clear                  - Clear all completed todos
  help                   - Show this help message
  quit                   - Exit the application

Examples:
  add "Buy groceries" high
  add "Read a book"
  done 1
  delete 2

Priority Levels:
  🔴 high   - Urgent tasks
  🟡 medium - Normal tasks (default)
  🟢 low    - Low priority tasks
"""
    print(help_text)


def main():
    """Main application loop."""
    print("\n🌟 Welcome to your Daily Todo List Manager!")
    print("Type 'help' for available commands.\n")

    while True:
        try:
            user_input = input("todo> ").strip()

            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command == "quit" or command == "exit" or command == "q":
                print("👋 Goodbye! Have a productive day!")
                break

            elif command == "help" or command == "h":
                print_help()

            elif command == "add" or command == "a":
                if not args:
                    print("❌ Please provide a task. Example: add 'Buy milk' high")
                    continue

                # Parse task and optional priority
                if args.endswith((" high", " medium", " low")):
                    *task_parts, priority = args.rsplit(maxsplit=1)
                    task = " ".join(task_parts).strip('"\'')
                else:
                    task = args.strip('"\'')
                    priority = "medium"

                add_todo(task, priority)

            elif command == "list" or command == "ls" or command == "l":
                show_all = args.lower() == "all"
                list_todos(show_all)

            elif command == "done" or command == "d":
                if not args:
                    print("❌ Please provide a todo ID. Example: done 1")
                    continue
                try:
                    todo_id = int(args)
                    complete_todo(todo_id)
                except ValueError:
                    print("❌ Invalid ID. Please provide a number.")

            elif command == "delete" or command == "del" or command == "rm":
                if not args:
                    print("❌ Please provide a todo ID. Example: delete 1")
                    continue
                try:
                    todo_id = int(args)
                    delete_todo(todo_id)
                except ValueError:
                    print("❌ Invalid ID. Please provide a number.")

            elif command == "clear":
                clear_completed()

            else:
                print(f"❌ Unknown command: '{command}'. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye! Have a productive day!")
            break
        except EOFError:
            print("\n👋 Goodbye! Have a productive day!")
            break


if __name__ == "__main__":
    main()
