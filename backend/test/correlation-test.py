import requests
from nacl.public import SealedBox, PrivateKey
from mpc import MPC_Functions

chosen_statistic_1 = "age"
chosen_statistic_2 = "financial_aid"

url = "https://us-east1-outstanding-map-421217.cloudfunctions.net"

response = requests.post(f"{url}/calculate_correlation", json={"statistic1": chosen_statistic_1, "statistic2": chosen_statistic_2})

if response.status_code != 200:
    print(response.reason)

print(response.text)