# your_app/management/commands/import_library.py

import csv
from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Imports data from CSV file to the Book model.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 
                if row['datePublished'] == '':
                    datePublished=0
                else:
                    datePublished=int(row['datePublished'])

                bid=row['bid']
                name=row['name']
                author=row['author']
                about=row['about']
                
                bookEdition=row['bookEdition']
                bookFormat=row['bookFormat']
                img=row['img']
                
                Book.objects.create(
                    bid=bid,
                    title=name,
                    author=author,
                    about=about,
                    date_published=datePublished,
                    book_edition=bookEdition,
                    book_format=bookFormat,
                    img=img
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))