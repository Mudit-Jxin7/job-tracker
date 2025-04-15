# Job Tracker

A Python-based job tracker that periodically scrapes job listings from multiple job portals and logs the new listings in a Google Sheet. The tracker sends an email notification whenever new jobs matching specific keywords are found.

---

## Features
- Scrapes job listings for specific roles (e.g., Software Engineer) from websites like Google, Adobe, and Expedia.
- Sends email notifications when new job listings are found.
- Logs new job listings in a Google Sheet for easy tracking.
- Runs periodically (every 12 hours) via GitHub Actions.

---

## Prerequisites
Before you begin, make sure you have the following:
- A **Google Sheets** account and a **Google Sheet** for logging job listings.
- A **Google Cloud project** with the **Google Sheets API** enabled.
- **Python 3.10+** installed locally or in a virtual environment.
- Access to **Gmail** for sending email notifications.
- A **GitHub account** to deploy the project using GitHub Actions (optional).

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/job-tracker.git
cd job-tracker
```

### 2. Install Dependencies

Create a virtual environment and activate it, then install the required dependencies.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root of the repository and add the following variables:

```ini
# Email settings
EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-email-app-password

# Google Sheets settings
SHEET_NAME=Your-Sheet-Name
SHEET_URL=Your-Sheet-URL
```

### 4. Set Up Google Sheets API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Sheets API**.
3. Create a **Service Account** in your project and download the **JSON key file**.
4. Rename the downloaded file to `creds.json` and place it in the root of the project.

### 5. Set Up GitHub Secrets (For GitHub Actions)

To securely store your sensitive information (like email credentials and Google Sheets credentials) in GitHub, follow these steps:

1. Navigate to your repository on GitHub.
2. Go to **Settings** > **Secrets** > **New repository secret**.
3. Add the following secrets:
   - `EMAIL`: Your email address.
   - `EMAIL_PASSWORD`: Your email app password (for Gmail).
   - `SHEET_NAME`: The name of your Google Sheet.
   - `SHEET_URL`: The URL of your Google Sheet.
   - `GOOGLE_CREDS`: The base64-encoded contents of your `creds.json` file (use `base64 creds.json` to encode it).

---

## Running Locally

You can run the script locally by executing the following:

```bash
python job_tracker.py
```

This will:
1. Fetch job listings from the URLs specified in `URLS_TO_MONITOR`.
2. Filter the jobs based on the `KEYWORDS` list.
3. Save new job listings to the Google Sheet.
4. Send an email notification with the details of the new listings.

---

## Deploying with GitHub Actions

To automate the process and run the script every 12 hours, GitHub Actions is used. This is set up via the `.github/workflows/job-tracker.yml` file. The cron job in the workflow runs the script every 12 hours.

Here’s the README section you can use to inform other users on how to fork the repository and run the GitHub Actions workflow:

---

## Automating Job Tracker with GitHub Actions

To automate the process of checking for new jobs, we use **GitHub Actions**. The workflow is configured to run the job tracker script every **12 hours** automatically using a cron job.

### Steps to Run the Job Tracker Automatically:

1. **Fork the repository**:
   - Click the **Fork** button on the top-right corner of this repository to create a copy of the repository under your GitHub account.

2. **Set up your GitHub secrets**:
   - Navigate to your forked repository on GitHub.
   - Go to **Settings** > **Secrets** > **New repository secret**.
   - Add the following secrets:
     - **`EMAIL`**: Your email address to receive job notifications.
     - **`EMAIL_PASSWORD`**: Your email app password (use Gmail app-specific password).
     - **`SHEET_NAME`**: The name of the Google Sheet where job data will be stored.
     - **`SHEET_URL`**: The URL of the Google Sheet.
     - **`GOOGLE_CREDS`**: Your **base64-encoded** Google credentials file (`creds.json`). You can generate this by running `base64 creds.json`.

3. **Check your Google Sheets**: After configuring your secrets, the workflow will run every 12 hours and will automatically check for new jobs. The job data will be saved to your Google Sheet, and you'll receive an email with details of the new jobs found.

4. **No manual execution required**: Once the secrets are set up, the GitHub Actions workflow will run automatically whenever:
   - There's a push to the `main` branch.
   - Or the cron job triggers every 12 hours.

This will automatically run the script every 12 hours and save any new job listings to your Google Sheets and send you an email notification.

---

## Troubleshooting

- **Email issues**: Make sure you are using an app password if using Gmail and have allowed "less secure apps" or enabled 2FA with app-specific passwords.
- **Google Sheets API issues**: Ensure that the `creds.json` file has been set up correctly and the Google Sheet is shared with the service account email.
- **Job not found**: Check if the URLs and keywords are set correctly and the job portals haven't changed their layout.

---
## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

---
