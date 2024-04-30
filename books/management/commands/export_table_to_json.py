# export_table_to_json.py

import json
from django.core.management.base import BaseCommand
from ...models import Book  # Replace with the actual model
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

class Command(BaseCommand):
    help = 'Export data from a table to a JSON file'

    def handle(self, *args, **options):
        # Retrieve data from the table
        queryset = Book.objects.all()  # Replace with the actual model
        data = list(queryset.values())

        # Specify the output file path
        output_file_path = 'books.json'

        # Write data to JSON file
        with open(output_file_path, 'w') as json_file:
            json.dump(data, json_file, cls=UUIDEncoder, default=str, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {output_file_path}'))
