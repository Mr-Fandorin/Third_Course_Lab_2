import json
from unittest.mock import mock_open, patch

from src.views import get_info_by_request


@patch("module_name.reader_excel_transaction")
@patch("module_name.get_period_transactions")
@patch("module_name.sort_by_paiment")
@patch("module_name.counter_by_card")
@patch("module_name.get_setting")
@patch("module_name.get_exchange_rate")
@patch("module_name.get_share_price")
def test_get_info_by_request(
    mock_get_share_price,
    mock_get_exchange_rate,
    mock_get_setting,
    mock_counter_by_card,
    mock_sort_by_paiment,
    mock_get_period_transactions,
    mock_reader_excel_transaction
):
    test_file = "../tests/view.json"
    mock_reader_excel_transaction.return_value = []
    mock_get_period_transactions.return_value = []
    mock_sort_by_paiment.return_value = []
    mock_counter_by_card.return_value = {}
    mock_get_setting.return_value = {}
    mock_get_exchange_rate.return_value = 1.0
    mock_get_share_price.return_value = 100.0

    result = get_info_by_request("04-01-2018 15:00:41", test_file)
    assert result == {"greeting": "Добрый день"}
    mock_reader_excel_transaction.assert_called_once_with("../data/operations.xlsx")
    mock_get_setting.assert_called_once_with("../data/user_settings.json")
