#!/usr/bin/env python3
"""
Todo List Web Application
A Flask-based web UI for managing your daily tasks.
Features: priority, status, estimated effort, and target date tracking.
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime, date
from pathlib import Path

app = Flask(__name__)

# File to store todos
TODO_FILE = Path(__file__).parent / "todos.json"


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


def get_next_id(todos):
    """Get the next available ID."""
    if not todos:
        return 1
    return max(todo["id"] for todo in todos) + 1


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    """Get all todos with computed target date info."""
    todos = load_todos()
    # Add computed fields for each todo
    for todo in todos:
        target_date = todo.get("target_date", "")
        status = todo.get("status", "pending")
        todo["days_until_target"] = calculate_days_until_target(target_date)
        todo["target_status"] = get_target_status(target_date, status)
    return jsonify(todos)


# Valid status values
VALID_STATUSES = ["pending", "in_progress", "on_hold", "completed"]

# Valid effort values (in hours)
VALID_EFFORTS = ["0.5", "1", "2", "4", "8", "16", "24", "40"]


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


@app.route("/api/todos", methods=["POST"])
def add_todo():
    """Add a new todo."""
    data = request.get_json()

    if not data or not data.get("task"):
        return jsonify({"error": "Task is required"}), 400

    todos = load_todos()

    # Parse effort as float for calculations, store as string
    effort = data.get("effort", "")
    target_date = data.get("target_date", "")

    todo = {
        "id": get_next_id(todos),
        "task": data["task"],
        "priority": data.get("priority", "medium"),
        "status": "pending",
        "effort": effort,  # Estimated effort in hours
        "target_date": target_date,  # Target completion date (YYYY-MM-DD)
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }

    # Add computed fields
    todo["days_until_target"] = calculate_days_until_target(target_date)
    todo["target_status"] = get_target_status(target_date, "pending")

    todos.append(todo)
    save_todos(todos)

    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a todo (change status, edit task, priority, effort, or target_date)."""
    data = request.get_json()
    todos = load_todos()

    for todo in todos:
        if todo["id"] == todo_id:
            if "status" in data:
                if data["status"] not in VALID_STATUSES:
                    return jsonify({"error": f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"}), 400
                todo["status"] = data["status"]
                if data["status"] == "completed":
                    todo["completed_at"] = datetime.now().isoformat()
                else:
                    todo["completed_at"] = None
            if "task" in data:
                todo["task"] = data["task"]
            if "priority" in data:
                todo["priority"] = data["priority"]
            if "effort" in data:
                todo["effort"] = data["effort"]
            if "target_date" in data:
                todo["target_date"] = data["target_date"]

            # Update computed fields
            target_date = todo.get("target_date", "")
            status = todo.get("status", "pending")
            todo["days_until_target"] = calculate_days_until_target(target_date)
            todo["target_status"] = get_target_status(target_date, status)

            save_todos(todos)
            return jsonify(todo)

    return jsonify({"error": "Todo not found"}), 404


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo."""
    todos = load_todos()

    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos)
            return jsonify({"message": "Todo deleted", "todo": removed})

    return jsonify({"error": "Todo not found"}), 404


@app.route("/api/todos/clear-completed", methods=["DELETE"])
def clear_completed():
    """Clear all completed todos."""
    todos = load_todos()
    active_todos = [t for t in todos if t.get("status", "pending") != "completed"]
    removed_count = len(todos) - len(active_todos)
    save_todos(active_todos)

    return jsonify({"message": f"Cleared {removed_count} completed todo(s)", "count": removed_count})


@app.route("/api/statuses", methods=["GET"])
def get_statuses():
    """Get all valid statuses."""
    return jsonify(VALID_STATUSES)


@app.route("/api/efforts", methods=["GET"])
def get_efforts():
    """Get all valid effort values in hours."""
    return jsonify(VALID_EFFORTS)


@app.route("/api/summary", methods=["GET"])
def get_summary():
    """Get summary statistics including effort tracking."""
    todos = load_todos()

    total_effort = 0
    completed_effort = 0
    overdue_count = 0
    due_soon_count = 0

    for todo in todos:
        effort = todo.get("effort", "")
        if effort:
            try:
                effort_hours = float(effort)
                total_effort += effort_hours
                if todo.get("status") == "completed":
                    completed_effort += effort_hours
            except ValueError:
                pass

        # Calculate target date status
        target_date = todo.get("target_date", "")
        status = todo.get("status", "pending")
        target_status = get_target_status(target_date, status)

        if target_status == "overdue":
            overdue_count += 1
        elif target_status in ["due_today", "due_soon"]:
            due_soon_count += 1

    return jsonify({
        "total_tasks": len(todos),
        "completed_tasks": len([t for t in todos if t.get("status") == "completed"]),
        "total_effort_hours": total_effort,
        "completed_effort_hours": completed_effort,
        "remaining_effort_hours": total_effort - completed_effort,
        "overdue_count": overdue_count,
        "due_soon_count": due_soon_count
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
