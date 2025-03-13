import csv
from django.core.management.base import BaseCommand
from cargo_delivery.models import Location

class Command(BaseCommand):
    help = "Загружает данные местоположений из CSV в базу данных"

    def handle(self, *args, **kwargs):
        file_path = "/home/test/PycharmProjects/gruz_perevozka/uszips.csv"

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            locations = []

            for row in reader:
                locations.append(
                    Location(
                        city=row["city"],
                        state=row["state_id"],
                        zip_code=row["zip"],
                        latitude=float(row["lat"]),
                        longitude=float(row["lng"]),  # исправлено 'Ing' -> 'lng'
                    )
                )

            # Добавляем данные в базу
            Location.objects.bulk_create(locations, ignore_conflicts=True, batch_size=1000)

            self.stdout.write(self.style.SUCCESS("✅ Locations loaded successfully"))
            for location in Location.objects.all()[:10]:
                    self.stdout.write(f'{location.city}, {location.state}, {location.zip_code}, {location.latitude}, {location.longitude}')




