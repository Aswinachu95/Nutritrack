import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Food
from pathlib import Path


class Command(BaseCommand):
    help = 'Load foods from data/food_demo.csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to CSV file', default=str(Path(settings.BASE_DIR) / 'data' / 'food_demo.csv'))

    def handle(self, *args, **options):
        path = options['path']
        created = 0
        updated = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                defaults = {
                    'category': row.get('category') or '',
                    'region': row.get('region') or '',
                    'is_vegetarian': str(row.get('is_vegetarian', '')).strip().lower() in ('true', '1', 'yes'),
                    'calories': float(row.get('calories') or 0),
                    'protein': float(row.get('protein') or 0),
                    'carbs': float(row.get('carbs') or 0),
                    'fat': float(row.get('fat') or 0),
                    'fiber': float(row.get('fiber') or 0),
                }
                obj, created_flag = Food.objects.update_or_create(name=row.get('name'), defaults=defaults)
                if created_flag:
                    created += 1
                else:
                    updated += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {created} new foods, updated {updated} existing.'))
