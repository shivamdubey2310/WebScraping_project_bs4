import sqlalchemy as sal
import pandas as pd
import logging
from dotenv import load_dotenv
import os
import psycopg2
import time

# Loading .env variables
load_dotenv()

# Customizing logging.basicConfig() to format logging 
logging.basicConfig(
    level = logging.DEBUG,
    filename = "ETL_log.log",
    encoding = "utf-8",
    filemode = "a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)


def creating_schema():
    """
    This function creates db and tables in postgres
    """

    db_user = os.getenv("DB_USER")
    db_host = os.getenv("DB_HOST")
    db_pass = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    try:
        # isolation_level='AUTOCOMMIT' is required to run CREATE DATABASE
        engine_for_db = sal.create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/postgres", isolation_level='AUTOCOMMIT')
        
        with engine_for_db.connect() as conn:
            existing_dbs = conn.execute(sal.text("SELECT datname FROM pg_database;")).fetchall()
            if (db_name,) not in existing_dbs:
                conn.execute(sal.text(f"CREATE DATABASE {db_name}"))
    
    except Exception as e:
        logging.error(f"An Exception occured while creating {db_name} - {e}")
        return
    else:
        logging.info(f"{db_name} created successfully.")

    create_table_query = [
        """
            CREATE TABLE IF NOT EXISTS jobs (
                job_id SERIAL PRIMARY KEY,
                job_title VARCHAR(255),
                company_name VARCHAR(255),
                location VARCHAR(255),
                posted_date DATE,
                job_category VARCHAR(100),
                job_apply_url TEXT
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS job_type ( 
                job_type_id SERIAL PRIMARY KEY ,
                job_id INT,
                job_type VARCHAR(100),
                FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            );
        """
    ]

    time.sleep(2)
    try:
        engine_for_tables = sal.create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
        
        with engine_for_tables.begin() as conn:
            for query in create_table_query:
                conn.execute(sal.text(query))

    except Exception as e:
        logging.error(f"An Exception occured while creating Tables: {e}")
    
    else:
        logging.info(f"Tables created successfully")


def load():
    """A Function to load data into tables """

    db_user = os.getenv("DB_USER")
    db_host = os.getenv("DB_HOST")
    db_pass = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    try:
        engine_for_tables = sal.create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
        
        with engine_for_tables.begin() as conn:
            conn.execute(sal.text("DROP TABLE IF EXISTS job_type;"))
            conn.execute(sal.text("DROP TABLE IF EXISTS jobs CASCADE;"))
            
            tables = ["jobs", "job_type"]
            for table in tables:
                file_name = f"CSVs/{table}.csv"
                df = pd.read_csv(file_name)
                df.to_sql(table, conn, if_exists="replace", index=False)

    except Exception as e:
        logging.error(f"An Exception occured while loading data into tables : {e}")
    
    else:
        logging.info(f"Tables loaded successfully")

creating_schema()
load()