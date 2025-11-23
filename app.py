#!/usr/bin/env python3
"""
Todo List Web Application
A Flask-based web UI for managing your daily tasks.
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
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
    """Get all todos."""
    todos = load_todos()
    return jsonify(todos)


# Valid status values
VALID_STATUSES = ["pending", "in_progress", "on_hold", "completed"]


@app.route("/api/todos", methods=["POST"])
def add_todo():
    """Add a new todo."""
    data = request.get_json()

    if not data or not data.get("task"):
        return jsonify({"error": "Task is required"}), 400

    todos = load_todos()

    todo = {
        "id": get_next_id(todos),
        "task": data["task"],
        "priority": data.get("priority", "medium"),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }

    todos.append(todo)
    save_todos(todos)

    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a todo (change status, edit task, or priority)."""
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
