#  VacancyMail Job Scraper & Logger

A robust Python project that scrapes the latest job listings from [VacancyMail Zimbabwe](https://vacancymail.co.zw/jobs/), extracts key information, logs all events, and stores the data in a structured CSV format. Designed for automation, the script runs every 24 hours using Python's `schedule` module.

---

## 🎯 Project Purpose

The Zimbabwean job market is dynamic and competitive. This script was created to help individuals and organizations:

- 🧠 Stay updated on the latest job opportunities
- 📈 Monitor job trends over time
- 🗃️ Build datasets for analysis and career planning
- ⚙️ Automate job board monitoring to save time

---

## 🔍 Features

- ✅ Scrapes the 10 most recent job listings from VacancyMail
- ✅ Extracts:
  - Job Title
  - Company Name
  - Location (e.g., Harare)
  - Expiry Date
  - Job Description
  - Scrape Timestamp
- ✅ Saves structured data to a CSV file: `scraped_data.csv`
- ✅ Automatically filters out duplicate entries
- ✅ Logs activity and errors to a dedicated log file: `scraper.log`
- ✅ Auto-runs the scraper every 24 hours using `schedule`
- ✅ Displays scraped results live in the terminal for transparency

---

## 📁 File & Folder Structure

