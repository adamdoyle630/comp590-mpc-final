import flask
from mpc import MPC_Functions
from nacl.public import PublicKey, SealedBox
import os

def generate_beaver_triples(request: flask.Request) -> flask.Response:

    request_data = request.get_json()

    triple_count = request_data.get("count", -1)

    if triple_count == -1:
        return flask.Response("Please provide a count of beaver triples")
    
    pk1 = os.environ["PK1"]
    pk2 = os.environ["PK2"]
    
    triples = []

    for _ in range(triple_count):
        sealed_box_1 = SealedBox(PublicKey(public_key=bytes.fromhex(pk1)))
        sealed_box_2 = SealedBox(PublicKey(public_key=bytes.fromhex(pk2)))      

        beaver_triples = MPC_Functions.generate_beavers(3)

        a_shares = [beaver_triples[0][0], sealed_box_1.encrypt(beaver_triples[0][1].to_bytes(length=4, byteorder="big")).hex(), sealed_box_2.encrypt(beaver_triples[0][2].to_bytes(length=4, byteorder="big")).hex()]
        b_shares = [beaver_triples[1][0], sealed_box_1.encrypt(beaver_triples[1][1].to_bytes(length=4, byteorder='big')).hex(), sealed_box_2.encrypt(beaver_triples[1][2].to_bytes(length=4, byteorder="big")).hex()]
        c_shares = [beaver_triples[2][0], sealed_box_1.encrypt(beaver_triples[2][1].to_bytes(length=4, byteorder='big')).hex(), sealed_box_2.encrypt(beaver_triples[2][2].to_bytes(length=4, byteorder="big")).hex()]

        triples.append({"a_shares": a_shares, "b_shares": b_shares, "c_shares": c_shares})

    return flask.jsonify(triples)

