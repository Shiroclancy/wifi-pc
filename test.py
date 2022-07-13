import json
x = {"name" : "ok", "age" : 20}
print(type(x),x)
x = json.dumps(x)
print(type(x),x)
x = json.loads(x)
print(type(x),x)