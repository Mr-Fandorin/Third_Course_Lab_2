import datetime
import json
import os
from collections import defaultdict
from datetime import datetime
from urllib.request import urlopen

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_SHARES = os.getenv("API_KEY_SHARES")


def reader_excel_transaction(file_excel):
    """Функция, которая загружает информацию из файла excel и выводит список словарей с данными"""
    excel_reader = pd.read_excel(file_excel)
    excel_reader = excel_reader.replace({np.nan: None})
    list_excel_transactions = excel_reader.to_dict(orient="records")

    return list_excel_transactions


def get_period_transactions(list_trans, sort_date):
    """Выборка данных по периоду от начала месяца до заданной даты того же месяца"""
    start_full_date = f"01-{sort_date[3:10]} 00:00:00"
    new_list_trans = []
    start_date = datetime.datetime.strptime(start_full_date, "%d-%m-%Y %H:%M:%S")
    end_date = datetime.datetime.strptime(sort_date, "%d-%m-%Y %H:%M:%S")
    for item in list_trans:
        operation_data = item["Дата операции"]
        split_data = f"{operation_data[:2]}-{operation_data[3:5]}-{operation_data[6:]}"
        now_date = datetime.datetime.strptime(split_data, "%d-%m-%Y %H:%M:%S")
        if start_date <= now_date <= end_date:
            new_list_trans.append(item)
    return new_list_trans


def get_current_time():
    """Вывод приветствия в соответствии с текущим временем суток"""
    current_date_time = datetime.datetime.now().time()
    time_morning_start = datetime.datetime.strptime("06:00:00", "%H:%M:%S").time()
    time_morning_end = datetime.datetime.strptime("11:59:59", "%H:%M:%S").time()
    time_day_start = datetime.datetime.strptime("12:00:00", "%H:%M:%S").time()
    time_day_end = datetime.datetime.strptime("17:59:59", "%H:%M:%S").time()
    time_evening_start = datetime.datetime.strptime("18:00:00", "%H:%M:%S").time()
    time_evening_end = datetime.datetime.strptime("23:59:59", "%H:%M:%S").time()
    time_night_start = datetime.datetime.strptime("00:00:00", "%H:%M:%S").time()
    time_night_end = datetime.datetime.strptime("05:59:59", "%H:%M:%S").time()

    if time_morning_start <= current_date_time <= time_morning_end:
        return f'{"Доброе утро"}'
    elif time_day_start <= current_date_time <= time_day_end:
        return f'{"Добрый день"}'
    elif time_evening_start <= current_date_time <= time_evening_end:
        return f'{"Добрый вечер"}'
    elif time_night_start <= current_date_time <= time_night_end:
        return f'{"Доброй ночи"}'


def sort_by_paiment(list_of_transactions: list[dict], sorting_type: bool = True) -> list[dict]:
    """Функция, сортирующая словари по нужному ключу"""
    sorted_list_of_paiment = sorted(
        list_of_transactions, key=lambda dict_user: abs(dict_user["Сумма операции"]), reverse=sorting_type
    )
    return sorted_list_of_paiment


def counter_by_card(transactions_by_period):
    """Подсчет суммы платежей по картам"""
    cards_dict = defaultdict(list)
    list_top_transactions = []
    for item in transactions_by_period:
        cards_dict[item["Номер карты"]].append(item["Сумма платежа"])
        dict_card = dict(cards_dict)
        new_dict_cards = {}
        for key, value in dict_card.items():
            sum_paiments = sum(value)
            new_dict_cards[key] = sum_paiments
        list_cards_data = []
        for key, value in new_dict_cards.items():
            dict_card_paiments = {}
            dict_card_paiments["last_digits"] = key
            dict_card_paiments["total_spent"] = abs(value)
            dict_card_paiments["cashback"] = abs(value / 100)
            list_cards_data.append(dict_card_paiments)
    for item in transactions_by_period[:5]:
        dict_top_transactions = {}
        dict_top_transactions["date"] = item["Дата платежа"]
        dict_top_transactions["amount"] = abs(item["Сумма операции"])
        dict_top_transactions["category"] = item["Категория"]
        dict_top_transactions["description"] = item["Описание"]
        list_top_transactions.append(dict_top_transactions)
    with open("../data/output.json", "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = {}
    if isinstance(existing_data, dict):
        new_data = {"cards": list_cards_data, "top_transactions": list_top_transactions}
        existing_data.update(new_data)
    with open("../data/output.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


def get_exchange_rate(dict_currency):
    """Получение курса валюты по API запросу"""
    list_of_currency = dict_currency["user_currencies"]
    list_rates = []
    for currency in list_of_currency:
        to_currency = "RUB"
        from_currency = currency
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount=100"
        payload = {}
        headers = {"apikey": API_KEY}
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        result = response.json()
        dict_rate = {}
        dict_rate["currency"] = from_currency
        dict_rate["rate"] = result["info"]["rate"]
        list_rates.append(dict_rate)
    with open("../data/output.json", "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = {}
    if isinstance(existing_data, dict):
        new_data = {"currency_rates": list_rates}
        existing_data.update(new_data)
    with open("../data/output.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


def get_jsonparsed_data(dict_symbol_names_company):
    """Получение стоимости акций по API запросу"""
    list_symbol_stocks = dict_symbol_names_company["user_stocks"]
    list_of_stocks = []
    for stock in list_symbol_stocks:
        url = f"https://financialmodelingprep.com/stable/quote-short?symbol={stock}&apikey={API_KEY_SHARES}"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        try:
            data_list = json.loads(data.replace("'", '"'))
        except json.JSONDecodeError as e:
            print("Ошибка декодирования JSON:", e)
        dict_stock = {}
        dict_stock["stock"] = stock
        dict_stock["price"] = data_list[0]["price"]
        list_of_stocks.append(dict_stock)
    with open("../data/output.json", "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = {}
    if isinstance(existing_data, dict):
        new_data = {"stock_prices": list_of_stocks}
        existing_data.update(new_data)
    with open("../data/output.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


def get_setting(file_name):
    """Получаем пользовательские настройки из файла JSON"""
    with open(file_name) as f:
        data = json.load(f)
        return data

