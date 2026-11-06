## Azure Databricks Financial Data Pipeline

An enterprise-grade, end-to-end financial data pipeline built using **PySpark, Delta Lake, Databricks Asset Bundles (DABs), Databricks Community Edition, Docker, and GitHub Actions**, following the Medallion Architecture pattern.

---

## Architecture & Tech Stack
* **Cloud & Orchestration:** Databricks Community Edition, Databricks Asset Bundles (DABs), Unity Catalog
* **Processing Framework:** PySpark, Delta Lake (Bronze, Silver, Gold layers)
* **Testing & Quality Assurance:** Pytest, local `SparkSession` fixtures, Custom Circuit Breaker Quality Gates
* **Containerization & CI/CD:** Docker, GitHub Actions (`ci.yml`, `deploy.yml`)

---

## Quality Gate Exception Error
<img width="3770" height="1945" alt="image" src="https://github.com/user-attachments/assets/185ce3d7-16ce-4511-aa2f-434e3d213271" />

## Unit Testing Failed Error
<img width="3807" height="1867" alt="Screenshot 2026-11-05 141033" src="https://github.com/user-attachments/assets/9a4f0751-bc91-4b28-9e1a-77f089504c03" />

---

## Project Structure
```text
├── .github/workflows/      # CI/CD pipelines for automated testing and deployment
├── bundle/                 # Databricks job definitions (setup_job.yml, pipeline_job.yml)
├── scripts/                # Utility shell scripts (upload_landing.sh, healthcheck.sh)
├── src/                    # Core pipeline logic (Generator, Bronze, Silver, Gold layers)
├── unit_tests/             # Pytest suite with local Spark testing fixtures
├── .dockerignore           # Specifies files ignored during Docker builds
├── .gitignore              # Specifies files ignored by Git version control
├── Dockerfile              # Container recipe for the local data generator
├── databricks.yml          # Databricks Asset Bundle (DAB) root configuration
├── pytest.ini              # Pytest configuration settings
├── requirements-dev.txt    # Development and testing dependencies (PySpark, Pytest)
└── requirements.txt        # Core application dependencies
