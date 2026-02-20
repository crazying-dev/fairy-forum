// 后端 API 基础地址
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// 页面加载完成后获取所有待办
document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
    // 绑定添加按钮点击事件
    document.getElementById('add-btn').addEventListener('click', addTodo);
    // 绑定回车事件（输入框按回车也能添加）
    document.getElementById('todo-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTodo();
    });
});

// 1. 获取所有待办事项并渲染到页面
async function fetchTodos() {
    try {
        const response = await fetch(`${API_BASE_URL}/todos`);
        const todos = await response.json();
        const todoList = document.getElementById('todo-list');
        // 清空现有列表
        todoList.innerHTML = '';
        // 渲染每个待办项
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = 'todo-item';
            li.innerHTML = `
                <span>${todo.title}</span>
                <button class="delete-btn" data-id="${todo.id}">删除</button>
            `;
            todoList.appendChild(li);
            // 绑定删除按钮事件
            li.querySelector('.delete-btn').addEventListener('click', () => deleteTodo(todo.id));
        });
    } catch (error) {
        console.error('获取待办失败:', error);
        alert('获取待办事项失败，请检查后端是否启动');
    }
}

// 2. 添加新的待办事项
async function addTodo() {
    const input = document.getElementById('todo-input');
    const title = input.value.trim();
    // 验证输入不为空
    if (!title) {
        alert('请输入待办事项标题');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title }),
        });

        if (response.ok) {
            // 清空输入框
            input.value = '';
            // 重新获取列表（刷新页面）
            fetchTodos();
        } else {
            const error = await response.json();
            alert(error.error || '添加失败');
        }
    } catch (error) {
        console.error('添加待办失败:', error);
        alert('添加失败，请检查后端是否启动');
    }
}

// 3. 删除待办事项
async function deleteTodo(todoId) {
    if (!confirm('确定要删除这个待办吗？')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            // 重新获取列表（刷新页面）
            fetchTodos();
        } else {
            alert('删除失败');
        }
    } catch (error) {
        console.error('删除待办失败:', error);
        alert('删除失败，请检查后端是否启动');
    }
}