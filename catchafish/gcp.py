import os
import json

from google.cloud import storage
from google.oauth2 import service_account
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

    #storage_location = 'models/{}/{}'.format(MODEL_NAME, 'model')

    #blob = client.blob(storage_location)

    os.system('gsutil -m cp -R /tmp/saved_model/my_model gs://catchafish_gcp/models')

    print(colored("=> model uploaded to bucket {} inside gs://catchafish_gcp/models".format(BUCKET_NAME),
                  "green"))

    if rm:
        os.rmtree('model')

def download_model(model = 'vgg16', bucket = BUCKET_NAME, rm = True):
    creds = get_credentials()
    client = storage.Client(credentials=creds, project=PROJECT_ID).bucket(bucket)

    storage_location = 'models/{}/{}'.format(model, 'model.h5')

    blob = client.blob(storage_location)
    blob.download_to_filename('model.h5')
    print(f"=> model.h5 downloaded from storage")

    model = load_model('model.h5')

    if rm:
        os.remove('model.h5')

    return model

#def image_upload(image_path, species_folder, bucket=BUCKET_NAME, rm = True):
#    creds = get_credentials()
#    client = storage.Client(credentials = creds, project = PROJECT_ID)
#    client = client.bucket(bucket)
#
#    storage_location = 'data/{}'.format(species_folder)
#
#    blob = client.blob(storage_location)
#    blob.upload_from_filename(image_path)
#
#    if rm:
#        os.remove(image_path)

if __name__ == "__main__":
    model = download_model()
    if model is not None:
        print('Yo')
