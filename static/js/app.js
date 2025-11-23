// Todo List Application JavaScript

const API_BASE = '/api/todos';

// Status definitions with labels and colors
const STATUS_CONFIG = {
    pending: { label: 'Pending', icon: '⏳' },
    in_progress: { label: 'In Progress', icon: '🔄' },
    on_hold: { label: 'On Hold', icon: '⏸️' },
    completed: { label: 'Completed', icon: '✅' }
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
const filterButtons = document.querySelectorAll('.filter-btn');
const clearCompletedBtn = document.getElementById('clear-completed-btn');
const tasksCount = document.getElementById('tasks-count');
const completedCount = document.getElementById('completed-count');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
    setupEventListeners();
});

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
    } catch (error) {
        console.error('Error fetching todos:', error);
        showError('Failed to load todos');
    }
}

// Add a new todo
async function handleAddTodo(e) {
    e.preventDefault();

    const task = taskInput.value.trim();
    const priority = prioritySelect.value;

    if (!task) return;

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task, priority })
        });

        if (response.ok) {
            const newTodo = await response.json();
            todos.push(newTodo);
            renderTodos();
            taskInput.value = '';
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
        }
    } catch (error) {
        console.error('Error updating todo:', error);
        showError('Failed to update todo');
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
        default:
            return todos;
    }
}

// Render todos to the DOM
function renderTodos() {
    const filteredTodos = getFilteredTodos();

    // Sort by status (pending > in_progress > on_hold > completed), then priority, then date
    const statusOrder = { pending: 0, in_progress: 1, on_hold: 2, completed: 3 };
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    filteredTodos.sort((a, b) => {
        const statusA = a.status || 'pending';
        const statusB = b.status || 'pending';
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
    li.className = `todo-item status-${status}`;
    li.dataset.id = todo.id;

    const createdDate = new Date(todo.created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    const statusConfig = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

    // Create status dropdown options
    const statusOptions = Object.entries(STATUS_CONFIG).map(([value, config]) =>
        `<option value="${value}" ${value === status ? 'selected' : ''}>${config.icon} ${config.label}</option>`
    ).join('');

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
                <span class="task-date">${createdDate}</span>
            </div>
        </div>
        <select class="status-select status-${status}" onchange="updateTodoStatus(${todo.id}, this.value)" title="Change status">
            ${statusOptions}
        </select>
        <button class="delete-btn" onclick="deleteTodo(${todo.id})" title="Delete task">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6"/>
            </svg>
        </button>
    `;

    return li;
}

// Update statistics display
function updateStats() {
    const total = todos.length;
    const completed = todos.filter(t => t.status === 'completed').length;
    const inProgress = todos.filter(t => t.status === 'in_progress').length;
    const onHold = todos.filter(t => t.status === 'on_hold').length;
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
