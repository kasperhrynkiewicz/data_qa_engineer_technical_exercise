from typing import Tuple

import pandas as pd

from pathlib import Path
from pandas import DataFrame
from helper.constants import EMAIL, ISO_CURRENCIES


class ETL:
    def __init__(self, input_dir="data_files/raw", output_dir="data_files/clean"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    def extract(self) -> Tuple[DataFrame, DataFrame]:
        """Read raw customer and transaction CSVs into DataFrames."""
        customers = pd.read_csv(self.input_dir / "customer_raw.csv")
        print("Customers data extracted successfully.")
        transactions = pd.read_csv(self.input_dir / "transaction_raw.csv")
        print("Transactions data extracted successfully.")
        return customers, transactions

    @staticmethod
    def transform(customers: DataFrame, transactions: DataFrame)  -> Tuple[DataFrame, DataFrame]:
        """Clean and standardize raw data."""
        # -----------------------------
        # Customer validation
        # -----------------------------
        customers = customers.copy()
        customers["customer_id"] = pd.to_numeric(customers["customer_id"], errors="coerce")
        customers["signup_date"] = pd.to_datetime(customers["signup_date"], errors="coerce", format="%d-%m-%Y")

        # Flags for invalid rows
        customers["valid"] = True
        customers.loc[customers["customer_id"].isnull(), "valid"] = False
        customers.loc[customers.duplicated("customer_id", keep=False), "valid"] = False
        customers.loc[customers["name"].isnull(), "valid"] = False
        customers.loc[~customers["email"].str.match(EMAIL, na=False), "valid"] = False
        customers.loc[customers["signup_date"].isnull(), "valid"] = False

        valid_customers = customers[customers["valid"]].drop(columns=["valid"])
        invalid_customers = customers[~customers["valid"]].drop(columns=["valid"])

        # -----------------------------
        # Transaction validation
        # -----------------------------
        transactions = transactions.copy()
        transactions["transaction_id"] = pd.to_numeric(transactions["transaction_id"], errors="coerce")
        transactions["customer_id"] = pd.to_numeric(transactions["customer_id"], errors="coerce")
        transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce")
        transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"], errors="coerce",
                                                          format="%Y-%m-%d")

        transactions["valid"] = True
        transactions.loc[transactions["transaction_id"].isnull(), "valid"] = False
        transactions.loc[transactions.duplicated("transaction_id", keep=False), "valid"] = False
        transactions.loc[transactions["customer_id"].isnull(), "valid"] = False
        transactions.loc[~transactions["customer_id"].isin(valid_customers["customer_id"]), "valid"] = False
        transactions.loc[transactions["amount"].isnull() | (transactions["amount"] < 0), "valid"] = False
        transactions.loc[transactions["currency"].isnull() | ~transactions["currency"].str.upper().isin(
            ISO_CURRENCIES), "valid"] = False
        transactions.loc[transactions["transaction_date"].isnull(), "valid"] = False

        valid_transactions = transactions[transactions["valid"]].drop(columns=["valid"])
        invalid_transactions = transactions[~transactions["valid"]].drop(columns=["valid"])

        # -----------------------------
        # Merge valid customers + transactions
        # -----------------------------
        cleaned = valid_transactions.merge(valid_customers, on="customer_id", how="inner")
        # Combine invalids for auditing
        invalid = pd.concat([invalid_customers, invalid_transactions], axis=0, ignore_index=True)

        print("Data transformed.")
        return cleaned, invalid

    def load(self, df: DataFrame, filename="cleaned_data.csv"):
        """Save cleaned data to output directory."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False)

        print(f"Clean data loaded to: {output_path}")
        return output_path
