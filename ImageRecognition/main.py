from spineExtraction import extract_spine_imgs
from textExtraction import extract_text
from bookLookup import get_book_details
import json
import re
import os


#loop through all shelf_imgs and extract spine images.
for _,_,files in os.walk('shelf_imgs'): 
    for shelf_img in files:
        extract_spine_imgs('shelf_imgs/%s'%(shelf_img))

dat = dict()

#loop through all spine_imgs and extract text
for _,_,files in os.walk('spine_imgs'):
    for spine_img in files:

        book_spine_text = extract_text('spine_imgs/%s'%(spine_img))
        print(book_spine_text)
        print('-'*20,end='\n\n')
        book_details = get_book_details(book_spine_text)

        if book_details:
            dat[spine_img] = book_details
        else:
            print('No book details found for %s in %s'%(book_spine_text, spine_img))

with open('book_details.json', 'w') as f:
    json.dump(dat, f, indent=4)