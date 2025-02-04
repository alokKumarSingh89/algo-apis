import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Use a service account.
cred = credentials.Certificate(os.path.dirname(__file__)+'/db.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()



def add_collection(collection, document, data):
  
  doc_ref = db.collection(collection).document(document)
  if doc_ref.get().exists:
    doc_ref.update(data)
  else:
    doc_ref.set(data)


def add_nse_code(collection, document, code):
  doc_ref = db.collection(collection).document(document)
  if doc_ref.get().exists:
    doc_ref.update({code:code})
  else:
    doc_ref.set({code:code})
  
def load_code(collection, document):
  doc_ref = db.collection(collection).document(document)
  doc = doc_ref.get()
  if doc.exists:
    return doc.to_dict()
  else:
    return None
  
def get_scripts():
  doc_ref = db.collection("scripts").document("nse")
  doc = doc_ref.get()
  if doc.exists:
    return doc.to_dict()
  return None
  
