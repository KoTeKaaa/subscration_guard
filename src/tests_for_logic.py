import unittest
from datetime import datetime, timedelta
from logic import (
    cost_for_month,
    cost_for_year,
    cost_for_5_years,
    UserProfile,
    Subscription
)


class TestCostCalculations(unittest.TestCase):
    """Тесты для функций расчета стоимости"""

    # Тесты для cost_for_month
    def test_cost_for_month_monthly_period(self):
        """Подписка с периодом 'месяц' должна вернуть саму цену"""
        self.assertEqual(cost_for_month(500, "month"), 500)

    def test_cost_for_month_weekly_period(self):
        """Подписка с периодом 'неделя' должна вернуть цену * 4.3"""
        self.assertEqual(cost_for_month(100, "week"), int(100 * 4.3))
        self.assertEqual(cost_for_month(100, "week"), 430)

    def test_cost_for_month_daily_period(self):
        """Подписка с периодом 'день' должна вернуть цену * 30"""
        self.assertEqual(cost_for_month(30, "day"), 900)

    def test_cost_for_month_yearly_period(self):
        """Подписка с периодом 'год' должна вернуть цену / 12"""
        self.assertEqual(cost_for_month(1200, "year"), 100)
        self.assertEqual(cost_for_month(1000, "year"), 83)  # int(1000/12) = 83

    def test_cost_for_month_invalid_period(self):
        """Неверный период должен вернуть None"""
        self.assertIsNone(cost_for_month(500, "invalid"))

    # Тесты для cost_for_year
    def test_cost_for_year_monthly_period(self):
        """Подписка с периодом 'месяц' должна вернуть цену * 12"""
        self.assertEqual(cost_for_year(500, "month"), 6000)

    def test_cost_for_year_weekly_period(self):
        """Подписка с периодом 'неделя' должна вернуть цену * 52"""
        self.assertEqual(cost_for_year(100, "week"), 5200)

    def test_cost_for_year_daily_period(self):
        """Подписка с периодом 'день' должна вернуть цену * 365"""
        self.assertEqual(cost_for_year(30, "day"), 10950)

    def test_cost_for_year_yearly_period(self):
        """Подписка с периодом 'год' должна вернуть саму цену"""
        self.assertEqual(cost_for_year(1000, "year"), 1000)

    def test_cost_for_year_invalid_period(self):
        """Неверный период должен вернуть None"""
        self.assertIsNone(cost_for_year(500, "invalid"))

    # Тесты для cost_for_5_years
    def test_cost_for_5_years_monthly_period(self):
        """Подписка с периодом 'месяц' должна вернуть цену * 12 * 5"""
        self.assertEqual(cost_for_5_years(500, "month"), 500 * 12 * 5)
        self.assertEqual(cost_for_5_years(500, "month"), 30000)

    def test_cost_for_5_years_yearly_period(self):
        """Подписка с периодом 'год' должна вернуть цену * 5"""
        self.assertEqual(cost_for_5_years(1000, "year"), 5000)

    def test_cost_for_5_years_weekly_period(self):
        """Подписка с периодом 'неделя' должна вернуть цену * 52 * 5"""
        self.assertEqual(cost_for_5_years(100, "week"), 100 * 52 * 5)
        self.assertEqual(cost_for_5_years(100, "week"), 26000)


