import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


load_dotenv()


USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                dbname=DBNAME
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("✅ Подключение к БД успешно!")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            raise

    def init_database(self):
        try:
            # Таблица пользователей
            self.cursor.execute("""
            CREATE TABLE IF EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                tg_id VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """)
            # Таблица подписок
            self.cursor.execute("""
            CREATE TABLE IF EXISTS subscriptions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name VARCHAR(50) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                period VARCHAR(50) NOT NULL CHECK (period IN ('day', 'week', 'month', 'year'))),
                category VARCHAR(50) NOT NULL CHECK (category IN ('entertainment', 'productivity','gaming', 'universal', 'health', 'other')),
                next_spend TIMESTAMP NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """)

            # Создание индексов
            self.cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id
                    ON subscriptions(user_id);
                """)

            self.cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_subscriptions_next_spend
                    ON subscriptions(next_spend);
                """)

            self.connection.commit()
            print("✅ Таблицы БД созданы успешно!")
        except Exception as e:
            print(f"❌ Ошибка при создании таблиц: {e}")
            raise

    def create_user(self, name, tg_id, password):
        try:
            self.cursor.execute("""
                INSERT INTO users (name, tg_id, password),
                VALUES (%s, %s, %s),
                RETURNING id, name, tg_id;
            """, (name, tg_id, password))

            user = self.cursor.fetchone()
            self.connection.commit()
            return user
        except psycopg2.IntegrityError:
            self.connection.rollback()
            print(f"⚠️ Пользователь с tg_id={tg_id} уже существует")
            return None
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при создании пользователя: {e}")
            return None

    def get_user_by_id(self, user_id):
        try:
            self.cursor.execute("""
                SELECT id, name, tg_id FROM users WHERE id = %s;
                    """, (user_id,))

            return self.cursor.fetchone()
        except Exception as e:
            print(f"❌ Ошибка при поиске пользователя: {e}")
            return None

    def add_subscription(self, user_id, name, price, period, category, next_spend=None):
        try:
            if not next_spend:
                now = datetime.now()
                if period == 'day':
                    next_spend = now + timedelta(days=1)
                elif period == 'week':
                    next_spend = now + timedelta(weeks=1)
                elif period == 'month':
                    next_spend = now + timedelta(days=30)
                elif period == 'year':
                    next_spend = now + timedelta(days=365)
                else:
                    next_spend = now + timedelta(days=30)

            self.cursor.execute("""
                INSERT INTO subscriptions (user_id, name, price, period, category, next_spend)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, name, price, period, category, next_spend;
            """, (user_id, name, price, period, category, next_spend))

            subscription = self.cursor.fetchone()
            self.connection.commit()
            return subscription
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при добавлении подписки: {e}")
            return None

    def get_user_subscriptions(self, user_id):
        try:
            self.cursor.execute("""
                SELECT id, name, price, period, category, next_spend
                FROM subscriptions
                WHERE user_id = %s
                ORDER BY next_spend ASC;
            """, (user_id,))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка при получении подписок: {e}")
            return None

    def update_subscription(self, subscription_id, **kwargs):

        try:
            allowed_fields = ['name', 'price', 'period', 'category', 'icon', 'next_spend']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

            if not updates:
                print("⚠️ Нет полей для обновления")
                return False

            # Строим SET часть запроса
            set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
            set_clause += ", updated_at = CURRENT_TIMESTAMP"

            query = f"""
                UPDATE subscriptions
                SET {set_clause}
                WHERE id = %s
                RETURNING id, name, price, period, category, next_spend;
            """

            values = list(updates.values()) + [subscription_id]
            self.cursor.execute(query, values)

            subscription = self.cursor.fetchone()
            self.connection.commit()
            return subscription
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при обновлении подписки: {e}")
            return None

    def delete_subscription(self, subscription_id):

        try:
            self.cursor.execute("""
                DELETE FROM subscriptions WHERE id = %s
                    RETURNING id;
            """, (subscription_id,))

            result = self.cursor.fetchone()
            self.connection.commit()
            return result is not None
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Ошибка при удалении подписки: {e}")
            return False

    def find_subscription_by_name(self, user_id, name):

        try:
            self.cursor.execute("""
                SELECT id, name, price, period, category, icon, next_spend
                FROM subscriptions
                WHERE user_id = %s AND LOWER(name) = LOWER(%s);
            """, (user_id, name))

            return self.cursor.fetchone()
        except Exception as e:
            print(f"❌ Ошибка при поиске подписки: {e}")
            return None

    def get_soon_spending(self, user_id, days=3):
        try:
            self.cursor.execute("""
                SELECT id, name, price, period, next_spend,
                       EXTRACT(DAY FROM (next_spend - CURRENT_TIMESTAMP)) as days_left
                FROM subscriptions
                WHERE user_id = %s
                  AND next_spend <= CURRENT_TIMESTAMP + INTERVAL '%s days'
                  AND next_spend > CURRENT_TIMESTAMP
                ORDER BY next_spend ASC;
            """, (user_id, days))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка при получении скорых трат: {e}")
            return None

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("✅ Соединение с БД закрыто")
        except Exception as e:
            print(f"❌ Ошибка при закрытии соединения: {e}")