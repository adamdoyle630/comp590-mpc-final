import requests

# Set the URL for the Cloud Function
url = "https://us-east1-outstanding-map-421217.cloudfunctions.net/insert_data"

gpas = [1.32, 2.31, 4.00, 3.11, 1.70, 3.11, 0.71, 3.11, 3.92,  2.11]
ages = [19, 21, 22, 30, 11, 20, 15, 26, 50, 40]
financial_aid = [1000, 2000, 5500, 3500, 10000, 20000, 7500, 0, 200, 3400]

for i in range(len(ages)):
    response = requests.post(url, json={"gpa": gpas[i], "age": ages[i], "financial_aid": financial_aid[i]})

    if response.status_code != 200:
        print(response.text)
    else:
        print(response.json())