class TestSubscription(unittest.TestCase):
    """Тесты для класса Subscription"""

    def setUp(self):
        """Создание подписки для каждого теста"""
        self.sub = Subscription("Spotify", 500, "month", "entertainment")

    def test_subscription_initialization(self):
        """Проверка инициализации подписки"""
        self.assertEqual(self.sub.name, "Spotify")
        self.assertEqual(self.sub.price, 500)
        self.assertEqual(self.sub.period, "month")
        self.assertEqual(self.sub.category, "entertainment")

    def test_subscription_next_spend_monthly(self):
        """Проверка расчета next_spend для месячной подписки"""
        expected_date = datetime.now() + timedelta(days=30)
        # Проверяем дату с точностью до дня
        self.assertEqual(self.sub.next_spend.date(), expected_date.date())

    def test_subscription_next_spend_weekly(self):
        """Проверка расчета next_spend для недельной подписки"""
        sub_weekly = Subscription("Test", 100, "week", "entertainment")
        expected_date = datetime.now() + timedelta(weeks=1)
        self.assertEqual(sub_weekly.next_spend.date(), expected_date.date())

    def test_subscription_next_spend_daily(self):
        """Проверка расчета next_spend для дневной подписки"""
        sub_daily = Subscription("Test", 50, "day", "entertainment")
        expected_date = datetime.now() + timedelta(days=1)
        self.assertEqual(sub_daily.next_spend.date(), expected_date.date())

    def test_subscription_next_spend_yearly(self):
        """Проверка расчета next_spend для годовой подписки"""
        sub_yearly = Subscription("Test", 1000, "year", "gaming")
        expected_date = datetime.now() + timedelta(days=365)
        self.assertEqual(sub_yearly.next_spend.date(), expected_date.date())

    def test_subscription_get_subscription(self):
        """Проверка метода get_subscription"""
        sub_dict = self.sub.get_subscription()
        self.assertEqual(sub_dict['name'], "Spotify")
        self.assertEqual(sub_dict['price'], 500)
        self.assertEqual(sub_dict['period'], "month")
        self.assertEqual(sub_dict['category'], "entertainment")
        self.assertIn('next_spend', sub_dict)

    def test_subscription_str(self):
        """Проверка строкового представления подписки"""
        str_repr = str(self.sub)
        self.assertIn("Spotify", str_repr)
        self.assertIn("500", str_repr)
        self.assertIn("month", str_repr)
        self.assertIn("entertainment", str_repr)

    def test_subscription_update_date_spend_monthly(self):
        """Проверка обновления даты платежа для месячной подписки"""
        old_date = self.sub.next_spend
        self.sub.update_date_spend()
        new_date = self.sub.next_spend
        self.assertEqual((new_date - old_date).days, 30)

    def test_subscription_update_date_spend_weekly(self):
        """Проверка обновления даты платежа для недельной подписки"""
        sub_weekly = Subscription("Test", 100, "week", "entertainment")
        old_date = sub_weekly.next_spend
        sub_weekly.update_date_spend()
        new_date = sub_weekly.next_spend
        self.assertEqual((new_date - old_date).days, 7)

    def test_subscription_update_date_spend_daily(self):
        """Проверка обновления даты платежа для дневной подписки"""
        sub_daily = Subscription("Test", 50, "day", "entertainment")
        old_date = sub_daily.next_spend
        sub_daily.update_date_spend()
        new_date = sub_daily.next_spend
        self.assertEqual((new_date - old_date).days, 1)

    def test_subscription_update_date_spend_yearly(self):
        """Проверка обновления даты платежа для годовой подписки"""
        sub_yearly = Subscription("Test", 1000, "year", "gaming")
        old_date = sub_yearly.next_spend
        sub_yearly.update_date_spend()
        new_date = sub_yearly.next_spend
        self.assertEqual((new_date - old_date).days, 365)


