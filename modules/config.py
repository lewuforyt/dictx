import json


config = open(r"config.json", "r")
config = json.loads(config.read())

mongoDbUri = config["uri"]
secretKey = config["secretKey"]
