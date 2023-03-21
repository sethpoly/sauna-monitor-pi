import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("rhodes_sauna_service_account.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

SENSOR_COLLECTION_ID = "sensors"
TEMPERATURE_DOC_ID = "temperature"

def set_current_temp(temp, timestamp):
    doc_ref = db.collection(f'{SENSOR_COLLECTION_ID}').document(f'{TEMPERATURE_DOC_ID}')
    doc_ref.set({
        u'current_temp': temp,
        u'last_timestamp': timestamp
    })

def update_logs(temp, timestamp):
    return
    doc_ref = db.collection(f'{SENSOR_COLLECTION_ID}').document(f'{TEMPERATURE_DOC_ID}')
    data = {
        str(timestamp): temp
    }
    doc_ref.update({
        f'past_logs.{timestamp}': temp
    })
