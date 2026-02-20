data = json.loads(response.read().decode('utf-8'))
print(json.dumps(data, indent=2))