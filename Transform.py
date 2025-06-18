import pandas as pd
import logging
import os
import ast

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


def merge_all_CSVs():
    """ 
    A function to merge all csv data in one file
    
    Parameters
    ----------
    None

    Returns
    --------
    None
    """

    directory = "CSVs"

    logging.info("Merging all CSVs")

    # Getting all file names 
    all_files = [f"{directory}/{file}" for file in os.listdir(directory) if file.startswith("pg")]
    
    # Concatenating them
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    
    # Renaming and shifting(we want job_id to start from 1, not 0) index to 1
    df.index.name = "job_id"
    df.index = df.index + 1

    # Saving all in new file
    df.to_csv("CSVs/merged_jobs.csv", index=True)

    logging.info("Merging successful")


def separatingData():
    """
    A function to separate data for two tables

    Parameters
    -------
    None

    Returns
    --------
    None
    """

    logging.info("Separating jobs and job_type data....")

    df = pd.read_csv("CSVs/merged_jobs.csv")

    # For jobs table 
    jobs_df = df.drop("job_type", axis=1).copy()

    # Saving jobs_df in a file 
    jobs_df.to_csv("CSVs/jobs.csv", index=False)

    # Creating job type data 
    job_type_df = df[["job_id", "job_type"]].copy()

    # Convert stringified lists to actual lists
    job_type_df["job_type"] = job_type_df["job_type"].apply(ast.literal_eval)

    # Explode the job_type column
    job_type_df = job_type_df.explode('job_type').reset_index(drop=True)

    # Removing whitespaces
    job_type_df["job_type"] = job_type_df["job_type"].str.strip()
    
    # Saving jobs_type_df in a file
    job_type_df.to_csv("CSVs/job_type.csv", index=False)

    logging.info("Separating jobs and job_type data successful")