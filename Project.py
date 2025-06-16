import requests
from bs4 import BeautifulSoup
import datetime


def display_info(job_title, company_name, location_list, job_type, posted_date_pretty, job_apply_full_link):
    print("Job Info")
    print(f"Title         : {job_title}")
    print(f"Company name  : {company_name}")
    print(f"Locations     : {', '.join(location_list)}")
    print(f"Date posted   : {posted_date_pretty}")
    print(f"Apply link    : {job_apply_full_link}")
    print("-" * 40)


def searchingData(divIdContent, pgNo, user_location, user_posted_within):
    content = divIdContent.find("div", class_="row")
    job_details = content.find("ol", class_="list-recent-jobs list-row-container menu")
    job_details = job_details.find_all("li")

    job_count = 0
    today = datetime.datetime.now().date()
    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)

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

        if user_location.lower() in location.lower():
            if user_posted_within == 1 and posted_date == today:
                job_count += 1
                print(f"Details for job {job_count} on page {pgNo}:")
                display_info(job_title, company_name, location.split(","), job_type, posted_pretty, job_apply_full_link)
            elif user_posted_within == 2 and posted_date >= week_ago:
                job_count += 1
                print(f"Details for job {job_count} on page {pgNo}:")
                display_info(job_title, company_name, location.split(","), job_type, posted_pretty, job_apply_full_link)
            elif user_posted_within == 3 and posted_date >= month_ago:
                job_count += 1
                print(f"Details for job {job_count} on page {pgNo}:")
                display_info(job_title, company_name, location.split(","), job_type, posted_pretty, job_apply_full_link)

    if job_count == 0:
        print(f"No jobs found on page {pgNo} for given location and date filter.")
    else:
        print(f"Total {job_count} jobs found on page {pgNo}.")

    pgNo += 1
    if nextPageExists(pgNo):
        print("\n--- Searching next page ---\n")
        URL = f"https://www.python.org/jobs/?page={pgNo}"
        data_extraction(user_location, user_posted_within, URL, pgNo)
    else:
        print("Search completed.")


def nextPageExists(pgNo):
    URL = f"https://www.python.org/jobs/?page={pgNo}"
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except:
        return False
    else:
        return True


def data_extraction(user_location, user_posted_within, URL="https://www.python.org/jobs/", pgNo=1):
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return
    soup = BeautifulSoup(response.content, "html.parser")
    divIdContent = soup.find(id="content")
    searchingData(divIdContent, pgNo, user_location, user_posted_within)


def Main_func():
    user_location = input("Enter location you want to work in: ").strip()
    user_posted_within = int(input("Enter posted within:\n1 = Day\n2 = Week\n3 = Month\nChoice: "))
    URL = "https://www.python.org/jobs/?page=1"
    data_extraction(user_location, user_posted_within, URL, pgNo=1)


if __name__ == "__main__":
    Main_func()
