import configparser
import os
import subprocess
import uuid
from datetime import datetime, timezone
import time
import bcrypt
import chardet


def read_ini_file(ini_path="./config.ini", section=None):
	"""
	读取INI配置文件

	Args:
		ini_path (str): INI文件路径
		section (str, optional): 指定要读取的节，None则返回所有节

	Returns:
		dict: 读取到的配置字典，格式如 {section: {key: value, ...}}
	"""
	# 检查文件是否存在
	if not os.path.exists(ini_path):
		raise FileNotFoundError(f"INI文件不存在：{ini_path}")
	
	# 创建配置解析器对象
	config = configparser.ConfigParser()
	# 读取INI文件（支持UTF-8编码，避免中文乱码）
	config.read(ini_path, encoding="utf-8")
	
	# 存储解析后的配置
	config_dict = {}
	
	# 确定要读取的节列表
	sections_to_read = [section] if section else config.sections()
	
	for sec in sections_to_read:
		if sec not in config.sections():
			raise ValueError(f"INI文件中不存在节：{sec}")
		
		# 读取当前节的所有键值对
		config_dict[sec] = {}
		for key, value in config.items(sec):
			# 自动转换常见类型（布尔值、整数、浮点数）
			# 处理布尔值
			if value.lower() in ("true", "false"):
				config_dict[sec][key] = value.lower() == "true"
			# 处理整数
			elif value.isdigit():
				config_dict[sec][key] = int(value)
			# 处理浮点数
			elif "." in value and all(part.isdigit() for part in value.split(".") if part):
				config_dict[sec][key] = float(value)
			# 其他保持字符串
			else:
				config_dict[sec][key] = value
	
	return config_dict


def run_exe_with_params(exe_path, params_dict, param_style="-"):
	"""
	运行带参数的exe程序（修复编码问题）

	Args:
		exe_path (str): exe文件的路径
		params_dict (dict): 参数字典，如 {'o': 'main.txt', 'name': 'test'}
		param_style (str): 参数前缀，可选 '--'（长参数）或 '-'（短参数）

	Returns:
		tuple: (返回码, 标准输出, 标准错误)
	"""
	# 验证参数前缀是否合法
	if param_style not in ("--", "-"):
		raise ValueError("param_style 只能是 '--' 或 '-'")
	
	# 将参数字典转换为命令行参数列表
	cmd_args = [exe_path]
	for key, value in params_dict.items():
		cmd_args.append(f"{param_style}{key}")
		if value is not None:
			cmd_args.append(str(value))
	
	try:
		# 执行exe程序，先捕获字节流（不指定encoding）
		result = subprocess.run(
			cmd_args,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=False,  # 关键：先以字节模式读取，避免直接解码
			creationflags=subprocess.CREATE_NO_WINDOW  # 可选：隐藏exe的命令行窗口
		)
		
		# 自动检测输出编码（优先适配Windows的gbk）
		def decode_output(byte_data):
			if not byte_data:
				return ""
			# 第一步：尝试自动检测编码
			detected = chardet.detect(byte_data)
			encoding = detected["encoding"] or "gbk"
			# 第二步：优先用gbk（Windows默认），失败则用ignore忽略错误
			try:
				return byte_data.decode(encoding)
			except:
				return byte_data.decode("gbk", errors="ignore")  # 兜底方案
		
		# 解码stdout和stderr
		stdout = decode_output(result.stdout)
		stderr = decode_output(result.stderr)
		
		return result.returncode, stdout, stderr
	
	except FileNotFoundError:
		return -1, "", f"错误：找不到exe文件 '{exe_path}'"
	except Exception as e:
		return -1, "", f"执行出错：{str(e)}"


def log(head, message, error_level: int = 3):
	path = read_ini_file()["path"]["log"]
	run_exe_with_params(path, {"m": message, "H": head, "e": error_level}, param_style="-")


def timestamp_tool(timestamp: int = None) -> int:
	"""
	忽略时区差异的UTC时间戳工具函数（机器友好，无需人读）
	:param timestamp: 仅"calc_diff"时需要，传入待对比的UTC时间戳（秒级）
	:return: 结果字典，包含状态和数据（机器可读）
	"""
	# 统一返回格式（机器友好，无冗余字符串）
	result = {"status": "success", "data": None, "error": None}
	
	try:
		if not timestamp:
			# 1. 获取当前UTC时间戳（秒级，忽略时区，数字格式）
			current_utc_ts = int(datetime.now(timezone.utc).timestamp())
			result["data"] = current_utc_ts
		
		elif timestamp:
			# 2. 计算时间差（当前UTC时间 - 传入的UTC时间戳），单位：秒
			if timestamp is None:
				raise ValueError("calc_diff操作必须传入timestamp参数")
			current_utc_ts = int(datetime.now(timezone.utc).timestamp())
			time_diff_seconds = current_utc_ts - timestamp  # 差值为正：传入时间在过去；为负：传入时间在未来
			result["data"] = time_diff_seconds
	
	except Exception as e:
		result["status"] = "failed"
		result["error"] = str(e)
	
	return int(result["data"])


def 加密(a):
	password = str(a).encode('utf-8')  # 转为字节串
	hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
	return hashed_password


def 验证(a, b):
	return bcrypt.checkpw(str(a).encode(), b)


def __uuid4_to_pure_digits():
	try:
		# 生成uuid4对象
		uuid_obj = uuid.uuid4()
		# 转换为128位整数（UUID本质）
		uuid_int = int(uuid_obj)
		log(head='INFO', message=f'Get uuid for user to as id , the uuid is {uuid_int}')
		return uuid_int
	except Exception as e:
		log(head="ERROR", message=f"Happen the ERROR when get uuid for user to as id \n the ERROR is {e}")


def id_to_pure_digits(uuid_int=__uuid4_to_pure_digits()):
	try:
		temp = ""
		for i in str(time.time()):
			i = ord(i)
			temp = temp + str(i)
		temp = temp[::-1]
		temp = int(temp[10::])
		uuid_int = str(uuid_int)[::-1]
		uuid_int = int((uuid_int * 10)[::-2][10::])
		output = int(str(temp + uuid_int)[0:20:1])
		log(head='INFO', message=f'Get id for user as id , the id is {output}')
		return output
	except Exception as e:
		log(head="ERROR", message=f"Happen the ERROR when get id for user as id \n the ERROR is {e}")
