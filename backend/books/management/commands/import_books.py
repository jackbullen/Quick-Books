# your_app/management/commands/import_library.py

import json
from django.core.management.base import BaseCommand
from books.models import Book
from django.utils import timezone
import uuid
class Command(BaseCommand):
    help = 'Imports data from CSV file to the Book model.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file to import.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        with open(json_file_path, 'r') as f:
            data = json.load(f)


        for book in data:
            # print(book)
            book = data[book]
            
            Book.objects.create(
                bid = uuid.uuid4(),
                title = book['title'],
                author = book['author'],
                about = book['description'],
                genre = book['genre'],
                page_count = book['page_ct'],
                publisher = book['pub'],
                date_published = book['pub_date'],
                created_at = timezone.now(),
                # edition = book['edition'],
                # typ = book['type'],
                language = book['lang'],
                link = book['link'],
                # img = book['imageLinks']['thumbnail'],
                info_link = book['info_link'],
                isbn = book['extra_info']['industryIdentifiers'][-1]['type']+book['extra_info']['industryIdentifiers'][-1]['identifier'],
            )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully.'))