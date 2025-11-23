// Todo List Application JavaScript
// Features: status tracking, priority, estimated effort, and target date

const API_BASE = '/api/todos';

// Status definitions with labels and colors
const STATUS_CONFIG = {
    pending: { label: 'Pending', icon: '⏳' },
    in_progress: { label: 'In Progress', icon: '🔄' },
    on_hold: { label: 'On Hold', icon: '⏸️' },
    completed: { label: 'Completed', icon: '✅' }
};

// Target status definitions
const TARGET_STATUS_CONFIG = {
    overdue: { label: 'Overdue', icon: '🚨', class: 'target-overdue' },
    due_today: { label: 'Due Today', icon: '⚡', class: 'target-due-today' },
    due_soon: { label: 'Due Soon', icon: '⏰', class: 'target-due-soon' },
    on_track: { label: 'On Track', icon: '✓', class: 'target-on-track' },
    no_target: { label: '', icon: '', class: '' },
    completed: { label: 'Done', icon: '✅', class: 'target-completed' }
};

// Effort labels for display
const EFFORT_LABELS = {
    '0.5': '30m',
    '1': '1h',
    '2': '2h',
    '4': '4h',
    '8': '1d',
    '16': '2d',
    '24': '3d',
    '40': '1w'
};

// State
let todos = [];
let currentFilter = 'all';

// DOM Elements
const todoList = document.getElementById('todo-list');
const emptyState = document.getElementById('empty-state');
const addTodoForm = document.getElementById('add-todo-form');
const taskInput = document.getElementById('task-input');
const prioritySelect = document.getElementById('priority-select');
const effortSelect = document.getElementById('effort-select');
const targetDateInput = document.getElementById('target-date-input');
const filterButtons = document.querySelectorAll('.filter-btn');
const clearCompletedBtn = document.getElementById('clear-completed-btn');
const tasksCount = document.getElementById('tasks-count');
const completedCount = document.getElementById('completed-count');

// Summary elements
const totalEffort = document.getElementById('total-effort');
const completedEffort = document.getElementById('completed-effort');
const remainingEffort = document.getElementById('remaining-effort');
const overdueCount = document.getElementById('overdue-count');
const overdueContainer = document.getElementById('overdue-container');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
    setupEventListeners();
    setMinDate();
});

// Set minimum date for target date input to today
function setMinDate() {
    const today = new Date().toISOString().split('T')[0];
    targetDateInput.min = today;
}

// Setup Event Listeners
function setupEventListeners() {
    addTodoForm.addEventListener('submit', handleAddTodo);
    clearCompletedBtn.addEventListener('click', handleClearCompleted);

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTodos();
        });
    });
}

// Fetch all todos from API
async function fetchTodos() {
    try {
        const response = await fetch(API_BASE);
        todos = await response.json();
        renderTodos();
        fetchSummary();
    } catch (error) {
        console.error('Error fetching todos:', error);
        showError('Failed to load todos');
    }
}

// Fetch summary statistics
async function fetchSummary() {
    try {
        const response = await fetch('/api/summary');
        const summary = await response.json();
        updateSummaryDisplay(summary);
    } catch (error) {
        console.error('Error fetching summary:', error);
    }
}

// Update summary banner display
function updateSummaryDisplay(summary) {
    totalEffort.textContent = formatEffortHours(summary.total_effort_hours);
    completedEffort.textContent = formatEffortHours(summary.completed_effort_hours);
    remainingEffort.textContent = formatEffortHours(summary.remaining_effort_hours);
    overdueCount.textContent = summary.overdue_count;

    // Show/hide overdue warning
    if (summary.overdue_count > 0) {
        overdueContainer.classList.add('has-overdue');
    } else {
        overdueContainer.classList.remove('has-overdue');
    }
}

// Format effort hours for display
function formatEffortHours(hours) {
    if (hours === 0) return '0h';
    if (hours < 1) return `${Math.round(hours * 60)}m`;
    if (hours >= 8) {
        const days = Math.floor(hours / 8);
        const remainingHours = hours % 8;
        if (remainingHours === 0) return `${days}d`;
        return `${days}d ${remainingHours}h`;
    }
    return `${hours}h`;
}

