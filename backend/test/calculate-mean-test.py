import requests

url = "https://us-east1-outstanding-map-421217.cloudfunctions.net/calculate_mean"

# Send the data to the Cloud Function
response = requests.post(url, json={"statistic": "gpa"})

if response.status_code != 200:
    print(response.text)
else:
    print(response.json())