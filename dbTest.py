import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection('user').document('2')
doc = doc_ref.get()

data = doc.to_dict()
print("Email:", data.get("email"))
print("Name:", data.get("name"))
print("Gender:", data.get("gender"))
