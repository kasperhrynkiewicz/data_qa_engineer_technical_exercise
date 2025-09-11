from helper.assertions import Assertions


def test_transaction_id_not_null(transaction_data):
    Assertions.assert_not_null(transaction_data, "transaction_id")


def test_transaction_id_unique(transaction_data):
    Assertions.assert_unique(transaction_data, "transaction_id")


def test_non_existing_customer(transaction_data, customer_data):
    Assertions.assert_in(transaction_data, "customer_id", customer_data["customer_id"])


def test_amount_non_negative(transaction_data):
    Assertions.assert_not_negative(transaction_data, "amount")


def test_currency_iso(transaction_data):
    Assertions.assert_iso_currency(transaction_data, "currency")


def test_transaction_date_valid(transaction_data):
    Assertions.assert_date(transaction_data, "transaction_date")
