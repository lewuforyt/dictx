import json


config = open(r"C:\Users\acmlk\OneDrive\Masaüstü\SÖZLÜK - Copy\modules\config.json", "r")
config = json.loads(config.read())

mongoDbUri = config["uri"]
secretKey = config["secretKey"]