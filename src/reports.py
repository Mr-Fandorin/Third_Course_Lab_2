import datetime
import logging
from collections import defaultdict
from typing import Optional

import pandas as pd

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/reports.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

data_test = [
    {
        "Дата операции": "05.01.2018 14:58:38",
        "Дата платежа": "07.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -120.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -120.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Цветы",
        "MCC": 5992.0,
        "Описание": "Magazin  Prestizh",
        "Бонусы (включая кэшбэк)": 2,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 120.0,
    },
    {
        "Дата операции": "04.01.2018 15:00:41",
        "Дата платежа": "05.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -1025.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -1025.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Топливо",
        "MCC": 5541.0,
        "Описание": "Pskov AZS 12 K2",
        "Бонусы (включая кэшбэк)": 20,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 1025.0,
    },
    {
        "Дата операции": "04.01.2018 14:05:08",
        "Дата платежа": "06.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -1065.9,
        "Валюта операции": "RUB",
        "Сумма платежа": -1065.9,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Пятёрочка",
        "Бонусы (включая кэшбэк)": 21,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 1065.9,
    },
    {
        "Дата операции": "03.01.2018 15:03:35",
        "Дата платежа": "04.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -73.06,
        "Валюта операции": "RUB",
        "Сумма платежа": -73.06,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Супермаркеты",
        "MCC": 5499.0,
        "Описание": "Magazin 25",
        "Бонусы (включая кэшбэк)": 1,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 73.06,
    },
    {
        "Дата операции": "03.01.2018 14:55:21",
        "Дата платежа": "05.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -21.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -21.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Красота",
        "MCC": 5977.0,
        "Описание": "OOO Balid",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 21.0,
    },
    {
        "Дата операции": "01.01.2018 20:27:51",
        "Дата платежа": "04.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -316.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -316.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Красота",
        "MCC": 5977.0,
        "Описание": "OOO Balid",
        "Бонусы (включая кэшбэк)": 6,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 316.0,
    },
    {
        "Дата операции": "01.01.2018 12:49:53",
        "Дата платежа": "01.01.2018",
        "Номер карты": None,
        "Статус": "OK",
        "Сумма операции": -3000.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -3000.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Переводы",
        "MCC": None,
        "Описание": "Линзомат ТЦ Юность",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 3000.0,
    },
    {
        "Дата операции": "31.12.2017 19:16:45",
        "Дата платежа": "16.07.2019",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -101.37,
        "Валюта операции": "RUB",
        "Сумма платежа": -101.37,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Магнит",
        "Бонусы (включая кэшбэк)": 2,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 101.37,
    },
]

df_data = pd.DataFrame(data_test)


def get_period_transactions(list_trans, user_date=None):
    """Выборка данных за три месяца до заданной даты"""

    if user_date == None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=90)
        logger.info("Выбираем отсчет 3 месяца от текущей даты, т.к. пользователь не ввел месяц отбора")
    else:
        end_date = datetime.datetime.strptime(user_date, "%d-%m-%Y")
        start_date = end_date - datetime.timedelta(days=90)
        logger.info("Выбираем 3 месяца от даты пользователя")
    new_list_trans = []
    for item in list_trans:
        operation_data = item["Дата операции"]
        split_data = f"{operation_data[:2]}-{operation_data[3:5]}-{operation_data[6:]}"
        now_date = datetime.datetime.strptime(split_data, "%d-%m-%Y %H:%M:%S")
        if start_date <= now_date <= end_date:
            new_list_trans.append(item)
    logger.info("Выбрали данные за три месяца")
    return new_list_trans


def counter_by_category(transactions_in_three_month, category):
    """Подсчет сумм по заданной категории"""
    if transactions_in_three_month == []:
        logger.info("Нет данных за 3 месяца")
        return "Не найдено операций за данный период"
    else:
        cards_dict = defaultdict(list)
        for item in transactions_in_three_month:
            if item[category] == None:
                cards_dict[category].append(0)
                dict_card = dict(cards_dict)
            else:
                cards_dict[category].append(abs(item[category]))
                dict_card = dict(cards_dict)
            new_dict_cards = {}
            for key, value in dict_card.items():
                sum_paiments = sum(value)
                new_dict_cards[key] = sum_paiments
    logger.info("Выводим суммы по заданной категории за 3 месяца")
    return new_dict_cards


def save_report(filename="../data/category.csv"):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_csv(filename, index=False, encoding="utf-8")
            logger.info("Записали данные по суммам по категории за 3 месяца в файл CSV")
            return result

        return wrapper

    return my_decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    list_transactions = transactions.to_dict(orient="records")  # Получаем данные из файла Excel
    logger.info("Производим выгрузку из файла Excel")
    sorted_list = get_period_transactions(list_transactions, date)  # Выбираем данные за 3 месяца
    logger.info("Выбираем данные за 3 месяца")
    sum_paiments_by_category = counter_by_category(sorted_list, category)  # Производим подсчет сумм по категории
    logger.info("Выводим суммы по заданной категории за 3 месяца")
    df = pd.DataFrame([sum_paiments_by_category])
    logger.info("Формируем dataframe с данными")
    return df


# print(spending_by_category(df_data, 'Сумма операции с округлением', '04-01-2018'))

