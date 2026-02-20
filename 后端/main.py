from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

import tools

database = 'todo.db'
conn = None
cursor = None

# 初始化 Flask 应用
app = Flask(__name__)
# 允许跨域请求
CORS(app)


# 初始化数据库
def init_db():
	global conn, cursor
	# 连接 SQLite 数据库（不存在则自动创建）
	conn = sqlite3.connect(database)
	cursor = conn.cursor()
	# 创建待办表
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Users (
		id INTEGER PRIMARY KEY,
		name TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL,
		email TEXT NOT NULL UNIQUE,
		ip TEXT,
		create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		last_login_time TIMESTAMP
	)
	''')
	conn.commit()
	conn.close()


def new_user_add_in_database(name, password, email, ip):
	UserId = tools.id_to_pure_digits()
	password = tools.加密(password)
	try:
		# 3. 连接数据库（每次操作单独连接，避免全局连接失效）
		conn = sqlite3.connect(database)
		cursor = conn.cursor()
		
		# 4. 插入用户数据（核心SQL：创建用户行）
		insert_sql = '''
	        INSERT INTO Users (id, name, password, email, ip)
	        VALUES (?, ?, ?, ?, ?)
	        '''
		# 用占位符传参，防SQL注入
		cursor.execute(insert_sql, (UserId, name, password, email, ip))
		
		# 5. 提交事务（必须！否则数据不写入）
		conn.commit()
		return {
			"status": "success",
			"message": "用户注册成功",
			"user_id": UserId
		}
	
	except sqlite3.IntegrityError as e:
		# 捕获唯一约束冲突（用户名/邮箱重复）
		if "UNIQUE constraint failed: Users.name" in str(e):
			return {"status": "failed", "message": "用户名已存在"}
		elif "UNIQUE constraint failed: Users.email" in str(e):
			return {"status": "failed", "message": "邮箱已存在"}
		else:
			return {"status": "failed", "message": f"数据约束错误：{str(e)}"}
	
	except Exception as e:
		# 捕获其他异常（如ID重复、字段为空等）
		print(e)
		return {"status": "failed", "message": f"注册失败：{str(e)}"}
	
	finally:
		# 无论是否成功，都关闭数据库连接
		if conn:
			conn.close()


# 启动时初始化数据库
init_db()

if __name__ == '__main__':
    new_user_add_in_database("Alan", "120283", "3890320020@qq.com", "127.0.0.1")