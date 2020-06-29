import os
from google.cloud import storage
from termcolor import colored

PROJECT_ID = "wagon-project-catchafish"
BUCKET_NAME = "catchafish_gcp"
MODEL_NAME = "vgg16"

def storage_upload(bucket=BUCKET_NAME, rm=False):
    client = storage.Client()
    client = client.bucket(bucket)

    storage_location = 'models/{}/{}'.format(MODEL_NAME, 'model.h5')

    blob = client.blob(storage_location)
    blob.upload_from_filename('model.h5')

    print(colored("=> model.h5 uploaded to bucket {} inside {}".format(BUCKET_NAME, storage_location),
                  "green"))

    if rm:
        os.remove('model.h5')
