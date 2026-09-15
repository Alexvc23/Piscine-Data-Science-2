# Piscine Data Science 2 - Technical Documentation & Project Journal

This repository contains the end-to-end lifecycle of data projects for the **Piscine Data Science 2** bootcamp, transitioning from infrastructure and ingestion (**Data Engineer**) to insights and patterns (**Data Analyst**) and predictive modeling (**Data Scientist**).

---

## 🛠️ Technical Stack & Environment Setup

### Stack Overview
* **Infrastructure:** Docker & Docker-Compose (containerized PostgreSQL & pgAdmin environment).
* **Storage / Warehouse:** PostgreSQL (relational database management, complex SQL transformations, window functions).
* **Languages:** Python 3 (Pandas, NumPy, Psycopg2) and SQL (PostgreSQL dialect).
* **Visualization:** Matplotlib, Seaborn.
* **Machine Learning:** Scikit-Learn (Preprocessing, K-Means, Decision Trees, KNN, Voting Classifiers).

### Quickstart & Environment Setup
1. **Run the Setup Script:**
   ```bash
   ./setup.sh
   ```
   This script creates a Python virtual environment (`env/`), installs all requirements from `requirements.txt`, and configures helper aliases (`norminette`, `py`, `pt`).

2. **Activate the Virtual Environment:**
   ```bash
   source env/bin/activate
   ```

3. **Start Infrastructure (Docker):**
   Navigate to the Data Engineering directory and launch PostgreSQL/pgAdmin:
   ```bash
   cd 0-DataEnginneer/ex00
   docker-compose up -d
   ```

---

## 🚀 Repository Roadmap & Architecture

### Section 0: Data Engineering (The Foundation)
* **Focus:** Infrastructure as Code and efficient ETL.
* **Key Highlights:**
  * `0-DataEnginneer/docker-compose.yml`: Local PostgreSQL 14 and pgAdmin 4 deployment.
  * `automatic_table.py`: High-performance bulk data loading using PostgreSQL `COPY` command via `psycopg2` (yielding up to 100x speed improvement over row-by-row `INSERT`).
* **Key Insight:** Reproducibility and secure credential management via `.env` files are critical pillars of robust data engineering.

### Section 1: Data Warehouse (The Cleanup)
* **Focus:** Data integrity, provenance, and optimization.
* **Key Highlights:**
  * `customers_table.sql`: Consolidating monthly e-commerce shards using `UNION ALL`.
  * `remove_duplicates.sql`: Utilizing SQL window functions (`LEAD()`, `PARTITION BY`) to detect and purge temporal duplicates.
* **Key Insight:** SQL-side data cleaning is significantly more efficient than Python-side processing for high-volume tabular datasets.

### Section 2: Data Analyst (The Insights)
* **Focus:** Descriptive analytics and customer segmentation.
* **Key Highlights:**
  * `mustache.py`: Box plot visualizations to identify price outliers and average cart values.
  * `elbow.py`: Implementing the Elbow Method to mathematically determine the optimal number of clusters ($k$) for customer segmentation.
* **Key Insight:** Translating raw transaction logs into actionable business intelligence (e.g., distinguishing high-value "Whale" customers from occasional buyers).

### Section 3: Data Scientist 1 (Preprocessing)
* **Focus:** Preparing data for Machine Learning.
* **Key Highlights:**
  * `Correlation.py`: Analyzing feature correlations to determine which knight attributes (Empowered, Prescience) drive Jedi/Sith classification.
  * `standardization.py` vs `Normalization.py`: Comparative analysis of Z-score scaling vs. Min-Max normalization.
* **Key Insight:** Strict adherence to the "Garbage In, Garbage Out" rule—proper feature scaling is non-negotiable prior to model training.

### Section 4: Data Scientist 2 (Modeling & Evaluation)
* **Focus:** Classification algorithms and ensemble learning.
* **Key Highlights:**
  * `Tree.ipynb` & `KNN.ipynb`: Comparing decision tree performance against K-Nearest Neighbors on the Star Wars dataset.
  * `democracy.ipynb`: Building a Voting Classifier (Ensemble method) to boost prediction robustness.
  * `Confusion_Matrix.ipynb`: Evaluating models beyond simple accuracy using Precision, Recall, and F1-scores.
* **Key Insight:** Balancing model interpretability (Decision Trees) with instance-based simplicity (KNN) while leveraging ensembles for peak performance.

---

## 📖 Navigation & Directory Structure
```
.
├── 0-DataEnginneer/     # Docker setup, PostgreSQL, high-speed COPY ETL scripts
├── 1-DataWarehouse/     # SQL shards union, deduplication, and data provenance
├── 2-DataAnalyst/       # Exploratory data analysis, boxplots, and K-Means clustering
├── 3-DataScientist1/    # Correlation analysis, standardization, normalization, and data splitting
├── 4-DataScientist2/    # Classification models, decision trees, KNN, and voting classifiers
├── instructions/        # Documentation roadmap and project guidelines
└── setup.sh             # Environment setup and dependency installer script
```

