from flask import Flask, request, jsonify
from flask_cors import CORS

# 创建 Flask 实例
app = Flask(__name__)
CORS(app)  # 解决跨域

# 定义 POST 接口
@app.route('/submit', methods=['POST'])
def receive_data():
    # 核心：request.get_json() 解析前端发送的 JSON 数据
    user_data = request.get_json()
    if not user_data:
        return jsonify({'success': False, 'message': '未接收到数据'}), 400

    print('接收到前端的数据：', user_data)

    # 验证数据
    if 'username' not in user_data or 'email' not in user_data:
        return jsonify({'success': False, 'message': '用户名或邮箱不能为空'}), 400

    # 返回响应
    return jsonify({
        'success': True,
        'message': '数据接收成功！',
        'data': user_data
    }), 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)  # 启动服务器，debug=True 自动重启