import pytest

from src.services import counter_by_category, get_month_transactions


@pytest.mark.parametrize(
    "year, month, expected",
    [
        (
            "2018",
            "03",
            [
                {
                    "Дата операции": "04.03.2018 15:00:41",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -21.37,
                    "Номер карты": "*2121",
                }
            ],
        ),
        (
            "2020",
            "01",
            [
                {
                    "Дата операции": "03.01.2020 15:03:35",
                    "Дата платежа": "04.01.2018",
                    "Сумма операции": -40.37,
                    "Номер карты": "*7197",
                }
            ],
        ),
    ],
)
def test_get_month_transactions(list_of_transactions, year, month, expected):
    assert get_month_transactions(list_of_transactions, year, month) == expected


@pytest.mark.parametrize(
    "expected",
    [
        {
            "Категория Цветы": 0,
            "Категория Топливо": 0,
            "Категория Супермаркеты": 0,
            "Категория Красота": 0,
            "Категория Переводы": 0,
        }
    ],
)
def test_counter_by_category_empty(transactions, expected):
    assert counter_by_category(transactions) == expected


def test_counter_by_category():
    result = counter_by_category([])
    assert result == "Нет информации за данный месяц"

