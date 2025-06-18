import requests
from bs4 import BeautifulSoup
import datetime
import sqlalchemy as sal
import pandas as pd
import logging
import os

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


def searchingData(divIdContent, pgNo):
    """
    Search for relevant data in the provided div content.

    Parameters
    ----------
    divIdContent : BeautifulSoup
        Parsed HTML content of the div identified by ID.

    pgNo : int
        Page number used for pagination.
    """

    logging.info(f"Searching for relevant data in pg : {pgNo}")
    content = divIdContent.find("div", class_="row")
    job_details = content.find("ol", class_="list-recent-jobs list-row-container menu")
    job_details = job_details.find_all("li")
    
    data_frame = pd.DataFrame(columns=["job_title", "company_name", "location", 
                                       "job_type", "posted_date", "job_category", 
                                       "job_apply_full_link"])

    # Extracting relevant info
    for job in job_details:
        job_title = job.find("h2", class_="listing-company").find("span", class_="listing-company-name").find("a").text.strip()
        company_name = job.find("h2", class_="listing-company").find("span", class_="listing-company-name").contents[-1].strip()
        location = job.find("h2", class_="listing-company").find("span", class_="listing-location").find("a").text.strip()
        job_type = [a.text.strip() for a in job.find("span", class_="listing-job-type").find_all("a")]
        posted_str = job.find("span", class_="listing-posted").find("time")["datetime"]
        posted_pretty = job.find("span", class_="listing-posted").find("time").text.strip()
        job_category = job.find("span", class_="listing-company-category").find("a").text.strip()
        job_apply_short_link = job.find("h2", class_="listing-company").find("a")["href"]
        job_apply_full_link = "https://www.python.org" + job_apply_short_link
        posted_date = datetime.datetime.fromisoformat(posted_str).date()

        # Creating new series of the data
        Data_Series = pd.Series({
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "job_type": job_type,
            "posted_date": posted_date,
            "job_category": job_category,
            "job_apply_full_link": job_apply_full_link
        })
        
        # Converting series into dataframe for merging
        Data_Series = Data_Series.to_frame().T

        # concatenating 
        data_frame = pd.concat([data_frame, Data_Series], axis=0, ignore_index=True)

    # Saving dataframe for the current page
    logging.info("Saving data in a csv file")
    
    try:
        # Trying to create a directory and if it exists do nothing (nothing means - don't raise fileExistsException)
        os.makedirs("CSVs", exist_ok=True)
    
        file_name = f"CSVs/pg{pgNo}.csv"
        data_frame.to_csv(file_name, index=False)
    
    except Exception as e:
        logging.error(f"Error saving data in the file {file_name} : {e}")
        return 
    

    # Incrementing pgNo for searching for next page
    pgNo += 1
    if nextPageExists(pgNo):
        URL = f"https://www.python.org/jobs/?page={pgNo}"
        data_extraction(URL, pgNo)
    else:
        logging.info("Overall Search completed.")
        return

    logging.info(f"Searching for relevant data in pg : {pgNo}")


def nextPageExists(pgNo):
    """
    Check if the next page exists.

    Parameters
    ----------
    pgNo : int
        Page number to check.

    Returns
    -------
    bool
        True if the page exists, False otherwise.
    """
    
    logging.info(f"Checking the existence of {pgNo} page")
    
    # New URL to search for 
    URL = f"https://www.python.org/jobs/?page={pgNo}"
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except:
        logging.info(f"pgNo - {pgNo} does not exist, ending the search")
        return False
    else:
        return True


def data_extraction(URL="https://www.python.org/jobs/", pgNo=1):
    """
    Main data_extraction function
    
    Parameters
    ----------
    URL : str
        URL to extract data from
    
    pgNo : int
        Number of the page
    """
    
    logging.info(f"Extracting data for page: {pgNo}")
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"request failed: {e}")
        return
    
    soup = BeautifulSoup(response.content, "html.parser")
    divIdContent = soup.find(id="content")
    
    searchingData(divIdContent, pgNo)

# data_extraction(URL="https://www.python.org/jobs/?page=1", pgNo=1)