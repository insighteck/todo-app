#!/usr/bin/env python3
"""
Daily Todo List Manager
A simple command-line application to manage your daily tasks.
Features: priority, status, estimated effort, and target date tracking.
"""

import json
import os
from datetime import datetime, date
from pathlib import Path

# File to store todos
TODO_FILE = Path.home() / ".todo_list.json"

# Valid effort values (in hours)
EFFORT_OPTIONS = {
    "30m": "0.5",
    "1h": "1",
    "2h": "2",
    "4h": "4",
    "1d": "8",
    "2d": "16",
    "3d": "24",
    "1w": "40"
}

EFFORT_DISPLAY = {
    "0.5": "30m",
    "1": "1h",
    "2": "2h",
    "4": "4h",
    "8": "1d",
    "16": "2d",
    "24": "3d",
    "40": "1w"
}


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


def calculate_days_until_target(target_date_str):
    """Calculate days remaining until target date."""
    if not target_date_str:
        return None
    try:
        target = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        today = date.today()
        delta = (target - today).days
        return delta
    except (ValueError, TypeError):
        return None


def get_target_status(target_date_str, status):
    """Get status indicator based on target date proximity."""
    if status == "completed":
        return "completed"

    days = calculate_days_until_target(target_date_str)
    if days is None:
        return "no_target"
    elif days < 0:
        return "overdue"
    elif days == 0:
        return "due_today"
    elif days <= 2:
        return "due_soon"
    else:
        return "on_track"


def get_target_indicator(target_date_str, status):
    """Get visual indicator for target date status."""
    target_status = get_target_status(target_date_str, status)
    indicators = {
        "overdue": "🚨",
        "due_today": "⚡",
        "due_soon": "⏰",
        "on_track": "📅",
        "no_target": "",
        "completed": "✅"
    }
    return indicators.get(target_status, "")


