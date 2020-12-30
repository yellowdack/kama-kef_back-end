import requests

class requests:

    response = requests.get("http://127.0.0.1:5000")
    jsonObj = response.json()
    print(jsonObj)

    response = requests.post("http://127.0.0.1:5000/quarks", json={"name":"top","charge":"+2/3"})
    response.json()