# Daily Todo List Manager

A simple command-line Python application to manage your daily tasks.

## Features

- ✅ Add tasks with priority levels (high, medium, low)
- 📋 List active or all todos
- ✔️ Mark tasks as completed
- 🗑️ Delete individual tasks
- 🧹 Clear all completed tasks
- 💾 Persistent storage (saves to JSON file)

## Installation

No external dependencies required! Just Python 3.6+.

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/todo-app.git
cd todo-app

# Make the script executable
chmod +x todo.py

# Run the app
python3 todo.py
```

## Usage

```
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
```

## Data Storage

Your todos are stored in `~/.todo_list.json` in your home directory.

## License

MIT License - feel free to use and modify!
