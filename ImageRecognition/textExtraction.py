import os, io
from google.cloud import vision
import spacy
import re

def extract_text(filepath):
    ''' 
    Extract the text from the cover of a book spine using Google Cloud Vision API.
    
    Parameters
    ----------
        filepath : str
        The path to the image file.
    
    Returns
    -------
        str or None
        The extracted text from the image. None if there is nothing.
     '''

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'serviceacctoken.json'

    client = vision.ImageAnnotatorClient()

    file_name = os.path.abspath(filepath)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts != []:
            # Ensure the text is suitable to be used with the Google Books API
            # More handling must be done to ensure the text is suitable for the Google Books API
            processed_text = texts[0].description.replace
    else: processed_text = ""

    if not len(texts) == 0:
        return processed_text   
    else:
        return None