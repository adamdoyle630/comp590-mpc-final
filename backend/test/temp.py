import flask
import firebase_admin
from firebase_admin import firestore
from mpc import MPC_Functions
import requests
import math
from nacl.public import SealedBox, PrivateKey


# Get statistic to calculate sd for
chosen_statistic = "age"

url = "https://us-east1-outstanding-map-421217.cloudfunctions.net"

# Calculate the mean of the chosen statistics
response = requests.post(f"{url}/calculate_mean", json={"statistic": chosen_statistic})

mean = int(response.json()["mean"])

print(mean)

# Get all documents from party 1 and this will set many variables such as number of beaver triples

shares = [668776771]

# Generate beaver triples for each of the shares we have to calculate squared difference
response = requests.post(f"{url}/generate_beaver_triples", json={"count": len(shares)})

temp = response.json()

# Get an array of beaver triple objects that each have 3 shares of a, b, c with the last 2 encrypted
beaver_triples = [{
    'a_shares': [1286805614, 1307462954, 304835607], 
    'b_shares': [701621459, 136899746, 124890706], 
    'c_shares': [340818287, 1396358873, 1108035185]
}]

# Arrays for beaver triples for each of the parties
beaver_triples_party1 = []
beaver_triples_party2 = []
beaver_triples_party3 = []

# Iterate through each beaver triple in beaver triples which represents one set of multiplication
for beaver_triple in beaver_triples:
    a_shares = beaver_triple["a_shares"]
    b_shares = beaver_triple["b_shares"]
    c_shares = beaver_triple["c_shares"]

    # Party 1 will get first share from a, b, and c which is unencrypted
    beaver_triples_party1.append({"a_share": a_shares[0], "b_share": b_shares[0], "c_share": c_shares[0]})

    # Party 2 and 3 will get encrypted shares that are encrypted under the public key of the parties
    beaver_triples_party2.append({"a_share": a_shares[1], "b_share": b_shares[1], "c_share": c_shares[1]})
    beaver_triples_party3.append({"a_share": a_shares[2], "b_share": b_shares[2], "c_share": c_shares[2]})

    # unseal_box_party2 = SealedBox(PrivateKey(bytes.fromhex("a87fdd552ad9b7c143f4fe27bf1a83d02e1e7f48549e40a396aab5e2d908fd59")))
    # unseal_box_party3 = SealedBox(PrivateKey(bytes.fromhex("775236c3be6ab91f6f6ffbad702e8227c98c16d851f8e4e17302b19c8e08e666")))

    # val1 = int.from_bytes(unseal_box_party2.decrypt(bytes.fromhex(a_shares[1])))
    # val2 = int.from_bytes(unseal_box_party3.decrypt(bytes.fromhex(a_shares[2])))

    # val3 = int.from_bytes(unseal_box_party2.decrypt(bytes.fromhex(b_shares[1])))
    # val4 = int.from_bytes(unseal_box_party3.decrypt(bytes.fromhex(b_shares[2])))

    # val5 = int.from_bytes(unseal_box_party2.decrypt(bytes.fromhex(c_shares[1])))
    # val6 = int.from_bytes(unseal_box_party3.decrypt(bytes.fromhex(c_shares[2])))


    print("A Value: ", MPC_Functions.calculate_sum_of_shares(a_shares))
    print("B Value: ", MPC_Functions.calculate_sum_of_shares(b_shares))
    print("C Value: ", MPC_Functions.calculate_sum_of_shares(c_shares))
    print("AB Value: ", MPC_Functions.calculate_sum_of_shares(a_shares) * MPC_Functions.calculate_sum_of_shares(b_shares) % (2 ** 31 - 1))

# Set lists for the masked values that will be generated by this party
d_shares_p1 = []
e_shares_p1 = []
for index, share in enumerate(shares):
    temp_triples = beaver_triples_party1[index]
    d_share, e_share = MPC_Functions.generate_beaver_mask(share - mean, share - mean, temp_triples["a_share"], temp_triples["b_share"])
    d_shares_p1.append(d_share)
    e_shares_p1.append(e_share)

    print(d_share, e_share)

# Get masked values from party 2 given all the shares of a and b, giving us len(shares) masked pairs of d and e
party2_results = requests.post(f"{url}/party2_beaver_mask", json={"statistic": chosen_statistic, "a_shares": [share["a_share"] for share in beaver_triples_party2], "b_shares": [share["b_share"] for share in beaver_triples_party2]})
if party2_results.status_code != 200:
    flask.Response(f"Failed to get second party's masked values", status=500)

    # Get masked values from party 3 given all the shares of a and b, giving us len(shares) masked pairs of d and e
party3_results = requests.post(f"{url}/party3_beaver_mask", json={"statistic": chosen_statistic, "a_shares": [share["a_share"] for share in beaver_triples_party3], "b_shares": [share["b_share"] for share in beaver_triples_party3]})
if party3_results.status_code != 200:
    flask.Response(f"Failed to get third party's masked values", status=500)

party2_masked_values = party2_results.json()
party3_masked_values = party3_results.json()

print(party2_masked_values)
print(party3_masked_values)

# Get all values from json objects
d_shares_p2 = party2_masked_values.get("d_shares")
e_shares_p2 = party2_masked_values.get("e_shares")
d_shares_p3 = party3_masked_values.get("d_shares")
e_shares_p3 = party3_masked_values.get("e_shares")

d_shares = []
e_shares = []

# Generate a list of lists where each sublist is a full set of d shares 
# and e shares that add to a d & e pair for a single multiplication
for i in range(len(d_shares_p1)):
    d_shares.append([d_shares_p1[i], d_shares_p2[i], d_shares_p3[i]])
    e_shares.append([e_shares_p1[i], e_shares_p2[i], e_shares_p3[i]])

    print("D Value: ", MPC_Functions.calculate_sum_of_shares(d_shares[i]))
    print("E Value: ", MPC_Functions.calculate_sum_of_shares(e_shares[i]))

z_shares_p1 = []
for index, share in enumerate(shares): 
    temp_triples = beaver_triples_party1[index]
    z_share = MPC_Functions.beaver_compute(share - mean, share - mean, temp_triples["c_share"], d_shares[index], e_shares[index], True)

    z_shares_p1.append(z_share)
    print(z_share)
party1_z_sum = MPC_Functions.calculate_sum_of_shares(z_shares_p1)

party2_results = requests.post(f"{url}/party2_beaver_compute", json={"statistic": chosen_statistic, "c_shares": [share["c_share"] for share in beaver_triples_party2], "d_shares": d_shares, "e_shares": e_shares})
if party2_results.status_code != 200:
    flask.Response(f"Failed to get second party's computed value", status=500)

print([share["c_share"] for share in beaver_triples_party3])
print(MPC_Functions.calculate_sum_of_shares(d_shares[0]))
print(MPC_Functions.calculate_sum_of_shares(e_shares[0]))

party3_results = requests.post(f"{url}/party3_beaver_compute", json={"statistic": chosen_statistic, "c_shares": [share["c_share"] for share in beaver_triples_party3], "d_shares": d_shares, "e_shares": e_shares})
if party3_results.status_code != 200:
    flask.Response(f"Failed to get third party's computed values", status=500)

party2_z_sum = party2_results.json()["data"]
party3_z_sum = party3_results.json()["data"]

print(party2_z_sum)
print(party3_z_sum)

squared_sum = MPC_Functions.calculate_sum_of_shares([party1_z_sum, party2_z_sum, party3_z_sum])

standard_deviation = math.sqrt(squared_sum) / len(shares)

print(standard_deviation)