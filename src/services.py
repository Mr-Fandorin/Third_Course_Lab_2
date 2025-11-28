import datetime
import logging
from collections import defaultdict

from src.utils import reader_excel_transaction

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/services.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_month_transactions(list_trans, year, month):
    """Выборка данных по месяцу и году"""
    new_list_trans = []
    logger.info("Начинаем сортировку базы данных")
    for item in list_trans:
        operation_data = item["Дата операции"][:10]
        date_obj = datetime.datetime.strptime(operation_data, "%d.%m.%Y")
        year_date = date_obj.year
        month_date = date_obj.month
        if month_date == int(month) and year_date == int(year):
            new_list_trans.append(item)
    logger.info("Сформировали новую базу данных за указанный месяц")
    return new_list_trans


def counter_by_category(transactions_in_month):
    """Подсчет сумм кэшбэков по категориям"""
    if transactions_in_month == []:
        logger.info("Нет данных за этот месяц")
        return "Нет информации за данный месяц"
    cards_dict = defaultdict(list)
    logger.info("Начинаем формирование данных по кэшбэкам за месяц")
    for item in transactions_in_month:
        if item["Кэшбэк"] == None:
            cards_dict[f'Категория {item["Категория"]}'].append(0)
            dict_card = dict(cards_dict)
        else:
            cards_dict[f'Категория {item["Категория"]}'].append(item["Кэшбэк"])
            dict_card = dict(cards_dict)
        new_dict_cards = {}
        for key, value in dict_card.items():
            sum_paiments = sum(value)
            new_dict_cards[key] = sum_paiments
    logger.info("Сформирована база по кэшбэкам за месяц")
    return new_dict_cards


def get_cashback_sum(file_name, year, month):
    """Главная функция, которая принимает путь к файлу, год и месяц, и выдает суммы кэшбэков по категориям"""
    list_transaction = reader_excel_transaction(file_name)  # Загрузка информации из файла Excel
    logger.info("Выгрузили данные из файла Excel")
    month_transactions = get_month_transactions(list_transaction, year, month)  # Выборка данных за месяц
    logger.info("Произвели выборку данных за нужный месяц")
    sum_cashback_by_category = counter_by_category(month_transactions)  # Подсчет сумм кэшбэков
    logger.info("Подсчитали данные по кэшбэкам за нужный месяц")
    return sum_cashback_by_category


# print(get_cashback_sum("../data/operations.xlsx", "2019", "07"))
