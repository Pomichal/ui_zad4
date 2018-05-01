import json

with open('rules.json') as data_file:
    data = json.load(data_file)
    row = data["rules"]

print(row.get("rodic1"))



