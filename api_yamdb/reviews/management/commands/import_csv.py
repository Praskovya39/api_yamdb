from csv import DictReader
from django.core.management.base import BaseCommand
from api_yamdb.settings import CSV_DIR
from reviews.models import User, Title, Review, Genre, Comment, Category


class Command(BaseCommand):
    help = 'Команда для создания БД на основе имеющихся csv файлов'

    def import_user(self):
        if User.objects.exists():
            print('Модель User уже содержит данные, отменена загрузки')
        with open(CSV_DIR / 'users.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],)
            print('Данные модели User успешно загружены')

    def import_category(self):
        if Category.objects.exists():
            print('Модель Category уже содержит данные, отменена загрузки')
        with open(CSV_DIR / 'category.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],)
            print('Данные модели Category успешно загружены')

    def import_genre(self):
        if Genre.objects.exists():
            print('Модель Genre уже содержит данные, отменена загрузки')
        with open(CSV_DIR / 'genre.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],)
            print('Данные модели Genre успешно загружены')

    def import_title(self):
        if Title.objects.exists():
            print('Модель Title уже содержит данные, отменена загрузки')
        with open(CSV_DIR / 'titles.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'])
            print('Данные модели Title успешно загружены')

    def import_genre_title(self):
        with open(CSV_DIR / 'genre_title.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                id = row['id'],
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)
            print('Данные модели Genre_title успешно загружены')

    def import_review(self):
        if Review.objects.exists():
            print('Модель Review уже содержит данные, отменена загрузки')
        with open(CSV_DIR / 'review.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],)
            print('Данные модели Review успешно загружены')

    def import_comment(self):
        if Comment.objects.exists():
            print('Модель Comment уже содержит данные, отменена загрузки')
        with open(CSV_DIR / 'comments.csv', encoding='utf8') as csvfile:
            dict_reader = DictReader(csvfile)
            for row in dict_reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date'],)
            print('Данные модели Comment успешно загружены')

    def handle(self, *args, **options):
        print('Загрузка данных из csv в базу:')
        self.import_category()
        self.import_genre()
        self.import_user()
        self.import_title()
        self.import_review()
        self.import_comment()
        self.import_genre_title()