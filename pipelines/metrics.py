from pandas import DataFrame

from helper.constants import EMAIL, ISO_CURRENCIES, ISO_COUNTRIES


def get_metrics(customers: DataFrame, transactions: DataFrame, cleaned: DataFrame, invalid: DataFrame):
    metrics = {}

    # -----------------------------
    # Volume
    # -----------------------------
    metrics["customers_total"] = len(customers)
    metrics["transactions_total"] = len(transactions)
    metrics["cleaned_total"] = len(cleaned)
    metrics["invalid_total"] = len(invalid)

    # -----------------------------
    # Completeness (null percentages)
    # -----------------------------
    for col in customers.columns:
        metrics[f"customers_completeness_{col}"] = 1 - customers[col].isnull().mean()

    for col in transactions.columns:
        metrics[f"transactions_completeness_{col}"] = 1 - transactions[col].isnull().mean()

    # -----------------------------
    # Uniqueness
    # -----------------------------
    metrics["customers_unique_customer_id"] = customers["customer_id"].nunique()
    metrics["transactions_unique_transaction_id"] = transactions["transaction_id"].nunique()

    # -----------------------------
    # Validity
    # -----------------------------
    # Emails
    metrics["customers_valid_email_pct"] = customers["email"].str.match(EMAIL, na=False).mean()

    # Countries
    metrics["transactions_valid_countries_pct"] = customers["country"].isin(ISO_COUNTRIES).mean()

    # Currencies
    metrics["transactions_valid_currency_pct"] = transactions["currency"].isin(ISO_CURRENCIES).mean()

    # Amounts >= 0
    metrics["transactions_valid_amount_pct"] = (transactions["amount"] >= 0).mean()

    # Dates
    metrics["customers_valid_signup_date_pct"] = customers["signup_date"].notnull().mean()
    metrics["transactions_valid_transaction_date_pct"] = transactions["transaction_date"].notnull().mean()

    return metrics