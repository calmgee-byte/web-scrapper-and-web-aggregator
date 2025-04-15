import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import schedule
import time
import os
from datetime import datetime

# Setup logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://vacancymail.co.zw/jobs/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_FILE = os.path.join(os.getcwd(), 'scraped_data.csv')

def scrape_jobs():
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        job_titles = soup.find_all("h3", class_="job-listing-title")[:10]
        print(f"Found {len(job_titles)} job listings.")

        for title_tag in job_titles:
            container = title_tag.find_parent("div", class_="job-listing-details")

            title = title_tag.get_text(strip=True)
            company_tag = container.find("h4", class_="job-listing-company")
            description_tag = container.find("p", class_="job-listing-text")
            location_li = container.find("li", text=lambda x: x and "Harare" in x)
            expiry_li = container.find("li", text=lambda x: x and "Expires" in x)

            job_data = {
                "Job Title": title,
                "Company": company_tag.get_text(strip=True) if company_tag else "N/A",
                "Location": location_li.get_text(strip=True) if location_li else "N/A",
                "Expiry Date": expiry_li.get_text(strip=True) if expiry_li else "N/A",
                "Description": description_tag.get_text(strip=True) if description_tag else "N/A",
                "Scraped At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(f"\n{job_data['Job Title']} | {job_data['Company']} | {job_data['Location']} | {job_data['Expiry Date']}")
            print(f"Description: {job_data['Description']}")
            print(f"Scraped At: {job_data['Scraped At']}")

            jobs.append(job_data)

        logging.info("Successfully scraped job data.")
        return jobs

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        print("❌ Request error:", e)
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("❌ Unexpected error:", e)
        return []

def clean_and_store_data(jobs):
    try:
        df = pd.DataFrame(jobs, columns=["Job Title", "Company", "Location", "Expiry Date", "Description", "Scraped At"])
        df.drop_duplicates(subset=["Job Title", "Company"], inplace=True)  # Prevent duplicates
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Data successfully saved to {OUTPUT_FILE}")
        print(f"✅ CSV saved with {len(df)} entries at {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Error while saving data: {e}")
        print("❌ Error saving data:", e)

def scheduled_task():
    jobs = scrape_jobs()
    if jobs:
        clean_and_store_data(jobs)

# Run immediately once when script starts
print("Scraper is running every 24 hours...")
scheduled_task()

# Schedule the scraper to run every 24 hours
schedule.every(24).hours.do(scheduled_task)

if __name__ == "__main__":
    logging.info("Web scraper started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