// Add a new todo
async function handleAddTodo(e) {
    e.preventDefault();

    const task = taskInput.value.trim();
    const priority = prioritySelect.value;
    const effort = effortSelect.value;
    const targetDate = targetDateInput.value;

    if (!task) return;

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task, priority, effort, target_date: targetDate })
        });

        if (response.ok) {
            const newTodo = await response.json();
            todos.push(newTodo);
            renderTodos();
            fetchSummary();
            // Reset form
            taskInput.value = '';
            effortSelect.value = '';
            targetDateInput.value = '';
            taskInput.focus();
        } else {
            showError('Failed to add todo');
        }
    } catch (error) {
        console.error('Error adding todo:', error);
        showError('Failed to add todo');
    }
}

// Update todo status
async function updateTodoStatus(id, newStatus) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.ok) {
            const updatedTodo = await response.json();
            const index = todos.findIndex(t => t.id === id);
            todos[index] = updatedTodo;
            renderTodos();
            fetchSummary();
        }
    } catch (error) {
        console.error('Error updating todo:', error);
        showError('Failed to update todo');
    }
}

// Update todo effort
async function updateTodoEffort(id, newEffort) {
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ effort: newEffort })
        });

        if (response.ok) {
            const updatedTodo = await response.json();
            const index = todos.findIndex(t => t.id === id);
            todos[index] = updatedTodo;
            renderTodos();
            fetchSummary();
        }
    } catch (error) {
        console.error('Error updating effort:', error);
        showError('Failed to update effort');
    }
}

// Update todo target date
async function updateTodoTargetDate(id, newTargetDate) {
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_date: newTargetDate })
        });

        if (response.ok) {
            const updatedTodo = await response.json();
            const index = todos.findIndex(t => t.id === id);
            todos[index] = updatedTodo;
            renderTodos();
            fetchSummary();
        }
    } catch (error) {
        console.error('Error updating target date:', error);
        showError('Failed to update target date');
    }
}

// Toggle todo completion (quick toggle between pending and completed)
async function toggleTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    const newStatus = todo.status === 'completed' ? 'pending' : 'completed';
    await updateTodoStatus(id, newStatus);
}

// Delete a todo
async function deleteTodo(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            todos = todos.filter(t => t.id !== id);
            renderTodos();
            fetchSummary();
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
        showError('Failed to delete todo');
    }
}

// Clear all completed todos
async function handleClearCompleted() {
    const completedTodos = todos.filter(t => t.status === 'completed');
    if (completedTodos.length === 0) return;

    try {
        const response = await fetch(`${API_BASE}/clear-completed`, {
            method: 'DELETE'
        });

        if (response.ok) {
            todos = todos.filter(t => t.status !== 'completed');
            renderTodos();
            fetchSummary();
        }
    } catch (error) {
        console.error('Error clearing completed:', error);
        showError('Failed to clear completed todos');
    }
}

// Filter todos based on current filter
function getFilteredTodos() {
    switch (currentFilter) {
        case 'pending':
            return todos.filter(t => t.status === 'pending');
        case 'in_progress':
            return todos.filter(t => t.status === 'in_progress');
        case 'on_hold':
            return todos.filter(t => t.status === 'on_hold');
        case 'completed':
            return todos.filter(t => t.status === 'completed');
        case 'overdue':
            return todos.filter(t => t.target_status === 'overdue');
        case 'due_soon':
            return todos.filter(t => ['due_today', 'due_soon'].includes(t.target_status));
        default:
            return todos;
    }
}

// Render todos to the DOM
function renderTodos() {
    const filteredTodos = getFilteredTodos();

    // Sort: overdue first, then by status, then priority, then date
    const targetOrder = { overdue: 0, due_today: 1, due_soon: 2, on_track: 3, no_target: 4, completed: 5 };
    const statusOrder = { pending: 0, in_progress: 1, on_hold: 2, completed: 3 };
    const priorityOrder = { high: 0, medium: 1, low: 2 };

    filteredTodos.sort((a, b) => {
        const statusA = a.status || 'pending';
        const statusB = b.status || 'pending';
        const targetStatusA = a.target_status || 'no_target';
        const targetStatusB = b.target_status || 'no_target';

        // Overdue items always come first (unless completed)
        if (statusA !== 'completed' && statusB !== 'completed') {
            if (targetOrder[targetStatusA] !== targetOrder[targetStatusB]) {
                return targetOrder[targetStatusA] - targetOrder[targetStatusB];
            }
        }

        if (statusOrder[statusA] !== statusOrder[statusB]) {
            return statusOrder[statusA] - statusOrder[statusB];
        }
        if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
            return priorityOrder[a.priority] - priorityOrder[b.priority];
        }
        return new Date(b.created_at) - new Date(a.created_at);
    });

    // Clear current list
    todoList.innerHTML = '';

    // Show/hide empty state
    if (filteredTodos.length === 0) {
        emptyState.classList.add('visible');
        todoList.style.display = 'none';
    } else {
        emptyState.classList.remove('visible');
        todoList.style.display = 'block';
    }

    // Render each todo
    filteredTodos.forEach(todo => {
        const li = createTodoElement(todo);
        todoList.appendChild(li);
    });

    // Update stats
    updateStats();
}

