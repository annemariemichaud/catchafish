import os
from google.cloud import storage
from termcolor import colored

from tensorflow.keras.models import load_model

PROJECT_ID = "wagon-project-catchafish"
BUCKET_NAME = "catchafish_gcp"
MODEL_NAME = "vgg16"

def get_credentials():
    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    if '.json' in credentials_raw:
        credentials_raw = open(credentials_raw).read()

    creds_json = json.loads(credentials_raw)
    creds_gcp = service_account.Credentials.from_service_account_info(creds_json)

    return creds_gcp

def model_upload(bucket=BUCKET_NAME, rm=False):
    client = storage.Client()
    client = client.bucket(bucket)

    storage_location = 'models/{}/{}'.format(MODEL_NAME, 'model.h5')

    blob = client.blob(storage_location)
    blob.upload_from_filename('model.h5')

    print(colored("=> model.h5 uploaded to bucket {} inside {}".format(BUCKET_NAME, storage_location),
                  "green"))

    if rm:
        os.remove('model.h5')

def download_model(model = 'vgg16', bucket = BUCKET_NAME, rm = True):
    creds = get_credentials()
    client = storage.Client(credentials=creds, project=PROJECT_ID).bucket(bucket)

    storage_location = 'models/{}/{}'.format(model, 'model.h5')

    blob = client.blob(storage_location)
    blob.download_to_filename('model.h5')
    print(f"=> model downloaded from storage")

    model = load_model('model.h5')

    if rm:
        os.remove('model.h5')

    return model
