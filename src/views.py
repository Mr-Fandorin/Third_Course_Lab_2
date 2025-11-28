import json

from src.utils import (counter_by_card, get_current_time, get_exchange_rate, get_period_transactions, get_setting,
                       get_share_price, reader_excel_transaction, sort_by_paiment)


def get_info_by_request(request_date):
    """Функция по переданной дате выдает транзакции за период от начала месяца до введенной даты,
    также сообщает текщий курс по валютам из файла пользователя,
    также выдает стоимость акций по компаниям из файла пользователя"""
    print(get_current_time())  # Приветствие согласно текущему времени суток
    dict_hi = {}
    dict_hi["greeting"] = "Добрый день"  # Запись приветствия в файл JSON
    with open("../data/output.json", "w", encoding="utf-8") as f:
        json.dump(dict_hi, f, ensure_ascii=False)
    list_transaction = reader_excel_transaction("../data/operations.xlsx")  # Загрузка информации из файла Excel
    period_list_transactions = get_period_transactions(list_transaction, request_date)  # Загрузка данных по периоду
    sort_list_transactions = sort_by_paiment(period_list_transactions)  # Сортировка данных по сумме платежей
    add_json_info = counter_by_card(sort_list_transactions)  # Подсчет сумм переводам по картам
    user_data = get_setting("../data/user_settings.json")  # Считывание данных из JSON-файла пользователя
    user_rates = get_exchange_rate(user_data)  # Запрос курса валют по API
    user_stocks = get_share_price(user_data)  # Запрос стоимости акций по API
    with open("../data/output.json", "r", encoding="utf-8") as f:  # Чтение итогового файла JSON со всеми данными
        existing_data = json.load(f)

    return existing_data


# print(get_info_by_request("04-01-2018 15:00:41"))

