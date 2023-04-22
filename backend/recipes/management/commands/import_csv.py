import csv
import os.path

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = "Loads data from csv files"

    def handle(self, *args, **options):
        print('Trying to load ingredients data')
        file_path = os.path.join(settings.DATA_ROOT, 'ingredients.csv')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for name, unit in reader:
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=unit
                )
            print('Ingredients data successfully uploaded')
        print('Trying to load tags data')
        file_path = os.path.join(settings.DATA_ROOT, 'tags.csv')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for tag, color, slug in reader:
                Tag.objects.get_or_create(
                    name=tag, color=color,
                    slug=slug
                )
            print('Tags data successfully uploaded')
