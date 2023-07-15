import json

from django.test import TestCase

import requests

headers = {
    "Cookie": ""
}

r = requests.post("http://192.168.0.106:8000/api/v1/tasks/delete-by-pid/124251", )
response = json.loads(r.content)

print(response)