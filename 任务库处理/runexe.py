import os
import sys
import ctypes
import ctypes.wintypes


def run_exe_as_standalone(exe_path, params=None, run_as_admin=False):
	"""
	以独立方式运行exe（如同手动双击），支持：
	- 相对路径/绝对路径
	- 字典格式参数传入
	- 可选管理员权限运行
	:param exe_path: exe文件的相对路径或绝对路径
	:param params: 传入exe的参数字典，如 {"mode": "fast", "output": "result.txt"}
	:param run_as_admin: 是否以管理员权限运行（True/False）
	:return: 启动的exe绝对路径 + 最终执行的命令行
	"""
	# ===================== 步骤1：处理路径（相对→绝对） =====================
	# 方案A：基于当前运行目录解析
	abs_exe_path = os.path.normpath(os.path.abspath(exe_path))
	# 方案B：基于脚本文件所在目录解析（如需启用，注释A，取消注释B）
	# script_dir = os.path.dirname(os.path.abspath(__file__))
	# abs_exe_path = os.path.normpath(os.path.join(script_dir, exe_path))
	
	# ===================== 步骤2：校验exe文件 =====================
	if not os.path.exists(abs_exe_path):
		raise FileNotFoundError(
			f"exe文件不存在！\n目标路径：{abs_exe_path}\n当前工作目录：{os.getcwd()}"
		)
	if not abs_exe_path.lower().endswith(".exe"):
		raise ValueError(f"不是有效的exe文件！路径：{abs_exe_path}")
	
	# ===================== 步骤3：处理字典参数 =====================
	cmd_params = []
	if params and isinstance(params, dict):
		for key, value in params.items():
			# 自定义参数格式（按需修改，示例为 key=value）
			# 如需改为 --key=value：cmd_params.append(f"--{key}={value}")
			# 如需改为 /key:value：cmd_params.append(f"/{key}:{value}")
			cmd_params.append(f"{key}={value}")
		# 布尔值特殊处理（可选）：True仅传key，False不传
		# if isinstance(value, bool):
		#     if value:
		#         cmd_params.append(f"--{key}")
		# else:
		#     cmd_params.append(f"--{key}={value}")
	
	# 拼接完整参数字符串（处理空格）
	full_params = ' '.join(cmd_params)
	full_command = f'"{abs_exe_path}" {full_params}'.strip()
	
	# ===================== 步骤4：启动exe（支持管理员权限） =====================
	try:
		if sys.platform != "win32":
			raise RuntimeError("管理员权限运行功能仅支持Windows系统！")
		
		# Windows API 常量定义
		SW_SHOWNORMAL = 1  # 正常显示窗口
		SEE_MASK_NOCLOSEPROCESS = 0x00000040
		if run_as_admin:
			# 管理员权限启动：触发UAC提示
			SHELLEXECUTEINFO = ctypes.Structure(
				'_SHELLEXECUTEINFO',
				[
					('cbSize', ctypes.wintypes.DWORD),
					('fMask', ctypes.wintypes.DWORD),
					('hwnd', ctypes.wintypes.HWND),
					('lpVerb', ctypes.c_wchar_p),
					('lpFile', ctypes.c_wchar_p),
					('lpParameters', ctypes.c_wchar_p),
					('lpDirectory', ctypes.c_wchar_p),
					('nShow', ctypes.wintypes.INT),
					('hInstApp', ctypes.wintypes.HINSTANCE),
					('lpIDList', ctypes.c_void_p),
					('lpClass', ctypes.c_wchar_p),
					('hKeyClass', ctypes.wintypes.HKEY),
					('dwHotKey', ctypes.wintypes.DWORD),
					('hIconOrMonitor', ctypes.wintypes.HANDLE),
					('hProcess', ctypes.wintypes.HANDLE),
				]
			)
			
			sei = SHELLEXECUTEINFO()
			sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
			sei.fMask = SEE_MASK_NOCLOSEPROCESS
			sei.hwnd = None
			sei.lpVerb = "runas"  # 关键：指定管理员权限
			sei.lpFile = abs_exe_path
			sei.lpParameters = full_params
			sei.lpDirectory = os.path.dirname(abs_exe_path)
			sei.nShow = SW_SHOWNORMAL
			
			# 调用ShellExecuteExW API启动exe
			success = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))
			if not success:
				raise RuntimeError("管理员权限启动失败！可能是用户取消了UAC授权")
		else:
			# 普通权限启动（原有逻辑）
			os.startfile(abs_exe_path, arguments=full_params)
		
		# 输出启动信息
		print(f"✅ 启动成功！")
		print(f"   权限模式：{'管理员' if run_as_admin else '普通'}")
		print(f"   exe路径：{abs_exe_path}")
		print(f"   执行命令：{full_command}")
		return abs_exe_path, full_command
	
	except Exception as e:
		raise RuntimeError(
			f"启动exe失败：{str(e)}\n执行命令：{full_command}\n权限模式：{'管理员' if run_as_admin else '普通'}"
		)


# ===================== 示例调用 =====================
if __name__ == "__main__":
	# 示例1：普通权限 + 相对路径 + 字典参数
	# exe_path = "./test.exe"
	# params = {"mode": "fast", "output": "result.txt", "count": 100}
	# run_exe_as_standalone(exe_path, params, run_as_admin=False)
	
	# 示例2：管理员权限 + 绝对路径 + 无参数
	exe_path = r"C:\Windows\System32\cmd.exe"
	params = {"k": None}  # cmd.exe 参数/k：执行后不关闭窗口
	run_exe_as_standalone(exe_path, params, run_as_admin=True)
	
	# Python主程序继续执行
	print("\n📌 Python程序继续运行，exe已独立启动...")