import json
import time
import uuid
import socket
from typing import Optional, Any, Dict, List, Tuple, Union
import colorama
import os

colorama.init(autoreset=True)

qp_list: List[str] = ["add", "get", "del", "delete", "return", "run", "stop"]
try:
	with open("from.list", "r", encoding='utf-8') as f:
		from_list = json.loads(f.read())
except FileNotFoundError:
	from_list: List[str] = ["APP", "log", "None"]
adder = 9999
ip = ''
backlog = 5

data: List[Dict[str, Any]] = []


def log(text: str):
	log_dir = "../../任务库处理/logs"
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	# 指定UTF-8编码写入文件
	with open(f"./logs/{time.strftime('%Y-%m-%d')}.log", "a", encoding='utf-8') as f:
		f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {'INFO' if not('error' in text) else 'ERROR'} | {text}\n")
	
	print(
		colorama.Fore.RED + f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {'INFO' if not('error' in text) else 'ERROR'} | {text}")
	return True


class Run:
	def __init__(self):
		pass
	
	def add(self, from_name: str, name: str, message: str, first: int = 1):
		"""
		添加任务
		:param from_name: 发起请求的模块
		:param name: 完成这个任务的模块
		:param message: 这个任务的内容
		:param first: 这个任务的优先级
		:return: 这个任务的ID
		"""
		log(f"start add | from {from_name} | name {name} | message {message} | first {first} | run __add")
		global data
		first = str(first)
		__id = str(uuid.uuid4())
		text: Dict = {
			"from": from_name,
			"name": name,
			"message": message,
			"first": first,
			"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
			"id": __id,
			"return-time": None}
		data.append(text)
		log(f"add | from {from_name} | to {name} of {message} | run __add | {first}")
		return __id
	
	def get(self, __id: str, from_name: str):
		"""
		获取这个任务完成后的返回
		:param __id: 这个任务的ID
		:param from_name: 发起请求的模块
		:return: 任务结果 如果没有任务返回False 任务未完成返回None
		"""
		log(f"start get | from {from_name} | id {__id} | run __get")
		for i in data:
			_id = i["id"]
			if _id == __id:
				log(f"get | from {from_name} | id {__id} | run __get")
				return i.get("return", None)
		log(f"unget | from {from_name} | id {__id} | run __get | error can`t find the id of {__id} in data")
		return False
	
	def delete(self, __id: str, from_name: str) -> bool:
		"""
		删除任务
		:param __id:这个任务的ID
		:param from_name: 发起请求的模块
		:return: 完成情况[bool]
		"""
		log(f"start delete | from {from_name} | id {__id} | run __delete")
		global data
		temp: int = 0
		
		for i in data:
			_id = i["id"]
			if _id == __id:
				del data[temp]
				log(f"deleted | from {from_name} | id {__id} | run __delete")
				return True
			else:
				temp += 1
		log(f"undelete | from {from_name} | id {__id} | run __delete | error can`t find the id of {__id} in data")
		return False
	
	def return_(self, __id: str, from_name: str, message: str):
		"""
		返回任务结果
		:param __id:完成的任务ID
		:param from_name: 发起请求的模块
		:param message: 完成情况
		:return: 完成情况[bool]
		"""
		log(f"start return | from {from_name} | id {__id} | message {message} | run __return")
		temp: int = 0
		
		for i in data:
			_id = i["id"]
			if _id == __id:
				data[temp]["return"] = message
				log(f"get return | from {from_name} | id {__id} | return {message} | run __return")
				return True
			else:
				temp += 1
		log(f"unget return | from {from_name} | id {__id} | return {message} | run __return | error can`t find the id of {__id} in data")
		return False
	
	def run(self, name: str, from_name: str = None) -> Union[list[dict[str, Any]], None, dict[str, Any]]:
		"""
		获取下一个要完成的任务
		:param name: 查找的模块
		:param from_name: 发起任务的模块，默认和name相同
		:return: 最优先的任务
		"""
		if name == "all":
			return data
		from_name = from_name if from_name else name
		log(f"start run | from {from_name} | name {name} | run __run")
		temp: List[Tuple[Dict[str, Any], int]] = []
		temp__: List[Tuple[Dict[str, Any], int]] = []
		temp_: int = 0
		temp___: int = 0
		
		for i in data:
			_name = i["name"]
			if _name == name:
				temp.append((i, temp_))
			else:
				temp_ += 1
		if len(temp) == 0:
			log(f"unrun | from {from_name} | name {name} | run __run | error can`t find the name of {name} in data")
			return None
		
		for i in temp:
			_first = i[0]["first"]
			if _first != str(1):
				temp__.append((i[0], int(_first)))
		
		if len(temp__) == 0:
			return temp[0][0]
		else:
			return self.__find_dict_by_max_int(temp__)
	
	def stop(self, from_name: str):
		"""
		停止任务库运行
		:param from_name: 发起的模块
		:return: None
		"""
		log(f"start stop | from {from_name} | stop __stop")
		exit(0)
	
	def __find_dict_by_max_int(self, data_: List[Tuple[Dict[str, Any], int]]) -> Optional[Dict[str, Any]]:
		"""
		在 List[Tuple[Dict[str, Any], int]] 结构中找到整数最大值对应的第一个字典

		:param data_: 目标数据列表，元素为(字典, 整数)的元组
		:return: 最大值对应的第一个字典；若输入为空列表则返回None
		"""
		# 处理空列表的边界情况
		log(f"start __find_dict_by_max_int | data_ {data_} | run __find_dict_by_max_int")
		if not data_:
			log(f"un__find_dict_by_max_int | data_ {data_} | run __find_dict_by_max_int | error can`t find anything in data_")
			return None
		
		# 初始化最大值和对应字典（默认取第一个元素）
		max_value = -float('inf')
		target_dict = None
		
		# 遍历数据，逐个比较整数大小
		for item_dict, item_int in data_:
			# 仅当当前整数 > 已记录的最大值时，更新（保证多个最大值时取第一个）
			if item_int > max_value:
				max_value = item_int
				target_dict = item_dict
		log(f"find max_value | {max_value} | target_dict | {target_dict} | run __find_dict_by_max_int")
		return target_dict


class web:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((ip, adder))
		self.s.listen(backlog)
		log(f"start TCP | listen ({ip if ip else '0.0.0.0'}||{adder}||{backlog}) | run __web")
		self.run = Run()
		self.main_loop()

	def main_loop(self):
		"""主循环：每次接受一个新连接，处理一个请求后立即关闭"""
		while True:
			try:
				client_socket, client_adder = self.s.accept()
				log(f"TCP | call {client_adder} True ")
				self.handle_client(client_socket, client_adder)
			except Exception as e:
				log(f"TCP | call user False | error {e}")
				# 短暂暂停避免疯狂报错
				time.sleep(0.1)

	def handle_client(self, client_socket: socket.socket, client_adder: tuple):
		"""处理单个客户端请求（接收→处理→发送→关闭）"""
		try:
			# 1. 接收消息（带长度前缀）
			len_data = client_socket.recv(4)
			if not len_data:
				log(f"TCP | Client {client_adder} disconnected without sending data")
				return
			data_len = int.from_bytes(len_data, byteorder='big')
			rec_data = b''
			while len(rec_data) < data_len:
				chunk = client_socket.recv(min(data_len - len(rec_data), 1024))
				if not chunk:
					log(f"TCP | Client {client_adder} disconnected midway")
					return
				rec_data += chunk
			rec_msg = rec_data.decode('utf-8')
			log(f"TCP | Client {client_adder} received {rec_msg}")

			# 2. 解析并处理请求
			response_data = self.process_request(rec_msg)
			response = json.dumps(response_data, ensure_ascii=False)  # 序列化为 JSON 字符串

			# 3. 如果有响应数据，发送给客户端
			if response is not None:
				self.send_response(client_socket, response)
		except Exception as e:
			log(f"TCP | Error processing request from client {client_adder} | error {e}")
		finally:
			client_socket.close()
			log(f"TCP | Connection with client {client_adder} closed")

	def process_request(self, rec_msg: str) -> Union[None, str, bool]:
		"""解析JSON请求并调用Run对应方法，返回需要发送给客户端的字符串（仅add有返回）"""
		try:
			req = json.loads(rec_msg)
		except json.JSONDecodeError:
			return None

		# 合法性校验
		if req.get("from") not in from_list:
			return None
		if req.get("qp") not in qp_list:
			return None
		if not int(int(req["time"]) / 10) == int(time.time() / 10):
			return None
		if "name" not in req:
			return None

		qp = req["qp"]
		from_name = req["name"]

		# 分发请求
		if qp == "add":
			try:
				first = int(req.get("first", 1))
			except ValueError:
				first = 1
			task_id = self.run.add(
				from_name=from_name,
				name=req["to_name"],
				message=req["message"],
				first=first
			)
			return task_id  # add返回ID
		elif qp == "get":
			return self.run.get(req["id"], from_name)
		elif qp in ("del", "delete"):
			return self.run.delete(req["id"], from_name)
		elif qp == "return":
			return self.run.return_(req["id"], from_name, req["message"])
		elif qp == "run":
			name = req.get("find_name", from_name)
			return self.run.run(name=name, from_name=from_name)
		elif qp == "stop":
			return self.run.stop(from_name)
		# 其他方法默认无返回
		return None

	def send_response(self, client_socket: socket.socket, message: str):
		"""向客户端发送响应（带长度前缀）"""
		try:
			msg_bytes = message.encode('utf-8')
			client_socket.send(len(msg_bytes).to_bytes(4, byteorder='big'))
			client_socket.send(msg_bytes)
			log(f"TCP | send {message}")
		except Exception as e:
			log(f"TCP | sned message error | error {e}")

	def __del__(self):
		if self.s:
			try:
				self.s.close()
			except:
				pass


if __name__ == '__main__':
	web()