class TestUserProfile(unittest.TestCase):
    """Тесты для класса UserProfile"""

    def setUp(self):
        """Создание профиля пользователя для каждого теста"""
        self.user = UserProfile("vadim", "vadim.08@mail.ru", "1234")
        self.sub1 = Subscription("Spotify", 500, "month", "entertainment")
        self.sub2 = Subscription("Netflix", 1000, "month", "entertainment")
        self.sub3 = Subscription("Yandex", 100, "week", "universal")

    def test_user_profile_initialization(self):
        """Проверка инициализации профиля"""
        self.assertEqual(self.user.name, "vadim")
        self.assertEqual(self.user.email, "vadim.08@mail.ru")
        self.assertEqual(self.user.password, "1234")
        self.assertEqual(len(self.user.subscriptions), 0)

    def test_add_subscription(self):
        """Проверка добавления подписки"""
        self.user.add_subscription(self.sub1.get_subscription())
        self.assertEqual(len(self.user.subscriptions), 1)
        self.assertEqual(self.user.subscriptions[0]['name'], "Spotify")

    def test_add_multiple_subscriptions(self):
        """Проверка добавления нескольких подписок"""
        self.user.add_subscription(self.sub1.get_subscription())
        self.user.add_subscription(self.sub2.get_subscription())
        self.user.add_subscription(self.sub3.get_subscription())
        self.assertEqual(len(self.user.subscriptions), 3)

    def test_remove_subscription(self):
        """Проверка удаления подписки"""
        self.user.add_subscription(self.sub1.get_subscription())
        self.user.add_subscription(self.sub2.get_subscription())
        self.assertEqual(len(self.user.subscriptions), 2)

        self.user.remove_subscription(self.user.subscriptions[0])
        self.assertEqual(len(self.user.subscriptions), 1)
        self.assertEqual(self.user.subscriptions[0]['name'], "Netflix")

    def test_all_subscriptions(self):
        """Проверка получения всех подписок"""
        self.user.add_subscription(self.sub1.get_subscription())
        self.user.add_subscription(self.sub2.get_subscription())

        all_subs = self.user.all_subscriptions()
        self.assertEqual(len(all_subs), 2)
        self.assertEqual(all_subs[0]['name'], "Spotify")
        self.assertEqual(all_subs[1]['name'], "Netflix")

    def test_summary_for_month(self):
        """Проверка расчета затрат за месяц"""
        self.user.add_subscription(self.sub1.get_subscription())  # 500
        self.user.add_subscription(self.sub2.get_subscription())  # 1000
        self.user.add_subscription(self.sub3.get_subscription())  # 100 * 4.3 = 430

        total = self.user.summary_for_month()
        expected = 500 + 1000 + 430
        self.assertEqual(total, expected)

    def test_summary_for_year(self):
        """Проверка расчета затрат за год"""
        self.user.add_subscription(self.sub1.get_subscription())  # 500 * 12 = 6000
        self.user.add_subscription(self.sub2.get_subscription())  # 1000 * 12 = 12000

        total = self.user.summary_for_year()
        expected = 6000 + 12000
        self.assertEqual(total, expected)

    def test_summary_for_5_years(self):
        """Проверка расчета затрат за 5 лет"""
        self.user.add_subscription(self.sub1.get_subscription())  # 500 * 12 * 5 = 30000
        self.user.add_subscription(self.sub2.get_subscription())  # 1000 * 12 * 5 = 60000

        total = self.user.summary_for_5_years()
        expected = 30000 + 60000
        self.assertEqual(total, expected)

    def test_get_spending_by_category_month(self):
        """Проверка распределения затрат по категориям"""
        self.user.add_subscription(self.sub1.get_subscription())  # entertainment: 500
        self.user.add_subscription(self.sub2.get_subscription())  # entertainment: 1000
        self.user.add_subscription(self.sub3.get_subscription())  # universal: 430

        spending = self.user.get_spending_by_category_month()
        self.assertEqual(spending['entertainment'], 1500)
        self.assertEqual(spending['universal'], 430)
        self.assertEqual(spending['productivity'], 0)
        self.assertEqual(spending['gaming'], 0)
        self.assertEqual(spending['health'], 0)

    def test_find_subscription_found(self):
        """Проверка поиска существующей подписки"""
        self.user.add_subscription(self.sub1.get_subscription())
        self.user.add_subscription(self.sub2.get_subscription())

        found = self.user.find_subscription("Spotify")
        self.assertIsNotNone(found)
        self.assertEqual(found['name'], "Spotify")
        self.assertEqual(found['price'], 500)

    def test_find_subscription_case_insensitive(self):
        """Проверка поиска без учета регистра"""
        self.user.add_subscription(self.sub1.get_subscription())

        found = self.user.find_subscription("spotify")
        self.assertIsNotNone(found)
        self.assertEqual(found['name'], "Spotify")

    def test_find_subscription_not_found(self):
        """Проверка поиска несуществующей подписки"""
        self.user.add_subscription(self.sub1.get_subscription())

        found = self.user.find_subscription("Disney")
        self.assertIsNone(found)

    def test_update_name_subscription_success(self):
        """Проверка успешного обновления имени подписки"""
        self.user.add_subscription(self.sub1.get_subscription())

        result = self.user.update_name_subscription("Spotify", "Spotify Premium")
        self.assertTrue(result)
        self.assertEqual(self.user.subscriptions[0]['name'], "Spotify Premium")

    def test_update_name_subscription_failure(self):
        """Проверка неудачного обновления имени подписки"""
        self.user.add_subscription(self.sub1.get_subscription())

        result = self.user.update_name_subscription("Disney", "Disney Plus")
        self.assertFalse(result)

    def test_update_price_subscription_success(self):
        """Проверка успешного обновления цены подписки"""
        self.user.add_subscription(self.sub1.get_subscription())

        result = self.user.update_price_subscription("Spotify", 600)
        self.assertTrue(result)
        self.assertEqual(self.user.subscriptions[0]['price'], 600)

    def test_update_price_subscription_failure(self):
        """Проверка неудачного обновления цены подписки"""
        self.user.add_subscription(self.sub1.get_subscription())

        result = self.user.update_price_subscription("Disney", 500)
        self.assertFalse(result)

    def test_get_subscriptions_for_soon_spend_with_soon_subscription(self):
        """Проверка получения подписок с платежом через 2 дня"""
        # Создаем подписку с платежом через 2 дня
        sub = Subscription("Test", 500, "month", "entertainment")
        sub.next_spend = datetime.now() + timedelta(days=2)

        self.user.add_subscription(sub.get_subscription())

        soon = self.user.get_subscriptions_for_soon_spend()
        self.assertIsNotNone(soon)
        self.assertEqual(len(soon), 1)
        self.assertEqual(soon[0]['name'], "Test")
        self.assertEqual(soon[0]['days_left'], 2)

    def test_get_subscriptions_for_soon_spend_empty(self):
        """Проверка получения подписок когда их нет в ближайшие 3 дня"""
        # Создаем подписку с платежом через 30 дней
        sub = Subscription("Test", 500, "month", "entertainment")
        sub.next_spend = datetime.now() + timedelta(days=30)

        self.user.add_subscription(sub.get_subscription())

        soon = self.user.get_subscriptions_for_soon_spend()
        self.assertIsNone(soon)

    def test_get_subscriptions_for_soon_spend_multiple(self):
        """Проверка получения нескольких подписок с платежом в ближайшие 3 дня"""
        sub1 = Subscription("Test1", 500, "month", "entertainment")
        sub1.next_spend = datetime.now() + timedelta(days=1)

        sub2 = Subscription("Test2", 100, "week", "universal")
        sub2.next_spend = datetime.now() + timedelta(days=3)

        sub3 = Subscription("Test3", 1000, "year", "gaming")
        sub3.next_spend = datetime.now() + timedelta(days=10)

        self.user.add_subscription(sub1.get_subscription())
        self.user.add_subscription(sub2.get_subscription())
        self.user.add_subscription(sub3.get_subscription())

        soon = self.user.get_subscriptions_for_soon_spend()
        self.assertIsNotNone(soon)
        self.assertEqual(len(soon), 2)
        self.assertEqual(soon[0]['name'], "Test1")
        self.assertEqual(soon[1]['name'], "Test2")


