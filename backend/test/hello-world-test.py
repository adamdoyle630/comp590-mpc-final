import requests

# Set the URL for the Cloud Function
url = "https://us-east1-outstanding-map-421217.cloudfunctions.net/hello_world"

# Send the data to the Cloud Function
response = requests.get(url)

# Print the response
print(response.text)

# import numpy as np
# from scipy import fft
# import math

# A = np.ones((100, 100))
# B = np.random.uniform(0, 2 * np.pi, (100, 100))

# wavefront = 1 * np.e ** (B*1j)

# fourier_transform = fft.fft(wavefront)

# print(fourier_transform)