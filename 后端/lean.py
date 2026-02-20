from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# 初始化 Flask 应用
app = Flask(__name__)
# 允许跨域请求
CORS(app)


# 初始化数据库
def init_db():
	# 连接 SQLite 数据库（不存在则自动创建）
	conn = sqlite3.connect('todo.db')
	cursor = conn.cursor()
	# 创建待办表
	cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0
        )
    ''')
	conn.commit()
	conn.close()


# 启动时初始化数据库
init_db()


# 1. 获取所有待办事项
@app.route('/api/todos', methods=['GET'])
def get_todos():
	conn = sqlite3.connect('todo.db')
	cursor = conn.cursor()
	cursor.execute('SELECT id, title, completed FROM todos')
	# 将查询结果转为字典列表
	todos = [{'id': row[0], 'title': row[1], 'completed': bool(row[2])} for row in cursor.fetchall()]
	conn.close()
	return jsonify(todos)


# 2. 添加新的待办事项
@app.route('/api/todos', methods=['POST'])
def add_todo():
	# 获取前端传递的 JSON 数据
	data = request.get_json()
	if not data or 'title' not in data:
		return jsonify({'error': '标题不能为空'}), 400
	
	conn = sqlite3.connect('todo.db')
	cursor = conn.cursor()
	cursor.execute('INSERT INTO todos (title) VALUES (?)', (data['title'],))
	conn.commit()
	# 获取新增数据的 ID
	todo_id = cursor.lastrowid
	conn.close()
	
	return jsonify({'id': todo_id, 'title': data['title'], 'completed': False}), 201


# 3. 删除待办事项
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
	conn = sqlite3.connect('todo.db')
	cursor = conn.cursor()
	cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
	conn.commit()
	conn.close()
	
	return jsonify({'message': '删除成功'}), 200


# 启动应用
if __name__ == '__main__':
	# 运行在 5000 端口，开启调试模式
	app.run(debug=True, port=5000)
