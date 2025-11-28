import pathlib

import pandas as pd
import pytest

from src.reports import counter_by_category, get_period_transactions, save_report


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            None,
            [],
        ),
        (
            "03-01-2018",
            [
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
            ],
        ),
    ],
)
def test_get_period_transactions(transactions, date, expected):
    assert get_period_transactions(transactions, date) == expected


@pytest.mark.parametrize(
    "category, expected",
    [
        ("Сумма платежа", {"Сумма платежа": 196718.33}),
    ],
)
def test_counter_by_category(transactions, category, expected):
    assert counter_by_category(transactions, category) == expected


def test_counter_by_category_empty():
    result = counter_by_category([], "Сумма платежа")
    assert result == "Не найдено операций за данный период"


def test_save_report(tmp_path: pathlib.Path):
    csv_file = tmp_path / "category.csv"

    @save_report(str(csv_file))
    def my_function(x, y):
        data = {"sum": [x + y]}
        return pd.DataFrame(data)

    result = my_function(2, 3)
    expected = pd.DataFrame({"sum": [5]})
    pd.testing.assert_frame_equal(result, expected)
