import flask
import firebase_admin
from firebase_admin import firestore
from mpc import MPC_Functions
from nacl.public import SealedBox, PrivateKey
import os

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()

def party3_sum(request: flask.Request) -> flask.Response:
    form_data = request.get_json()

    chosen_statistic = form_data.get("statistic").lower()

    if chosen_statistic not in ["gpa", "age", "financial_aid"]:
        return flask.Response(f"Invalid chosen statistics: {chosen_statistic}", status=401)
    
    db = firestore.client(app)

    party1_ref = db.collection("party3")
    docs = party1_ref.stream()

    shares = []

    for doc in docs:
        doc_dict = doc.to_dict()
        shares.append(doc_dict.get(chosen_statistic))

    party3_sum = MPC_Functions.calculate_sum_of_shares(shares)

    return flask.jsonify({"data": party3_sum})

def party3_beaver_mask(request: flask.Request) -> flask.Response:
    form_data = request.get_json()

    chosen_statistic_1 = form_data.get("statistic1").lower()
    chosen_statistic_2 = form_data.get("statistic2").lower()
    encrypted_a_shares = form_data.get("a_shares")
    encrypted_b_shares = form_data.get("b_shares")
    sk = os.environ["SK2"]

    if chosen_statistic_1 not in ["gpa", "age", "financial_aid"]:
        return flask.Response(f"Invalid chosen statistics: {chosen_statistic_1}", status=401)
    
    if chosen_statistic_2 not in ["gpa", "age", "financial_aid"]:
        return flask.Response(f"Invalid chosen statistics: {chosen_statistic_2}", status=401)
    
    db = firestore.client(app)

    party3_ref = db.collection("party3")
    docs = party3_ref.stream()

    shares1 = []
    shares2 = []

    for doc in docs:
        doc_dict = doc.to_dict()
        shares1.append(doc_dict.get(chosen_statistic_1))
        shares2.append(doc_dict.get(chosen_statistic_2))

    unseal_box_party3 = SealedBox(PrivateKey(bytes.fromhex(sk)))

    def decrypt(value):
        decrypted_bytes = unseal_box_party3.decrypt(bytes.fromhex(value))
        return int.from_bytes(decrypted_bytes)
    
    a_shares = [decrypt(share) for share in encrypted_a_shares]
    b_shares = [decrypt(share) for share in encrypted_b_shares]

    d_shares = []
    e_shares = []

    for index in range(len(shares1)):
        d_share, e_share = MPC_Functions.generate_beaver_mask(shares1[index], shares2[index], a_shares[index], b_shares[index])
        d_shares.append(d_share)
        e_shares.append(e_share)

    return flask.jsonify({"d_shares": d_shares, "e_shares": e_shares})

def party3_beaver_compute(request: flask.Request) -> flask.Response:
    form_data = request.get_json()

    chosen_statistic_1 = form_data.get("statistic1").lower()
    chosen_statistic_2 = form_data.get("statistic2").lower()
    encrypted_c_shares = form_data.get("c_shares")
    d_shares = form_data.get("d_shares")
    e_shares = form_data.get("e_shares")
    sk = os.environ["SK2"]

    if chosen_statistic_1 not in ["gpa", "age", "financial_aid"]:
        return flask.Response(f"Invalid chosen statistics: {chosen_statistic_1}", status=401)
    
    if chosen_statistic_2 not in ["gpa", "age", "financial_aid"]:
        return flask.Response(f"Invalid chosen statistics: {chosen_statistic_2}", status=401)
    
    if not encrypted_c_shares:
        return flask.Response("Provide a c_share", status=401)
    
    db = firestore.client(app)

    party3_ref = db.collection("party3")
    docs = party3_ref.stream()

    shares1 = []
    shares2 = []

    for doc in docs:
        doc_dict = doc.to_dict()
        shares1.append(doc_dict.get(chosen_statistic_1))
        shares2.append(doc_dict.get(chosen_statistic_2))

    unseal_box_party3 = SealedBox(PrivateKey(bytes.fromhex(sk)))

    def decrypt(value):
        decrypted_bytes = unseal_box_party3.decrypt(bytes.fromhex(value))
        return int.from_bytes(decrypted_bytes)

    c_shares = [decrypt(share) for share in encrypted_c_shares]

    z_shares = []

    for index in range(len(shares1)):
        z_share = MPC_Functions.beaver_compute(shares1[index], shares2[index], c_shares[index], d_shares[index], e_shares[index])

        z_shares.append(z_share)

    print(z_shares)

    return flask.jsonify({"data": MPC_Functions.calculate_sum_of_shares(z_shares)})