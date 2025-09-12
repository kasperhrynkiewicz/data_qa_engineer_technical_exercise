import json
import os

from pipelines.metrics import get_metrics


def test_data_quality_metrics(etl, customer_data, transaction_data):
    cleaned, invalid = etl.transform(customer_data, transaction_data)
    metrics = get_metrics(customer_data, transaction_data, cleaned, invalid)

    os.makedirs("reports", exist_ok=True)
    output_file = os.path.join("reports", "data_metrics.json")
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)

    assert os.path.exists(output_file), "Metrics file not created"
