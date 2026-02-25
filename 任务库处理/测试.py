import api

path = "./A.py"

text = api.TaskAPI(path)
text.add("log", "123")

text1 = api.TaskAPI(path)
print(text1.run("log"))
text1.send("345")

print(text.get())
