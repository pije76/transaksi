import requests


base_url = "http://localhost:8000"

login_url = base_url + "/login"
login_data = {"username": "admin", "password": "password"}
response = requests.post(login_url, json=login_data)
print(response)
token = response.json()["token"]
headers = {"Authorization": f"Bearer {token}"}
print(headers)  # {'Authorization': 'Bearer eyJh... and so on'}

items_url = base_url + "/items"
response = requests.get(items_url, headers=headers)
print(response.json()) # {'detail': [{'loc': ['query', 'kwargs'],
                       # 'msg': 'field required', 'type': 'value_error.missing'}]}

item_id = 1
item_url = f"{base_url}/items/{item_id}"
response = requests.get(item_url, headers=headers)
print(response.json()) # {'detail': [{'loc': ['query', 'kwargs'],
                       # 'msg': 'field required', 'type': 'value_error.missing'}]}
