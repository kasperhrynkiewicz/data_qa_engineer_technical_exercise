import pytest
from pandas import DataFrame

from pipelines.etl import ETL

@pytest.fixture(scope="session")
def etl() -> ETL:
    return ETL()

@pytest.fixture
def extracted_data(etl) -> tuple[DataFrame, DataFrame]:
    return etl.extract()

@pytest.fixture
def customer_data(extracted_data) -> DataFrame:
    customers, _ = extracted_data
    return customers

@pytest.fixture
def transaction_data(extracted_data) -> DataFrame:
    _, transactions = extracted_data
    return transactions
