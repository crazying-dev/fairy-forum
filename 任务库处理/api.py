import json
import os
import socket
import time
from typing import Optional, Dict, Any, Union, List


class ModNameError(Exception):
	pass


class Config:
	log_dir = "./client_logs"
	server_host: str = '127.0.0.1'
	server_port: int = 9999
	log_enabled: bool = True
	source_name: str = "None"
	path: str = "./A.exe"


class BaseClient(Config):
	"""客户端基类，封装网络通信和日志"""
	
	def __init__(self):
		if not self.source_name and type(self.source_name) is not str:
			raise ModNameError(f"The mod name is error ,mod name:{self.source_name}")

	def log(self, text: str, level: str = "INFO"):
		if not self.log_enabled:
			return
		os.makedirs(self.log_dir, exist_ok=True)
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		log_line = f"{timestamp} | {level} | {text}"
		with open(f"{self.log_dir}/{time.strftime('%Y-%m-%d')}.log", "a", encoding='utf-8') as f:
			f.write(log_line + "\n")
	
	# print(f"\033[91m{log_line}\033[0m")
	
	def _send_request(self, qp: str, **kwargs) -> Any:
		"""发送请求，返回解析后的响应数据（可能为任意类型）"""
		request = {
			"from": self.source_name,
			"qp": qp,
			"time": str(int(time.time())),
			"name": kwargs.get("name", self.source_name),
		}
		request.update(kwargs)
		json_data = json.dumps(request, ensure_ascii=False)
		self.log(f"send | {json_data}")
		
		# 建立连接
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.server_host, self.server_port))
		except Exception as e:
			self.log(f"连接服务器失败: {e}", "ERROR")
			return None
		
		try:
			# 发送
			msg_bytes = json_data.encode('utf-8')
			sock.send(len(msg_bytes).to_bytes(4, 'big'))
			sock.send(msg_bytes)
			
			# 接收响应（服务器可能不返回，此时 recv 会阻塞？但服务器现在总是返回）
			len_data = sock.recv(4)
			if not len_data:
				self.log("服务器未返回数据", "WARN")
				return None
			data_len = int.from_bytes(len_data, 'big')
			recv_data = b''
			while len(recv_data) < data_len:
				chunk = sock.recv(min(data_len - len(recv_data), 1024))
				if not chunk:
					self.log("接收响应时连接断开", "ERROR")
					return None
				recv_data += chunk
			response_str = recv_data.decode('utf-8')
			self.log(f"收到响应: {response_str}")
			
			# 解析响应（服务器统一返回 JSON 字符串）
			return json.loads(response_str)
		except json.JSONDecodeError:
			self.log("响应不是有效的JSON", "ERROR")
			return None
		except Exception as e:
			self.log(f"通信异常: {e}", "ERROR")
			return None
		finally:
			sock.close()
			self.log("连接已关闭")


class TaskQueueClient(BaseClient):
	"""任务生产者：添加任务，并对特定任务进行查询/删除"""
	
	def __init__(self, to_name: str, message: str, first: int = 1):
		super().__init__()
		# 添加任务，保存返回的ID
		self.id = self._send_request(
			qp="add",
			name=self.source_name,
			to_name=to_name,
			message=message,
			first=str(first)
		)
		if self.id is not None:
			self.log(f"任务创建成功，ID: {self.id}")
		else:
			self.log(f"处理文件未启动，尝试启动")
			
	
	def get(self) -> Any:
		"""获取任务结果，返回服务器响应的原始数据"""
		return self._send_request(
			qp="get",
			name=self.source_name,
			id=self.id
		)
	
	def delete(self) -> bool:
		"""删除任务，返回布尔值"""
		result = self._send_request(
			qp="delete",
			name=self.source_name,
			id=self.id
		)
		return bool(result)  # 服务器返回 True/False 字符串，解析后为 bool


class stop(BaseClient):
	def stop(self) -> bool:
		"""停止服务器"""
		result = self._send_request(
			qp="stop",
			name=self.source_name
		)
		return bool(result)


class RunAPI(BaseClient):
	"""任务消费者：获取任务并处理"""
	def __init__(self):
		super().__init__()
		self.current_task: Optional[Dict[str, Any]] = None  # 最近获取的任务
	
	def run(self, find_name: Optional[str] = None) -> Union[Dict, List, None]:
		"""
		获取下一个任务。
		如果 find_name 为 "all"，返回所有任务列表。
		否则返回单个任务字典，并自动将任务 ID 保存到 self.current_task。
		"""
		kwargs = {"name":self.source_name}
		if find_name is not None:
			kwargs["find_name"] = find_name
		
		result = self._send_request(qp="run", **kwargs)
		
		if find_name == "all":
			# 返回列表，不更新当前任务
			return result if isinstance(result, list) else []
		else:
			# 预期返回单个任务字典
			if isinstance(result, dict) and "id" in result:
				self.current_task = result
				self.log(f"获取到任务: {result['id']}")
			else:
				self.current_task = None
			return result
	
	def return_(self, message: str, task_id: Optional[str] = None) -> bool:
		"""
		返回任务结果。如果未提供 task_id，则使用 self.current_task 的 id。
		"""
		tid = task_id or (self.current_task and self.current_task.get("id"))
		if not tid:
			self.log("无法返回：没有可用的任务ID", "ERROR")
			return False
		result = self._send_request(
			qp="return",
			name=self.source_name,
			id=tid,
			message=message
		)
		return bool(result)
	
	def delete(self, task_id: Optional[str] = None) -> bool:
		"""删除任务，参数同 return_"""
		tid = task_id or (self.current_task and self.current_task.get("id"))
		if not tid:
			self.log("无法删除：没有可用的任务ID", "ERROR")
			return False
		result = self._send_request(
			qp="delete",
			name=self.source_name,
			id=tid
		)
		return bool(result)