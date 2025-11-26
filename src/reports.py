import csv
import datetime
from collections import defaultdict
from typing import Optional

import pandas as pd


def get_period_transactions(list_trans, user_date = None):
    """Выборка данных за три месяца до заданной даты"""

    if user_date == None:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=90)
    else:
        end_date = datetime.datetime.strptime(user_date, "%d-%m-%Y")
        start_date = end_date - datetime.timedelta(days=90)
    new_list_trans = []
    for item in list_trans:
        operation_data = item["Дата операции"]
        split_data = f"{operation_data[:2]}-{operation_data[3:5]}-{operation_data[6:]}"
        now_date = datetime.datetime.strptime(split_data, "%d-%m-%Y %H:%M:%S")
        if start_date <= now_date <= end_date:
            new_list_trans.append(item)
    return new_list_trans



def counter_by_category(transactions_in_three_month, category):
    """Подсчет сумм по заданной категории"""
    if transactions_in_three_month == []:
        return 'Не найдено операций за данный период'
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

    return new_dict_cards


def save_report(filename="../data/category.csv"):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_csv(filename, index=False, encoding='utf-8')
            return result
        return wrapper
    return my_decorator



@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    list_transactions = transactions.to_dict(orient="records")
    sorted_list = get_period_transactions(list_transactions, date)
    sum_paiments_by_category = counter_by_category(sorted_list, category)
    df = pd.DataFrame([sum_paiments_by_category])
    return df






