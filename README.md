# Daily Todo List Manager

A feature-rich Todo List application with both command-line (CLI) and web-based (Web UI) interfaces.

## Features

### Core Features
- Task management with priority levels (high, medium, low)
- Multiple task statuses (Pending, In Progress, On Hold, Completed)
- **NEW: Estimated Effort Tracking** - Track time estimates for each task
- **NEW: Target Date Tracking** - Set deadlines and track progress against them
- **NEW: Overdue Alerts** - Visual warnings for overdue and due-soon tasks

### Web UI
- Modern, responsive web interface
- Real-time effort summary dashboard
- Overdue/Due Soon task filters
- Inline editing of effort and target dates
- Color-coded target date indicators
- Mobile-friendly design

### CLI
- Interactive command-line interface
- Same task management features as Web UI
- Support for relative dates (today, tomorrow, 3d, etc.)
- Effort tracking summary

## Screenshots

The Web UI features:
- **Summary Banner**: Shows total effort, completed effort, remaining effort, and overdue count
- **Task Input**: Priority selector, effort estimate, and target date picker
- **Filter Buttons**: All/Pending/In Progress/On Hold/Completed + Overdue/Due Soon
- **Task Cards**: Priority badges, effort badges, target date status indicators
- **Inline Editing**: Update effort and target dates directly on each task

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

1. **Add a task**: Enter task description, select priority, effort estimate, and target date
2. **Complete a task**: Click the checkbox or change status to "Completed"
3. **Set effort**: Use the inline effort dropdown on each task
4. **Set target date**: Use the inline date picker on each task
5. **Filter tasks**: Use status filters or "Overdue"/"Due Soon" filters
6. **Clear completed**: Click "Clear Completed" button in the footer

### CLI Commands

```
DAILY TODO LIST MANAGER (Enhanced)
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
  high   - Urgent tasks
  medium - Normal tasks (default)
  low    - Low priority tasks

Target Date Indicators:
  Overdue      - Past the target date
  Due today    - Due today
  Due soon     - Due within 2 days
  On track     - More than 2 days remaining
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
| GET | `/api/todos` | Get all todos with computed target date info |
| POST | `/api/todos` | Create a new todo (supports effort and target_date) |
| PUT | `/api/todos/<id>` | Update a todo (status, task, priority, effort, target_date) |
| DELETE | `/api/todos/<id>` | Delete a todo |
| DELETE | `/api/todos/clear-completed` | Clear all completed todos |
| GET | `/api/statuses` | Get all valid status values |
| GET | `/api/efforts` | Get all valid effort values |
| GET | `/api/summary` | Get summary statistics (effort tracking, overdue count) |

### Request/Response Examples

**Create a todo with effort and target date:**
```json
POST /api/todos
{
  "task": "Complete project report",
  "priority": "high",
  "effort": "4",
  "target_date": "2024-12-31"
}
```

**Response:**
```json
{
  "id": 1,
  "task": "Complete project report",
  "priority": "high",
  "status": "pending",
  "effort": "4",
  "target_date": "2024-12-31",
  "days_until_target": 15,
  "target_status": "on_track",
  "created_at": "2024-12-16T10:00:00",
  "completed_at": null
}
```

**Summary endpoint response:**
```json
GET /api/summary
{
  "total_tasks": 10,
  "completed_tasks": 3,
  "total_effort_hours": 24.5,
  "completed_effort_hours": 8.0,
  "remaining_effort_hours": 16.5,
  "overdue_count": 2,
  "due_soon_count": 3
}
```

## Target Date Status Values

| Status | Description |
|--------|-------------|
| `overdue` | Target date has passed |
| `due_today` | Target date is today |
| `due_soon` | Target date is within 2 days |
| `on_track` | Target date is more than 2 days away |
| `no_target` | No target date set |
| `completed` | Task is completed |

## License

MIT License - feel free to use and modify!
