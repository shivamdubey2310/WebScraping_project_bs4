# Python Jobs ETL Pipeline 🚀

A comprehensive ETL (Extract, Transform, Load) pipeline built with Apache Airflow to automatically scrape, process, and store Python job listings from [python.org/jobs](https://www.python.org/jobs/) into a PostgreSQL database.

---

[!Diagram](https://github.com/shivamdubey2310/WebScraping_project_bs4/blob/main/bs4.drawio.png)

---

## 🌐 Overview

This automated data pipeline:

* **Extracts** job listings from python.org daily using web scraping
* **Transforms** the raw data by cleaning, normalizing, and structuring it
* **Loads** the processed data into a PostgreSQL database for analysis
* **Orchestrates** the entire workflow using Apache Airflow with Docker

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   EXTRACTION    │     │  TRANSFORMATION  │     │     LOADING     │
│                 │     │                  │     │                 │
│ • Web Scraping  │───▶│ • Data Cleaning  │───▶│ • PostgreSQL DB │
│ • BeautifulSoup │     │ • CSV Merging    │     │ • Table Creation│
│ • Pagination    │     │ • Data Validation│     │ • Data Insert   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## 📚 Features

* **Automated Daily Extraction**: Scrapes all job pages automatically
* **Comprehensive Data Capture**: Job title, company, location, type, posting date, category, and application links
* **Data Transformation**: Merges multiple CSV files and normalizes job data
* **Database Integration**: Creates and populates PostgreSQL tables
* **Airflow Orchestration**: Scheduled daily runs with dependency management
* **Docker Support**: Containerized deployment with Astro CLI
* **Error Handling & Logging**: Comprehensive logging throughout the pipeline

---

## 📦 Requirements & Setup

### Prerequisites
* Docker and Docker Compose
* Apache Airflow (managed via Astro CLI)
* PostgreSQL database

### Python Dependencies
```bash
pip install -r astro_project/requirements.txt
```

**Key packages:**
* `pandas` - Data manipulation and analysis
* `sqlalchemy` - Database toolkit and ORM
* `requests` - HTTP library for web scraping
* `beautifulsoup4` - HTML/XML parser
* `psycopg2-binary` - PostgreSQL adapter
* `python-dotenv` - Environment variables management

### Environment Variables
Create a `.env` file in the `astro_project` directory:
```bash
DB_USER=your_postgres_user
DB_HOST=your_postgres_host
DB_PASS=your_postgres_password
DB_PORT=5432
DB_NAME=python_jobs_db
```

### Airflow Setup
```bash
# Initialize Airflow project with Astro CLI
astro dev init

# Start the Airflow environment
astro dev start
```

---

## 💡 How It Works

### Daily ETL Pipeline

1. **Extract** (Task 1):
   * Scrapes all pages of job listings from python.org/jobs
   * Extracts job details: title, company, location, type, posting date, category, and application links
   * Saves raw data as CSV files (one per page)

2. **Transform** (Task 2):
   * Merges all individual CSV files into a single dataset
   * Cleans and normalizes job data
   * Handles data type conversions and formatting
   * Creates structured data ready for database insertion

3. **Load** (Task 3):
   * Connects to PostgreSQL database
   * Creates database schema and tables if they don't exist
   * Inserts transformed data into the database
   * Handles duplicate prevention and data integrity

### Airflow DAG
The pipeline runs daily (`@daily` schedule) with the following task dependencies:
```
Extract → Transform → Load
```

---

## � Database Schema

The pipeline creates the following tables in PostgreSQL:

### `jobs` table
| Column | Type | Description |
|--------|------|-------------|
| job_id | SERIAL PRIMARY KEY | Unique identifier |
| job_title | VARCHAR | Job position title |
| company_name | VARCHAR | Hiring company name |
| location | VARCHAR | Job location |
| job_type | TEXT[] | Array of job types (Full-time, Remote, etc.) |
| posted_date | DATE | When the job was posted |
| job_category | VARCHAR | Job category/field |
| job_apply_full_link | VARCHAR | Direct application URL |

### `job_type` table
| Column | Type | Description |
|--------|------|-------------|
| type_id | SERIAL PRIMARY KEY | Unique identifier |
| job_id | INTEGER | Foreign key to jobs table |
| type_name | VARCHAR | Individual job type |

---

## 🖥️ Usage

### Running the Pipeline

1. **Start Airflow:**
   ```bash
   cd astro_project
   astro dev start
   ```

2. **Access Airflow UI:**
   Open http://localhost:8080 in your browser

3. **Trigger the DAG:**
   * Navigate to the `python_org_jobs` DAG
   * Click "Trigger DAG" or wait for the daily schedule

4. **Monitor Progress:**
   * View task logs and status in the Airflow UI
   * Check the PostgreSQL database for inserted data

### Querying the Data

```sql
-- Get all remote Python jobs from the last week
SELECT job_title, company_name, posted_date, job_apply_full_link 
FROM jobs 
WHERE location ILIKE '%remote%' 
  AND posted_date >= CURRENT_DATE - INTERVAL '7 days';

-- Count jobs by location
SELECT location, COUNT(*) as job_count 
FROM jobs 
GROUP BY location 
ORDER BY job_count DESC;
```

---

## 🎓 Educational Value

This project demonstrates advanced data engineering concepts:

* **ETL Pipeline Design**: Extract, Transform, Load pattern implementation
* **Workflow Orchestration**: Apache Airflow DAG creation and scheduling
* **Web Scraping**: Advanced BeautifulSoup techniques with pagination
* **Data Processing**: Pandas for data manipulation and cleaning
* **Database Integration**: SQLAlchemy ORM and PostgreSQL operations
* **Containerization**: Docker and Astro CLI for deployment
* **Error Handling**: Comprehensive logging and exception management
* **Configuration Management**: Environment variables and .env files

---

## 🚫 Disclaimer

This scraper is designed for educational and personal use only. Be respectful to `python.org`'s terms of service.

---

## 🚀 Future Improvements

* **Data Analytics Dashboard**: Build a Streamlit/Dash dashboard for job market insights
* **Advanced Filtering**: Add keyword search and salary range filtering
* **Data Quality Monitoring**: Implement data validation and quality checks
* **Notification System**: Email alerts for new jobs matching specific criteria
* **Cloud Deployment**: Deploy on AWS/GCP with managed Airflow (MWAA/Cloud Composer)
* **Data Warehouse Integration**: Connect to BigQuery/Snowflake for analytics

---

## 📁 Project Structure

```
WebScraping_project_bs4/
├── astro_project/                # Airflow project directory
│   ├── dags/
│   │   ├── python_org_jobs.py    # Main ETL DAG
│   │   └── exampledag.py         # Example DAG
│   ├── include/
│   │   ├── Extraction.py         # Web scraping logic
│   │   ├── Transform.py          # Data transformation
│   │   ├── Load.py               # Database loading
│   │   └── CSVs/                 # Temporary CSV storage
│   ├── tests/                    # Unit tests
│   ├── Dockerfile                # Container configuration
│   ├── requirements.txt          # Python dependencies
│   └── airflow_settings.yaml     # Airflow configuration
├── python_env/                   # Virtual environment
└── README.md                     # Project documentation
```

---

## ✅ License

MIT License. Free to use and modify.