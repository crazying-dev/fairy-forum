from api import *

if __name__ == "__main__":
	Config().source_name = "log"
	# 生产者：添加任务
	#for i in range(1, 11):
	producer = TaskQueueClient(to_name="worker", message="测试任务", first=2)
	print(f"任务ID: {producer.id}")
	print(type(producer.id))
	
	# 消费者：获取任务
	consumer = RunAPI()
	task = consumer.run(find_name="worker")
	print("获取到的任务:", task)
	print(type(task))
	
	# 返回结果
	if task:
		consumer.return_("处理成功")
	# 也可以手动指定ID
	# consumer.return_("处理成功", task_id=task["id"])
	
	# 查询所有任务
	all_tasks = consumer.run(find_name="all")
	print("当前所有任务:", all_tasks)

	stop().stop()
