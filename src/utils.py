import pandas as pd


def reader_excel_transaction(file_excel):
    """Функция, которая загружает информацию из файла excel и выводит список словарей с данными"""
    excel_reader = pd.read_excel(file_excel)
    list_excel_transactions = excel_reader.to_dict(orient="records")
    return list_excel_transactions

# print(reader_excel_transaction('../data/operations.xlsx'))
