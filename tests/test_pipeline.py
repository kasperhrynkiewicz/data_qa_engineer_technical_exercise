from pandas import DataFrame
from helper.assertions import Assertions
from helper.constants import EMAIL


def test_transform_returns_cleaned_and_invalid(etl, customer_data, transaction_data):
    cleaned, invalid = etl.transform(customer_data, transaction_data)

    assert isinstance(cleaned, DataFrame)
    assert isinstance(invalid, DataFrame)


def test_cleaned_schema(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)

    expected_columns = {
        "transaction_id",
        "customer_id",
        "amount",
        "currency",
        "transaction_date",
        "name",
        "email",
        "signup_date",
    }
    Assertions.assert_columns(cleaned, expected_columns)


def test_transform_removes_doubled_customer_id(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_unique(cleaned, "customer_id")


def test_transform_removes_null_names(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_not_null(cleaned, "name")


def test_transform_removes_invalid_emails(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_regex(cleaned, "email", EMAIL)


def test_transform_removes_invalid_signup_dates(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_date(cleaned, "signup_date")


def test_transform_removes_doubled_transaction_id(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_unique(cleaned, "transaction_id")


def test_transform_enforces_foreign_key(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_in(cleaned, "customer_id", customer_data["customer_id"])


def test_transform_removes_negative_amounts(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_not_negative(cleaned, "amount")


def test_transform_removes_invalid_currencies(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_iso_currency(cleaned, "currency")


def test_transform_removes_invalid_transaction_dates(etl, customer_data, transaction_data):
    cleaned, _ = etl.transform(customer_data, transaction_data)
    Assertions.assert_date(cleaned, "transaction_date")
