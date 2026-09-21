
import requests

url = "http://127.0.0.1:8000/ask"
payload = {"question": "Who is Harsh Dubey?"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload)
print("Status:", response.status_code)
print("Response:", response.text)
