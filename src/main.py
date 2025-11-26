from typing import Optional

import pandas as pd

from src.reports import spending_by_category
from src.services import get_cashback_sum
from src.views import get_info_by_request


def main(filename: str, year: str, month: str, user_date: str, transactions: pd.DataFrame,
         category: str, date: Optional[str] = None):
    info_by_request = get_info_by_request(user_date)
    info_about_cashback = get_cashback_sum(filename, year, month)
    info_by_category = spending_by_category(transactions, category, date)

print(main('../data/operations.xlsx', '2019', '07', '04-01-2018 15:00:41',
           df, 'Сумма операции с округлением'))