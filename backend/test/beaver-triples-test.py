import requests

url = "https://us-east1-outstanding-map-421217.cloudfunctions.net/generate_beaver_triples"

# Send the data to the Cloud Function
response = requests.post(url, json={"count": 100})

if response.status_code != 200:
    print(response.text)
else:
    data = response.json()

    print(len(data))