import json

from pipelines.metrics import get_metrics


def test_data_quality_metrics(etl, customer_data, transaction_data, tmp_path):
    cleaned, invalid = etl.transform(customer_data, transaction_data)
    metrics = get_metrics(customer_data, transaction_data, cleaned, invalid)

    output_file = tmp_path / "dq_metrics.json"
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)
