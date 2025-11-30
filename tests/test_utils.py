import json
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest
from freezegun import freeze_time

from src.utils import (counter_by_card, get_current_time, get_exchange_rate, get_period_transactions, get_setting,
                       get_share_price, reader_excel_transaction, sort_by_paiment)
from tests.conftest import user_setting


def test_reader_excel_transaction():
    df = pd.DataFrame({"name": ["Tom", "Mike"], "age": ["35", "45"]})
    with patch("pandas.read_excel") as mocked_read:
        mocked_read.return_value = df
        result = reader_excel_transaction("list_data")
        expected = [{"age": "35", "name": "Tom"}, {"age": "45", "name": "Mike"}]
        assert result == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            "04-01-2018 15:00:41",
            [
                {
                    "Дата операции": "04.01.2018 14:05:08",
                    "Дата платежа": "06.01.2018",
                    "Сумма операции": -1001.37,
                    "Номер карты": "*7197",
                },
                {
                    "Дата операции": "03.01.2018 14:55:21",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -200.37,
                    "Номер карты": "*2121",
                },
            ],
        ),
        (
            "03-01-2018 15:00:41",
            [
                {
                    "Дата операции": "03.01.2018 14:55:21",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -200.37,
                    "Номер карты": "*2121",
                }
            ],
        ),
    ],
)
def test_get_period_transactions(list_of_transactions, date, expected):
    assert get_period_transactions(list_of_transactions, date) == expected


@pytest.mark.parametrize(
    "sorting_parameter, expected",
    [
        (
            True,
            [
                {
                    "Дата операции": "04.01.2018 14:05:08",
                    "Дата платежа": "06.01.2018",
                    "Сумма операции": -1001.37,
                    "Номер карты": "*7197",
                },
                {
                    "Дата операции": "03.01.2018 14:55:21",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -200.37,
                    "Номер карты": "*2121",
                },
                {
                    "Дата операции": "05.01.2019 14:58:38",
                    "Дата платежа": "07.01.2018",
                    "Сумма операции": -101.37,
                    "Номер карты": "*7197",
                },
                {
                    "Дата операции": "03.01.2020 15:03:35",
                    "Дата платежа": "04.01.2018",
                    "Сумма операции": -40.37,
                    "Номер карты": "*7197",
                },
                {
                    "Дата операции": "04.03.2018 15:00:41",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -21.37,
                    "Номер карты": "*2121",
                },
            ],
        ),
        (
            False,
            [
                {
                    "Дата операции": "04.03.2018 15:00:41",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -21.37,
                    "Номер карты": "*2121",
                },
                {
                    "Дата операции": "03.01.2020 15:03:35",
                    "Дата платежа": "04.01.2018",
                    "Сумма операции": -40.37,
                    "Номер карты": "*7197",
                },
                {
                    "Дата операции": "05.01.2019 14:58:38",
                    "Дата платежа": "07.01.2018",
                    "Сумма операции": -101.37,
                    "Номер карты": "*7197",
                },
                {
                    "Дата операции": "03.01.2018 14:55:21",
                    "Дата платежа": "05.01.2018",
                    "Сумма операции": -200.37,
                    "Номер карты": "*2121",
                },
                {
                    "Дата операции": "04.01.2018 14:05:08",
                    "Дата платежа": "06.01.2018",
                    "Сумма операции": -1001.37,
                    "Номер карты": "*7197",
                },
            ],
        ),
    ],
)
def test_sort_by_paiment(list_of_transactions, sorting_parameter, expected):
    assert sort_by_paiment(list_of_transactions, sorting_parameter) == expected


def test_get_current_time_day():
    part_of_day = "Добрый день"
    with freeze_time("2023-01-01 12:30:45"):
        result = get_current_time()
        assert result == part_of_day


def test_get_current_time_evening():
    part_of_day = "Добрый вечер"
    with freeze_time("2023-01-01 19:00:45"):
        result = get_current_time()
        assert result == part_of_day


def test_get_current_time_night():
    part_of_day = "Доброй ночи"
    with freeze_time("2023-01-01 02:30:45"):
        result = get_current_time()
        assert result == part_of_day


def test_get_current_time_morning():
    part_of_day = "Доброе утро"
    with freeze_time("2023-01-01 08:30:45"):
        result = get_current_time()
        assert result == part_of_day


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps(
        [
            {
                "Дата операции": "04.03.2018 15:00:41",
                "Дата платежа": "05.01.2018",
                "Сумма операции": -21.37,
                "Номер карты": "*2121",
            }
        ]
    ),
)
def test_get_setting(mock_file):
    assert get_setting("../data/output.json") == [
        {
            "Дата операции": "04.03.2018 15:00:41",
            "Дата платежа": "05.01.2018",
            "Сумма операции": -21.37,
            "Номер карты": "*2121",
        }
    ]
    mock_file.assert_called_once_with("../data/output.json")


def test_counter_by_card(transactions):
    test_file = "tests/dump_data.json"
    counter_by_card(transactions, test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data.get("cards") is not None
        assert data.get("top_transactions") is not None
        assert data["cards"][0] == {"last_digits": "*7197", "total_spent": 193718.33, "cashback": 1937.1833}
        assert data["top_transactions"][0] == {
            "date": "07.01.2018",
            "amount": 120000.0,
            "category": "Цветы",
            "description": "Magazin  Prestizh",
        }


def test_get_exchange_rate(user_setting):
    test_file = "tests/api_data.json"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 100},
        "info": {"timestamp": 1764272947, "rate": 77.949058},
        "date": "2025-11-27",
        "result": 7794.9058,
    }

    with patch("requests.request", return_value=mock_response):
        result = get_exchange_rate(user_setting, test_file)
        assert result == None
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["currency_rates"][0] == {"currency": "USD", "rate": 77.949058}


@patch("src.utils.urlopen")
def test_get_share_price(mock_urlopen, user_setting):
    test_file = "tests/api_share.json"
    mock_urlopen.return_value.read.return_value.decode.return_value = (
        '[{"symbol": "AAPL", "price": 277.55, "change": 0.58, "volume": 31050665}]'
    )
    result = get_share_price(user_setting, test_file)
    assert result is None
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["stock_prices"][0] == {"stock": "AAPL", "price": 277.55}
