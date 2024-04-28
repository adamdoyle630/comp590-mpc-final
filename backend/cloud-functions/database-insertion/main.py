import flask
import firebase_admin
from firebase_admin import firestore
from mpc import MPC_Functions

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()

def insert_data(request: flask.Request) -> flask.Response:
    """HTTP Cloud Function to insert 

    Returns:
    - int: number of parties that recieved shares
    - int: number of different data points inserted
    """

    if request.method != "POST":
        return flask.Response("Method not allowed (Please use post request)", status=405)
    
    form_data = request.get_json()

    gpa = int(form_data.get("gpa") * 100)
    age = int(form_data.get("age"))
    financial_aid = int(form_data.get("financial_aid"))

    gpa_shares = MPC_Functions.generate_shares(gpa, 3)
    age_shares = MPC_Functions.generate_shares(age, 3)
    financial_aid_shares = MPC_Functions.generate_shares(financial_aid, 3)

    db = firestore.client(app)

    # Used to see the current document row
    collection_ref = db.collection('party1')
    docs = collection_ref.get()
    num_docs = len(docs)

    party1_ref = db.collection("party1").document(f"document{num_docs}")
    party2_ref = db.collection("party2").document(f"document{num_docs}")
    party3_ref = db.collection("party3").document(f"document{num_docs}")

    parties = [party1_ref, party2_ref, party3_ref]
    shares = [gpa_shares, age_shares, financial_aid_shares]

    for index, party in enumerate(parties):
        party.set({"gpa": shares[0][index], "age": shares[1][index], "financial_aid": shares[2][index]})

    return flask.jsonify({"parties": 3, "data_points": len(form_data)})