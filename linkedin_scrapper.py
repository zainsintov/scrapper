import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
from datetime import timedelta
import math


job_titles = []
company_names = []
locations = []
posted_times = []
applicants = []
job_urls = []

jobs_scrapped = 0


def scrap_jobs(item_num, jobs_list):

    total_jobs = len(jobs_list)
    print("total jobs are", total_jobs)
    for x in range(item_num, total_jobs):
        print("Job number", x)
        jobs_list[x].click()
        time.sleep(4)
        section = driver.find_element(By.CLASS_NAME, "top-card-layout__card")

        title = section.find_element(By.TAG_NAME, "h2")

        company = section.find_element(By.CSS_SELECTOR, "span.topcard__flavor")

        location = section.find_element(
            By.CSS_SELECTOR, "span.topcard__flavor.topcard__flavor--bullet")

        time_posted = section.find_element(
            By.CSS_SELECTOR, "span.posted-time-ago__text.topcard__flavor--metadata")

        j_url = driver.current_url
        print("current url is", j_url)

        today = datetime.now()
        ptime = datetime.now()

        number_to_sub = [int(i)
                         for i in time_posted.text if i.isdigit()] or [0]
        number_to_sub = int(number_to_sub[0])

        if "week" in time_posted.text:
            ptime = today - timedelta(weeks=number_to_sub)
        elif "hour" in time_posted.text:
            ptime = today - timedelta(hours=number_to_sub)
        elif "day" in time_posted.text:
            ptime = today - timedelta(days=number_to_sub)
        elif "month" in time_posted.text:
            ptime = today - timedelta(weeks=(number_to_sub * 4))

        applicant = section.find_element(
            By.CLASS_NAME, "num-applicants__caption")

        job_titles.append(title.text.strip())
        company_names.append(company.text.strip())
        locations.append(location.text.strip())
        posted_times.append(ptime.strftime("%d-%m-%y %H:%M"))
        applicants.append(applicant.text.strip())
        job_urls.append(j_url)

        global jobs_scrapped
        jobs_scrapped = x + 1


jobsToBeScrapped = int(
    input("Enter the number you want total jobs to scrapped in multiple of 25: "))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3815344269&f_TPR=r2592000&geoId=103644278&keywords=ios%20developer&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R")


for y in range(math.ceil(jobsToBeScrapped / 25)):
    time.sleep(4)

    btn = driver.find_element(
        By.XPATH, '//*[@id="main-content"]/section[2]/button')

    if btn.is_displayed() and btn.is_enabled():
        print("Button is clickable now")
        btn.click()

    time.sleep(4)

    job_list_element = driver.find_element(
        By.CLASS_NAME, 'jobs-search__results-list')

    list_item_elements = job_list_element.find_elements(By.TAG_NAME, "li")
    print("list item elements in the iteration", y, len(list_item_elements))

    scrap_jobs(jobs_scrapped, list_item_elements)

    df = pd.DataFrame({'Job title': job_titles, 'Company Name': company_names,
                       "Location": locations, "Posted Time": posted_times, "Applicants": applicants, "URL": job_urls})
    df.to_csv('data.csv', index=False, encoding='utf-8')
