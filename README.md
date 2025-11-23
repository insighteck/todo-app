# Daily Todo List Manager

A feature-rich Todo List application with both command-line (CLI) and web-based (Web UI) interfaces.

## Features

### Web UI
- 🌐 Modern, responsive web interface
- ✅ Add tasks with priority levels (high, medium, low)
- 📋 Filter tasks by status (All, Active, Completed)
- ✔️ Mark tasks as completed with a single click
- 🗑️ Delete individual tasks
- 🧹 Clear all completed tasks at once
- 💾 Persistent storage (saves to JSON file)
- 📱 Mobile-friendly design

### CLI
- 🖥️ Interactive command-line interface
- Same task management features as Web UI

## Screenshots

The Web UI features a beautiful purple gradient design with:
- Task input with priority selector
- Filter buttons (All/Active/Completed)
- Checkbox toggles for completion
- Priority badges (🔴 High, 🟡 Medium, 🟢 Low)
- Task counter and clear completed button

## Installation

### Web UI

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/todo-app.git
cd todo-app

# Install dependencies
pip install -r requirements.txt

# Run the web server
python app.py
```

Then open your browser to: **http://localhost:5000**

### CLI

```bash
# No additional dependencies needed for CLI
python3 todo.py
```

## Usage

### Web UI

1. **Add a task**: Type your task in the input field, select priority, and click "Add Task"
2. **Complete a task**: Click the checkbox next to the task
3. **Delete a task**: Click the trash icon (appears on hover)
4. **Filter tasks**: Click "All", "Active", or "Completed" buttons
5. **Clear completed**: Click "Clear Completed" button in the footer

### CLI Commands

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

## Tech Stack

### Backend
- Python 3.x
- Flask (web framework)

### Frontend
- HTML5
- CSS3 (custom styles, responsive design)
- Vanilla JavaScript (no frameworks)

## Data Storage

- **Web UI**: Todos are stored in `todos.json` in the app directory
- **CLI**: Todos are stored in `~/.todo_list.json` in your home directory

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Get all todos |
| POST | `/api/todos` | Create a new todo |
| PUT | `/api/todos/<id>` | Update a todo |
| DELETE | `/api/todos/<id>` | Delete a todo |
| DELETE | `/api/todos/clear-completed` | Clear all completed todos |

## License

MIT License - feel free to use and modify!
