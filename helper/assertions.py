import pandas as pd
from pandas import DataFrame

from helper.constants import ISO_CURRENCIES, ISO_COUNTRIES


class Assertions:
    @staticmethod
    def assert_not_null(data: DataFrame, column: str, message: str = None):
        nulls = data[data[column].isnull()]
        assertion_message = message if message is not None else f"Null found for {column}:\n{nulls}"
        assert nulls.empty, assertion_message

    @staticmethod
    def assert_not_negative(data: DataFrame, column: str, message: str = None):
        negatives = data[data[column] < 0]
        assertion_message = message if message is not None else f"Negative values found for {column}:\n{negatives}"
        assert negatives.empty, assertion_message

    @staticmethod
    def assert_unique(data: DataFrame, column: str, message: str = None):
        duplicates = data[data.duplicated(column, keep=False)]
        assertion_message = message if message is not None else f"Duplicates found for {column}:\n{duplicates}"
        assert duplicates.empty, assertion_message

    @staticmethod
    def assert_date(data: DataFrame, column: str, date_format: str = "%Y-%m-%d", message: str = None):
        invalid_dates = []
        for idx, val in data[column].items():
            try:
                pd.to_datetime(val, format=date_format, errors="raise")
            except (ValueError, TypeError):
                invalid_dates.append((idx, val))
        assertion_message = message if message is not None else f"Invalid date found for {column}:\n{invalid_dates}"
        assert not invalid_dates, assertion_message

    @staticmethod
    def assert_regex(data: DataFrame, column: str, regex: str, message: str = None):
        non_matching = data[~data[column].str.match(regex, na=False)]
        assertion_message = message if message is not None else f"Non matching value found for {column}:\n{non_matching}"
        assert non_matching.empty, assertion_message

    @staticmethod
    def assert_in(data: DataFrame, column: str, comparison_set: DataFrame, message: str = None):
        data_not_in = data[~data[column].isin(comparison_set)]
        assertion_message = message if message is not None else f"Invalid values found for `{column}`:\n{data_not_in[[column]]}"
        assert data_not_in.empty, assertion_message

    @staticmethod
    def assert_iso_currency(data: DataFrame, column: str, message: str = None):
        non_iso_currencies = data[~data[column].isin(ISO_CURRENCIES)]
        assertion_message = message if message is not None else f"Non ISO currencies found for `{column}`:\n{non_iso_currencies[[column]]}"
        assert non_iso_currencies.empty, assertion_message

    @staticmethod
    def assert_iso_country(data: DataFrame, column: str, message: str = None):
        non_iso_countries = data[~data[column].isin(ISO_COUNTRIES)]
        assertion_message = message if message is not None else f"Non ISO countries found for `{column}`:\n{non_iso_countries[[column]]}"
        assert non_iso_countries.empty, assertion_message

    @staticmethod
    def assert_columns(data: DataFrame, expected_columns: set, message: str = None):
        assertion_message = message if message is not None else f"Unexpected columns: {data.columns}"
        assert set(data.columns) == expected_columns, assertion_message