class TestMainFunctionScenarios(unittest.TestCase):
    """Тесты для сценариев функции main"""

    def test_main_scenario_full_workflow(self):
        """Проверка полного сценария добавления и удаления подписок"""
        user = UserProfile("vadim", "vadim.08@mail.ru", "1234")

        # Добавляем подписки
        subs1 = Subscription("Spotify", 500, "month", "entertainment")
        subs2 = Subscription("Yandex", 100, "week", "universal")
        subs3 = Subscription("Netflix", 1000, "month", "entertainment")
        subs4 = Subscription("Google", 500, "month", "productivity")
        subs5 = Subscription("Steam", 1000, "year", "gaming")
        subs6 = Subscription("Heal", 200, "month", "health")

        user.add_subscription(subs1.get_subscription())
        user.add_subscription(subs2.get_subscription())
        user.add_subscription(subs3.get_subscription())
        user.add_subscription(subs4.get_subscription())
        user.add_subscription(subs5.get_subscription())
        user.add_subscription(subs6.get_subscription())

        # Проверяем количество подписок
        self.assertEqual(len(user.all_subscriptions()), 6)

        # Проверяем расчеты
        monthly = user.summary_for_month()
        yearly = user.summary_for_year()
        five_years = user.summary_for_5_years()

        # Ожидаемые значения:
        # Spotify: 500
        # Yandex: 100 * 4.3 = 430
        # Netflix: 1000
        # Google: 500
        # Steam: 1000/12 = 83
        # Heal: 200
        # Total for month: 500 + 430 + 1000 + 500 + 83 + 200 = 2713

        self.assertEqual(monthly, 2713)
        self.assertEqual(yearly, monthly * 12)
        self.assertEqual(five_years, yearly * 5)

        # Проверяем распределение по категориям
        spending = user.get_spending_by_category_month()
        self.assertEqual(spending['entertainment'], 1500)  # Spotify + Netflix
        self.assertEqual(spending['universal'], 430)       # Yandex
        self.assertEqual(spending['productivity'], 500)    # Google
        self.assertEqual(spending['gaming'], 83)           # Steam
        self.assertEqual(spending['health'], 200)          # Heal

        # Удаляем подписку
        user.remove_subscription(subs2.get_subscription())
        self.assertEqual(len(user.all_subscriptions()), 5)

        # Проверяем новые расчеты
        new_monthly = user.summary_for_month()
        expected_new_monthly = monthly - 430  # Удалили Yandex
        self.assertEqual(new_monthly, expected_new_monthly)

    def test_main_scenario_with_updates(self):
        """Проверка сценария с обновлением подписок"""
        user = UserProfile("vadim", "vadim.08@mail.ru", "1234")

        sub = Subscription("Spotify", 500, "month", "entertainment")
        user.add_subscription(sub.get_subscription())

        # Проверяем исходную цену
        self.assertEqual(user.summary_for_month(), 500)

        # Обновляем цену
        user.update_price_subscription("Spotify", 600)
        self.assertEqual(user.summary_for_month(), 600)

        # Обновляем имя
        user.update_name_subscription("Spotify", "Spotify Premium")
        self.assertEqual(user.find_subscription("Spotify Premium")['name'], "Spotify Premium")
        self.assertIsNone(user.find_subscription("Spotify"))

    def test_main_scenario_with_different_periods(self):
        """Проверка сценария с различными периодами подписок"""
        user = UserProfile("test", "test@test.ru", "pass")

        # Добавляем подписки с разными периодами
        daily_sub = Subscription("Daily", 10, "day", "other")
        weekly_sub = Subscription("Weekly", 50, "week", "other")
        monthly_sub = Subscription("Monthly", 200, "month", "other")
        yearly_sub = Subscription("Yearly", 2000, "year", "other")

        user.add_subscription(daily_sub.get_subscription())
        user.add_subscription(weekly_sub.get_subscription())
        user.add_subscription(monthly_sub.get_subscription())
        user.add_subscription(yearly_sub.get_subscription())

        # Проверяем расчеты за месяц
        # Daily: 10 * 30 = 300
        # Weekly: 50 * 4.3 = 215
        # Monthly: 200
        # Yearly: 2000 / 12 = 166
        monthly = user.summary_for_month()
        expected = 300 + 215 + 200 + 166
        self.assertEqual(monthly, expected)

        # Проверяем расчеты за год
        # Daily: 10 * 365 = 3650
        # Weekly: 50 * 52 = 2600
        # Monthly: 200 * 12 = 2400
        # Yearly: 2000
        yearly = user.summary_for_year()
        expected_yearly = 3650 + 2600 + 2400 + 2000
        self.assertEqual(yearly, expected_yearly)


if __name__ == '__main__':
    unittest.main()