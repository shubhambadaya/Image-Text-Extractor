import base64
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jupyter/image-classification-mlops-e48685e1fcab.json"

from google.cloud import vision_v1

# [START functions_ocr_process]
def process_image(file, context):
    """Cloud Function triggered by Cloud Storage when a file is changed.
    Args:
        file (dict): Metadata of the changed file, provided by the triggering
                                 Cloud Storage event.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to stdout and Stackdriver Logging
    """
    bucket = validate_message(file, "bucket")
    name = validate_message(file, "name")

    detect_text(bucket, name)

    print("File {} processed.".format(file["name"]))


def sample_batch_annotate_files(bucket,filename):

    text = ""
    """Perform batch file annotation."""
    mime_type = "application/pdf"

    client = vision_v1.ImageAnnotatorClient()

    gcs_source = {"uri": f"gs://{bucket}/{filename}"}
    input_config = {"gcs_source": gcs_source, "mime_type": mime_type}
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    # The service can process up to 5 pages per document file.
    # Here we specify the first, second, and last page of the document to be
    # processed.
    pages = [1, 2, -1]
    requests = [{"input_config": input_config, "features": features, "pages": pages}]

    response = client.batch_annotate_files(requests=requests)
    for image_response in response.responses[0].responses:
        print('=========================================')
        print(u"Full text: {}".format(image_response.full_text_annotation.text))

        #text += image_response.full_text_annotation.text

    #return(text)
