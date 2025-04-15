import os
import smtplib
import time
from email.mime.text import MIMEText

import gspread
import requests
import schedule
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SHEET_NAME = os.getenv("SHEET_NAME")
SHEET_URL = os.getenv("SHEET_URL")

# Configure job URLs
URLS_TO_MONITOR = {
    "Google": "https://www.google.com/about/careers/applications/jobs/results/?employment_type=FULL_TIME&company=Google&location=India",
    "Adobe": "https://careers.adobe.com/us/en/search-results?keywords=software%20engineer",
    "Expedia": "https://careers.expediagroup.com/jobs/?keyword=software+engineer&&filter[country]=India",
}

KEYWORDS = ["Software", "engineer"]
last_seen_jobs = {}


# Connect to Google Sheets
def connect_sheet():
    print("📄 Connecting to Google Sheet...")
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SHEET_URL).sheet1
    print("✅ Connected to Google Sheet!")
    return sheet


# Add job to Google Sheets
def save_to_google_sheets(company, title, link):
    print(f"📌 Saving job to sheet: {company} | {title} | {link}")
    sheet = connect_sheet()
    sheet.append_row([company, title, link])
    print("✅ Job saved to Google Sheets.")


# Send notification email
def send_email(subject, content):
    print("📧 Sending email notification...")
    msg = MIMEText(content, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Email failed: {e}")


# Scrape jobs
def fetch_jobs(url):
    print(f"🌐 Fetching jobs from: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        print(f"✅ Successfully fetched HTML from: {url}")
        return BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None


# Extract job title + link
def extract_jobs(soup, base_url, company):
    print(f"🔍 Extracting jobs for {company}...")
    job_entries = []

    for a in soup.find_all("a", href=True):
        link = a["href"]
        text = company

        if any(keyword.lower() in link.lower() for keyword in KEYWORDS):
            if not link.startswith("http"):
                link = base_url + link
            job_entries.append((text, link))

    print(f"📝 Found {len(job_entries)} potential jobs for {company}.")
    return job_entries


# Main logic
def check_jobs():
    global last_seen_jobs
    new_jobs_total = []

    print("🚀 Checking jobs from all companies...\n")
    for company, url in URLS_TO_MONITOR.items():
        soup = fetch_jobs(url)
        if not soup:
            continue
        jobs = extract_jobs(soup, url, company)

        seen = last_seen_jobs.get(company, set())
        new_jobs = [(title, link) for title, link in jobs if title not in seen]

        if new_jobs:
            print(f"✅ {len(new_jobs)} new jobs found for {company}!")
            last_seen_jobs[company] = seen.union({title for title, _ in new_jobs})
            for title, link in new_jobs:
                save_to_google_sheets(company, title, link)
            new_jobs_total.append(
                f"{company}:\n" + "\n".join(f"{t} - {l}" for t, l in new_jobs)
            )
        else:
            print(f"🕵️ No new jobs found for {company}.")

    if new_jobs_total:
        content = "\n\n".join(new_jobs_total)
        send_email("🚨 New SDE Jobs Found!", content)
    else:
        print("📭 No new jobs found across all companies.")

print("📅 Job Tracker started! First check happening now...\n")
check_jobs()
