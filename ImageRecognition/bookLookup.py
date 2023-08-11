from textExtraction import extract_text
import requests
from dotenv import load_dotenv
import os

def get_book_details(text):
    ''' Get the book details from Google Books API. '''

    load_dotenv()
    api_key = os.environ.get('GOOGLE_BOOKS_API_KEY')
    if not api_key:
        raise ValueError("Google Books API key not set in environment variables or .env file.")

    base_url = 'https://www.googleapis.com/books/v1/volumes'

    print(text)
    print('-'*20,end='\n\n')

    # CHANGE PARAMS
    params = {'q': f'{text}', 'key': api_key}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'items' in data:
            book_info = data['items'][0]['volumeInfo']
            book_title = book_info.get('title', '')
            book_author = ', '.join(book_info.get('authors', []))            
            book_description = book_info.get('description', '')
            book_genre = ', '.join(book_info.get('categories', []))
            book_pageCt = book_info.get('pageCount', '')
            book_img = book_info.get('imageLinks', {}).get('thumbnail', '')
            book_isbn = book_info.get('industryIdentifiers', [])[0].get('identifier', '')
            book_lang = book_info.get('language', '')
            book_pubDate = book_info.get('publishedDate', '')
            book_pub = book_info.get('publisher', '')
            book_link = book_info.get('previewLink', '')
            book_infoLink = book_info.get('infoLink', '')
            book_saleInfo = book_info.get('saleInfo', {}).get('retailPrice', '')
            return {
                'title': book_title,
                'author': book_author,
                'description': book_description,
                'genre': book_genre,
                'page_ct': book_pageCt,
                'img': book_img,
                'isbn': book_isbn,
                'lang': book_lang,
                'pub_date': book_pubDate,
                'pub': book_pub,
                'link': book_link,
                'info_link': book_infoLink,
                'sale_info': book_saleInfo,
                'extra_info': book_info
            }
        else:
            return None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

