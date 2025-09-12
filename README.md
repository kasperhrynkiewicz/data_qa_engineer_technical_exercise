# Data QA Engineer Technical Exercise

---

## Overview

This project demonstrates **automated data quality testing and monitoring** for a data pipeline that ingests customer and transaction CSV files.  

It includes:  

- **Unit tests** validating raw CSVs for schema, completeness, uniqueness, and data validity.  
- **ETL transform** that standardizes data, separates valid and invalid rows, and merges transactions with valid customers.  
- **Data quality metrics** automatically calculated and exported to JSON.  
- **CI/CD integration** using GitHub Actions:  
  - Runs tests  
  - Generates metrics  
  - Publishes metrics in the **GitHub Actions summary**  
  - Uploads reports as artifacts.

---

## Run Tests Locally

```bash
pytest -v --maxfail=1 --disable-warnings
```

---

## CI/CD Pipeline (GitHub Actions)

Runs automatically on **push** or **pull** request.

**Steps include:**

1. Checkout repository
2. Setup Python environment
3. Install dependencies
4. Run tests
5. Generate data quality metrics
6. Publish metrics in GitHub Actions job summary
7. Upload reports as artifacts (`reports/pytest-report.xml` and `reports/data_metrics.json`)

---

## Data Quality Metrics

Metrics include:

- **Volume**: total rows for customers, transactions, cleaned, invalid
- **Completeness**: fraction of non-null values per column
- **Uniqueness**: unique counts of primary keys
- **Validity**: valid emails, ISO currency codes, amounts ≥ 0, and valid dates
