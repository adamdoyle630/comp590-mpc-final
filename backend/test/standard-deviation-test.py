import requests
from nacl.public import SealedBox, PrivateKey
from mpc import MPC_Functions

chosen_statistic = "gpa"

if chosen_statistic not in ["gpa", "age", "financial_aid"]:
    raise

url = "https://us-east1-outstanding-map-421217.cloudfunctions.net"

response = requests.post(f"{url}/calculate_standard_deviation", json={"statistic": chosen_statistic})

if response.status_code != 200:
    print(response.reason)

print(response.text)

# response = requests.post(f"{url}/generate_beaver_triples", json={"count": 3})

# if response.status_code != 200:
#     print(response.reason)
#     raise

# beaver_triples = response.json()

# beaver_triples_party1 = []
# beaver_triples_party2 = []
# beaver_triples_party3 = []

# def decrypt(value, box: SealedBox):
#     decrypted_bytes = box.decrypt(bytes.fromhex(value))
#     return int.from_bytes(decrypted_bytes)

# for beaver_triple in beaver_triples:
#     a_shares = beaver_triple["a_shares"]
#     b_shares = beaver_triple["b_shares"]
#     c_shares = beaver_triple["c_shares"]

#     beaver_triples_party1.append({"a_share": a_shares[0], "b_share": b_shares[0], "c_share": c_shares[0]})
#     beaver_triples_party2.append({"a_share": a_shares[1], "b_share": b_shares[1], "c_share": c_shares[1]})
#     beaver_triples_party3.append({"a_share": a_shares[2], "b_share": b_shares[2], "c_share": c_shares[2]})


# d_shares_p1 = []
# e_shares_p1 = []
# for index, share in enumerate([10, 20, 30]):
#     temp_triples = beaver_triples_party1[index]
#     d_share, e_share = MPC_Functions.generate_beaver_mask(share - mean, share - mean, temp_triples["a_share"], temp_triples["b_share"])
#     d_shares_p1.append(d_share)
#     e_shares_p1.append(e_share)

# party2_results = requests.post(f"{url}/party2_beaver_mask", json={"statistic": chosen_statistic, "a_shares": [share["a_share"] for share in beaver_triples_party2], "b_shares": [share["b_share"] for share in beaver_triples_party2]})

# if party2_results.status_code != 200:
#     print(party2_results.reason, party2_results.text)

# party3_results = requests.post(f"{url}/party3_beaver_mask", json={"statistic": chosen_statistic, "a_shares": [share["a_share"] for share in beaver_triples_party3], "b_shares": [share["b_share"] for share in beaver_triples_party3]})

# if party3_results.status_code != 200:
#     print(party3_results.reason, party3_results.text)

# party2_masked_values = party2_results.json()
# party3_masked_values = party3_results.json()
 
# d_shares_p2 = party2_masked_values.get("d_shares")
# e_shares_p2 = party2_masked_values.get("e_shares")
# d_shares_p3 = party3_masked_values.get("d_shares")
# e_shares_p3 = party3_masked_values.get("e_shares")

# d_shares = []
# e_shares = []

# for i in range(d_shares_p1):
#     d_shares.append([d_shares_p1[i], d_shares_p2[i], d_shares_p3[i]])
#     e_shares.append([e_shares_p1[i], e_shares_p2[i], e_shares_p3[i]])


