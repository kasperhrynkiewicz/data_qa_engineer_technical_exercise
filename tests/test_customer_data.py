from helper.assertions import Assertions
from helper.constants import EMAIL


def test_customer_id_not_null(customer_data):
    Assertions.assert_not_null(customer_data, "customer_id")


def test_customer_id_unique(customer_data):
    Assertions.assert_unique(customer_data, "customer_id")


def test_name_not_null(customer_data):
    Assertions.assert_not_null(customer_data, "name")


def test_email_format(customer_data):
    Assertions.assert_regex(customer_data, "email", EMAIL)


def test_signup_date_valid(customer_data):
    Assertions.assert_date(customer_data, "signup_date")
