import csv
import os.path

from django.core.management import BaseCommand

from foodgram.settings import DATA_ROOT
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Loads data from csv files"

    def handle(self, *args, **options):
        file_path = os.path.join(DATA_ROOT, 'ingredients.csv')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