def parse_date(date_str):
    """Parse date string in various formats."""
    if not date_str:
        return None

    # Try different date formats
    formats = [
        "%Y-%m-%d",      # 2024-01-15
        "%d/%m/%Y",      # 15/01/2024
        "%m/%d/%Y",      # 01/15/2024
        "%d-%m-%Y",      # 15-01-2024
    ]

    # Handle relative dates
    date_str_lower = date_str.lower()
    if date_str_lower == "today":
        return date.today().strftime("%Y-%m-%d")
    elif date_str_lower == "tomorrow":
        from datetime import timedelta
        return (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str_lower.endswith("d"):
        try:
            days = int(date_str_lower[:-1])
            from datetime import timedelta
            return (date.today() + timedelta(days=days)).strftime("%Y-%m-%d")
        except ValueError:
            pass

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def add_todo(task, priority="medium", effort="", target_date=""):
    """Add a new todo item."""
    todos = load_todos()

    # Parse effort if provided
    if effort and effort in EFFORT_OPTIONS:
        effort = EFFORT_OPTIONS[effort]

    # Parse target date if provided
    parsed_date = parse_date(target_date) if target_date else ""

    todo = {
        "id": len(todos) + 1,
        "task": task,
        "priority": priority,
        "status": "pending",
        "effort": effort,
        "target_date": parsed_date,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    todos.append(todo)
    save_todos(todos)

    effort_display = f" | Effort: {EFFORT_DISPLAY.get(effort, effort)}" if effort else ""
    date_display = f" | Due: {parsed_date}" if parsed_date else ""
    print(f"✅ Added: '{task}' (Priority: {priority}{effort_display}{date_display})")


def list_todos(show_all=False, filter_by=None):
    """List all todo items."""
    todos = load_todos()

    if not todos:
        print("📋 No todos yet! Add some tasks to get started.")
        return

    # Filter based on show_all flag and specific filter
    if filter_by == "overdue":
        display_todos = [t for t in todos if get_target_status(t.get("target_date", ""), t.get("status", "pending")) == "overdue"]
    elif filter_by == "due_soon":
        display_todos = [t for t in todos if get_target_status(t.get("target_date", ""), t.get("status", "pending")) in ["due_today", "due_soon"]]
    elif not show_all:
        display_todos = [t for t in todos if t.get("status", "pending") != "completed" and not t.get("completed")]
    else:
        display_todos = todos

    if not display_todos:
        if filter_by == "overdue":
            print("🎉 No overdue tasks! Great job staying on track!")
        elif filter_by == "due_soon":
            print("📅 No tasks due soon.")
        else:
            print("🎉 All tasks completed! Great job!")
        return

    # Priority colors/symbols
    priority_symbols = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }

    # Status symbols
    status_symbols = {
        "pending": "⏳",
        "in_progress": "🔄",
        "on_hold": "⏸️",
        "completed": "✅"
    }

    print("\n" + "=" * 70)
    print("📋 YOUR TODO LIST")
    print("=" * 70)

    # Calculate totals for summary
    total_effort = 0
    completed_effort = 0
    overdue_count = 0

    for todo in todos:
        effort = todo.get("effort", "")
        if effort:
            try:
                effort_hours = float(effort)
                total_effort += effort_hours
                if todo.get("status") == "completed" or todo.get("completed"):
                    completed_effort += effort_hours
            except ValueError:
                pass

        if get_target_status(todo.get("target_date", ""), todo.get("status", "pending")) == "overdue":
            overdue_count += 1

    # Sort todos: overdue first, then by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    target_order = {"overdue": 0, "due_today": 1, "due_soon": 2, "on_track": 3, "no_target": 4, "completed": 5}

    display_todos.sort(key=lambda t: (
        target_order.get(get_target_status(t.get("target_date", ""), t.get("status", "pending")), 4),
        priority_order.get(t.get("priority", "medium"), 1)
    ))

    for todo in display_todos:
        status = todo.get("status", "pending")
        if todo.get("completed") and status == "pending":
            status = "completed"

        status_icon = status_symbols.get(status, "⬜")
        priority = priority_symbols.get(todo.get("priority", "medium"), "⚪")
        task_display = todo["task"]

        if status == "completed":
            task_display = f"\033[9m{task_display}\033[0m"  # Strikethrough

        # Build effort and date display
        extras = []
        if todo.get("effort"):
            effort_label = EFFORT_DISPLAY.get(todo["effort"], f"{todo['effort']}h")
            extras.append(f"⏱️ {effort_label}")

        target_date = todo.get("target_date", "")
        if target_date:
            days = calculate_days_until_target(target_date)
            target_indicator = get_target_indicator(target_date, status)
            if days is not None:
                if days < 0:
                    extras.append(f"{target_indicator} {abs(days)}d overdue")
                elif days == 0:
                    extras.append(f"{target_indicator} Due today")
                elif days == 1:
                    extras.append(f"{target_indicator} Due tomorrow")
                else:
                    extras.append(f"{target_indicator} {days}d left")

        extras_str = f" ({', '.join(extras)})" if extras else ""

        print(f"{status_icon} [{todo['id']}] {priority} {task_display}{extras_str}")

    print("=" * 70)

    # Summary
    total = len(todos)
    completed = len([t for t in todos if t.get("status") == "completed" or t.get("completed")])

    print(f"📊 Progress: {completed}/{total} tasks completed")

    if total_effort > 0:
        remaining = total_effort - completed_effort
        print(f"⏱️  Effort: {completed_effort:.1f}h completed / {total_effort:.1f}h total ({remaining:.1f}h remaining)")

    if overdue_count > 0:
        print(f"🚨 Warning: {overdue_count} task(s) overdue!")

    print()


def complete_todo(todo_id):
    """Mark a todo as completed."""
    todos = load_todos()

    for todo in todos:
        if todo["id"] == todo_id:
            if todo.get("status") == "completed" or todo.get("completed"):
                print(f"ℹ️  Task '{todo['task']}' is already completed!")
                return
            todo["status"] = "completed"
            todo["completed"] = True
            todo["completed_at"] = datetime.now().isoformat()
            save_todos(todos)
            print(f"🎉 Completed: '{todo['task']}'")
            return

    print(f"❌ Todo with ID {todo_id} not found.")


def set_effort(todo_id, effort):
    """Set estimated effort for a todo."""
    todos = load_todos()

    # Parse effort
    if effort in EFFORT_OPTIONS:
        effort = EFFORT_OPTIONS[effort]

    for todo in todos:
        if todo["id"] == todo_id:
            todo["effort"] = effort
            save_todos(todos)
            effort_display = EFFORT_DISPLAY.get(effort, f"{effort}h")
            print(f"⏱️  Set effort for '{todo['task']}' to {effort_display}")
            return

    print(f"❌ Todo with ID {todo_id} not found.")


def set_target_date(todo_id, target_date):
    """Set target date for a todo."""
    todos = load_todos()

    parsed_date = parse_date(target_date)
    if not parsed_date:
        print(f"❌ Invalid date format. Use YYYY-MM-DD, today, tomorrow, or Nd (e.g., 3d for 3 days)")
        return

    for todo in todos:
        if todo["id"] == todo_id:
            todo["target_date"] = parsed_date
            save_todos(todos)
            print(f"📅 Set target date for '{todo['task']}' to {parsed_date}")
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
    active_todos = [t for t in todos if t.get("status") != "completed" and not t.get("completed")]

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
📋 DAILY TODO LIST MANAGER (Enhanced)
======================================

Commands:
  add <task> [priority] [effort] [date]  - Add a new task
  list                                    - List active todos
  list all                                - List all todos (including completed)
  list overdue                            - List overdue todos
  list due                                - List todos due soon
  done <id>                               - Mark a todo as completed
  effort <id> <effort>                    - Set effort estimate for a task
  due <id> <date>                         - Set target date for a task
  delete <id>                             - Delete a todo
  clear                                   - Clear all completed todos
  help                                    - Show this help message
  quit                                    - Exit the application

Effort Options:
  30m, 1h, 2h, 4h, 1d (8h), 2d, 3d, 1w

Date Formats:
  YYYY-MM-DD     (e.g., 2024-01-15)
  today          (current date)
  tomorrow       (next day)
  Nd             (N days from now, e.g., 3d)

Examples:
  add "Buy groceries" high 1h tomorrow
  add "Write report" medium 4h 2024-12-31
  add "Read a book" low 2h 7d
  effort 1 2h
  due 1 tomorrow
  done 1
  delete 2

Priority Levels:
  🔴 high   - Urgent tasks
  🟡 medium - Normal tasks (default)
  🟢 low    - Low priority tasks

Target Date Indicators:
  🚨 Overdue      - Past the target date
  ⚡ Due today    - Due today
  ⏰ Due soon     - Due within 2 days
  📅 On track     - More than 2 days remaining
"""
    print(help_text)


def main():
    """Main application loop."""
    print("\n🌟 Welcome to your Daily Todo List Manager (Enhanced)!")
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
                    print("❌ Please provide a task. Example: add 'Buy milk' high 1h tomorrow")
                    continue

                # Parse task and optional parameters
                # Format: add "task" [priority] [effort] [date]
                remaining = args

                # Extract task (may be quoted)
                if remaining.startswith('"') or remaining.startswith("'"):
                    quote_char = remaining[0]
                    end_quote = remaining.find(quote_char, 1)
                    if end_quote > 0:
                        task = remaining[1:end_quote]
                        remaining = remaining[end_quote + 1:].strip()
                    else:
                        task = remaining.strip('"\'')
                        remaining = ""
                else:
                    # Split by spaces, task is first word
                    task_parts = remaining.split()
                    task = task_parts[0]
                    remaining = " ".join(task_parts[1:])

                # Parse remaining parameters
                priority = "medium"
                effort = ""
                target_date = ""

                if remaining:
                    params = remaining.split()
                    for param in params:
                        param_lower = param.lower()
                        if param_lower in ["high", "medium", "low"]:
                            priority = param_lower
                        elif param_lower in EFFORT_OPTIONS:
                            effort = param_lower
                        elif parse_date(param):
                            target_date = param

                add_todo(task, priority, effort, target_date)

            elif command == "list" or command == "ls" or command == "l":
                args_lower = args.lower()
                if args_lower == "all":
                    list_todos(show_all=True)
                elif args_lower == "overdue":
                    list_todos(filter_by="overdue")
                elif args_lower == "due":
                    list_todos(filter_by="due_soon")
                else:
                    list_todos(show_all=False)

            elif command == "done" or command == "d":
                if not args:
                    print("❌ Please provide a todo ID. Example: done 1")
                    continue
                try:
                    todo_id = int(args)
                    complete_todo(todo_id)
                except ValueError:
                    print("❌ Invalid ID. Please provide a number.")

            elif command == "effort" or command == "e":
                if not args:
                    print("❌ Please provide a todo ID and effort. Example: effort 1 2h")
                    continue
                try:
                    parts = args.split()
                    if len(parts) < 2:
                        print("❌ Please provide both ID and effort. Example: effort 1 2h")
                        continue
                    todo_id = int(parts[0])
                    effort = parts[1].lower()
                    set_effort(todo_id, effort)
                except ValueError:
                    print("❌ Invalid ID. Please provide a number.")

            elif command == "due" or command == "target":
                if not args:
                    print("❌ Please provide a todo ID and date. Example: due 1 tomorrow")
                    continue
                try:
                    parts = args.split(maxsplit=1)
                    if len(parts) < 2:
                        print("❌ Please provide both ID and date. Example: due 1 2024-12-31")
                        continue
                    todo_id = int(parts[0])
                    target_date = parts[1]
                    set_target_date(todo_id, target_date)
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
