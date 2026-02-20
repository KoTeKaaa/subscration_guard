from datetime import datetime, timedelta

# Функция для расчета стоимости подписки за 5 лет
def cost_for_5_years(price, period):
    return cost_for_year(price, period) * 5


# Функция для расчета стоимости подписки за 1 месяц
def cost_for_month(price, period):
    if period == "month":
        return price
    elif period == "week":
        return int(price * 4.3)
    elif period == "day":
        return price * 30
    elif period == "year":
        return int(price / 12)
    else:
        return None

# Функция для расчета стоимости подписки за 1 год
def cost_for_year(price, period):
    if period == "year":
        return price
    elif period == "month":
        return price * 12
    elif period == "week":
        return price * 52
    elif period == "day":
        return price * 365
    else:
        return None


# Основной класс пользователя
class UserProfile:
    # Инициализация профиля с именем, электронной почтой и паролем
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.subscriptions = []

    # Добавление подписки в профиль
    def add_subscription(self, subscription):
        self.subscriptions.append(subscription)
    # Удаление подписки из профиля
    def remove_subscription(self, subscription):
        self.subscriptions.remove(subscription)

    # Общая стоимость всех подписок за 5 лет, за 1 месяц и за 1 год
    def summary_for_5_years(self):
        total_cost = 0
        for subscription in self.subscriptions:
            total_cost += cost_for_5_years(subscription['price'], subscription['period'])
        return total_cost
    def summary_for_month(self):
        total_cost = 0
        for subscription in self.subscriptions:
            total_cost += cost_for_month(subscription['price'], subscription['period'])
        return total_cost
    def summary_for_year(self):
        total_cost = 0
        for subscription in self.subscriptions:
            total_cost += cost_for_year(subscription['price'], subscription['period'])
        return total_cost

    # Вывод всех подписок пользователя
    def all_subscriptions(self):
        return self.subscriptions

    # Распределение подписок по категориям и тратам за месяц
    def get_spending_by_category_month(self):
        spending = {"entertainment": 0, "productivity": 0, "gaming": 0, "universal": 0, "health": 0, "other": 0}
        for subscription in self.subscriptions:
            if subscription['category'] == 'entertainment':
                spending['entertainment'] += cost_for_month(subscription['price'], subscription["period"])
            elif subscription['category'] == 'productivity':
                spending['productivity'] += cost_for_month(subscription['price'], subscription["period"])
            elif subscription['category'] == 'gaming':
                spending['gaming'] += cost_for_month(subscription['price'], subscription["period"])
            elif subscription['category'] == 'universal':
                spending['universal'] += cost_for_month(subscription['price'], subscription["period"])
            elif subscription['category'] == 'health':
                spending['health'] += cost_for_month(subscription['price'], subscription["period"])
            else:
                spending['other'] += cost_for_month(subscription['price'], subscription["period"])
        return spending

    # Функция для нахождения подписки по имени
    def find_subscription(self, name):
        for subscription in self.subscriptions:
            if subscription['name'].lower() == name.lower():
                return subscription
        return None

    # Обновление имени подписки
    def update_name_subscription(self, old_name, new_name):
        subscription = self.find_subscription(old_name)
        if subscription:
            subscription['name'] = new_name
            return True
        return False

    # Обновление цены за подписку
    def update_price_subscription(self, name, new_price):
        subscription = self.find_subscription(name)
        if subscription:
            subscription['price'] = new_price
            return True
        return False

    # Функция для получения подписок, у которых ближайшая трата будет в течение 3 дней
    def get_subscriptions_for_soon_spend(self):
        soon_spend = []
        for subscription in self.subscriptions:
            days_left = (subscription['next_spend'] - datetime.now()).days
            if 0 <= days_left <= 3:
                soon_spend.append({
                    'name' : subscription['name'],
                    'price' : subscription['price'],
                    'days_left' : days_left
                })
        if soon_spend:
            return soon_spend
        return None



# Основной класс подписки
class Subscription:
    # Инициализация подписки с именем, ценой, периодом оплаты и категорией
    def __init__(self, name, price, period, category):
        self.name = name
        self.price = price
        self.period = period
        self.category = category
        if period == "week":
            next_spend = datetime.now() + timedelta(weeks=1)
        elif period == "day":
            next_spend = datetime.now() + timedelta(days=1)
        elif period == "month":
            next_spend = datetime.now() + timedelta(days=30)
        elif period == "year":
            next_spend = datetime.now() + timedelta(days=365)
        else:
            next_spend = datetime.now() + timedelta(days=30)
        self.next_spend = next_spend

    # Получение подписки в виде словаря
    def get_subscription(self):
        return {'name': self.name, 'price': self.price, 'period': self.period, 'category': self.category, 'next_spend': self.next_spend}

    def __str__(self):
        return f"Subscription (name={self.name}, price={self.price}, period={self.period}, category={self.category})"

    # Обновление даты следующей оплаты
    def update_date_spend(self):
        if self.period == "year":
            self.next_spend = self.next_spend + timedelta(days=365)
        elif self.period == "month":
            self.next_spend = self.next_spend + timedelta(days=30)
        elif self.period == "week":
            self.next_spend = self.next_spend + timedelta(days=7)
        elif self.period == "day":
            self.next_spend = self.next_spend + timedelta(days=1)
        else:
            self.next_spend = self.next_spend + timedelta(days=30)

def main():
    pass

if __name__ == "__main__":
    main()