// Create a todo list item element
function createTodoElement(todo) {
    const li = document.createElement('li');
    const status = todo.status || 'pending';
    const targetStatus = todo.target_status || 'no_target';
    const targetConfig = TARGET_STATUS_CONFIG[targetStatus] || TARGET_STATUS_CONFIG.no_target;

    li.className = `todo-item status-${status} ${targetConfig.class}`;
    li.dataset.id = todo.id;

    const createdDate = new Date(todo.created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });

    const statusConfig = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

    // Create status dropdown options
    const statusOptions = Object.entries(STATUS_CONFIG).map(([value, config]) =>
        `<option value="${value}" ${value === status ? 'selected' : ''}>${config.icon} ${config.label}</option>`
    ).join('');

    // Create effort dropdown options
    const effortOptions = Object.entries(EFFORT_LABELS).map(([value, label]) =>
        `<option value="${value}" ${value === todo.effort ? 'selected' : ''}>${label}</option>`
    ).join('');

    // Format target date display
    let targetDateDisplay = '';
    if (todo.target_date) {
        const daysUntil = todo.days_until_target;
        let daysText = '';
        if (daysUntil === null) {
            daysText = '';
        } else if (daysUntil < 0) {
            daysText = `${Math.abs(daysUntil)}d overdue`;
        } else if (daysUntil === 0) {
            daysText = 'Due today';
        } else if (daysUntil === 1) {
            daysText = 'Due tomorrow';
        } else {
            daysText = `${daysUntil}d left`;
        }

        const targetDate = new Date(todo.target_date + 'T00:00:00').toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
        });

        targetDateDisplay = `
            <span class="target-date-badge ${targetConfig.class}" title="Target: ${targetDate}">
                ${targetConfig.icon} ${daysText}
            </span>
        `;
    }

    // Format effort display
    const effortDisplay = todo.effort ? EFFORT_LABELS[todo.effort] || `${todo.effort}h` : '';

    li.innerHTML = `
        <div class="checkbox-wrapper">
            <input
                type="checkbox"
                class="todo-checkbox"
                ${status === 'completed' ? 'checked' : ''}
                onclick="toggleTodo(${todo.id})"
                title="Quick toggle complete"
            >
        </div>
        <span class="priority-badge priority-${todo.priority}">${todo.priority}</span>
        <div class="task-content">
            <span class="task-text">${escapeHtml(todo.task)}</span>
            <div class="task-meta">
                <span class="task-date">Created ${createdDate}</span>
                ${effortDisplay ? `<span class="effort-badge" title="Estimated effort">⏱️ ${effortDisplay}</span>` : ''}
                ${targetDateDisplay}
            </div>
        </div>
        <div class="todo-actions">
            <select class="effort-select-inline" onchange="updateTodoEffort(${todo.id}, this.value)" title="Update effort">
                <option value="">⏱️</option>
                ${effortOptions}
            </select>
            <input
                type="date"
                class="target-date-inline ${targetConfig.class}"
                value="${todo.target_date || ''}"
                onchange="updateTodoTargetDate(${todo.id}, this.value)"
                title="Set target date"
            >
            <select class="status-select status-${status}" onchange="updateTodoStatus(${todo.id}, this.value)" title="Change status">
                ${statusOptions}
            </select>
            <button class="delete-btn" onclick="deleteTodo(${todo.id})" title="Delete task">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6"/>
                </svg>
            </button>
        </div>
    `;

    return li;
}

// Update statistics display
function updateStats() {
    const total = todos.length;
    const completed = todos.filter(t => t.status === 'completed').length;
    const inProgress = todos.filter(t => t.status === 'in_progress').length;
    const pending = todos.filter(t => t.status === 'pending' || !t.status).length;

    tasksCount.textContent = `${pending} pending, ${inProgress} in progress`;
    completedCount.textContent = `${completed} completed`;

    // Show/hide clear completed button
    clearCompletedBtn.style.display = completed > 0 ? 'block' : 'none';
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Utility: Show error message (simple alert for now)
function showError(message) {
    alert(message);
}
