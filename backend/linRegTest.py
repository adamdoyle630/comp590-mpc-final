import requests
import json
import numpy as np

# Generate some dummy data for linear regression
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Prepare the data to be sent as JSON
data = {
    'X': X.tolist(),
    'y': y.tolist()
}

# Set the URL for the Cloud Function
url = 'https://us-central1-mpc-model.cloudfunctions.net/linReg'

# Send the data to the Cloud Function
response = requests.post(url, json=data)

# Print the response
print(response.json() if response.status_code == 200 else response.text)