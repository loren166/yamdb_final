import csv

from django.core.management import BaseCommand
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User

TABLES = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comments: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                f'static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)

        """создаем M2M связь."""
        with open(
                'static/data/genre_title.csv', 'r', encoding='utf-8'
        ) as file:
            title_genres = csv.DictReader(file, delimiter=',')

        for title_genre in title_genres:
            genre_id = title_genre['genre_id']
            title_id = Title(title_genre['title_id'])
            title_id.genre.add(genre_id)

        self.stdout.write(self.style.SUCCESS('Загрузка данных завершена'))
