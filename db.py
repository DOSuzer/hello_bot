import os
import psycopg2

from dotenv import load_dotenv, find_dotenv
from psycopg2.extras import DictCursor


if not find_dotenv():
    print('Переменные окружения не загружены т.к отсутствует файл .env')
    exit()
else:
    load_dotenv()


class Database:
    def __init__(self):
        """Инициализация экземпляра класса."""
        self.connection = psycopg2.connect(
            database='tg_bot', port='5432', user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'), host='localhost')
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def add_user(self, user):
        """Создание пользователя в БД."""
        with self.connection:
            self.cursor.execute(
                '''INSERT INTO users (name, family_name, sex, photo, user_id)
                   VALUES(%s, %s, %s, %s, %s);''', (
                    user.name, user.family_name,
                    user.sex, user.photo, user.user_id
                )
            )
            self.connection.commit()
            return 'done'

    def get_users(self):
        """Получение пользователей из БД."""
        with self.connection:
            self.cursor.execute('SELECT * FROM users')
            return self.cursor.fetchall()

    def create_db(self):
        """Создание БД."""
        with self.connection:
            self.cursor.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR ( 50 ) NOT NULL,
                    family_name VARCHAR ( 50 ) NOT NULL,
                    sex VARCHAR ( 50 ) NOT NULL,
                    photo VARCHAR ( 255 ),
                    user_id BIGINT UNIQUE NOT NULL);'''
            )
            self.connection.commit()
            return 'done'

    def user_exists(self, user_id):
        """Проверка на существовние пользователя."""
        with self.connection:
            self.cursor.execute(
                'SELECT * FROM users WHERE user_id = %s', (user_id,)
            )
            result = self.cursor.fetchall()
            return bool(len(result))
