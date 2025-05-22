#  EventWisher

EventWisher is a Python automation script that event wishes via email using data from a Google Sheet. It is scheduled to run daily using GitHub Actions.

## To run it on local:
### Clone the Repository

Open your terminal and run the following commands:

```bash
git clone https://github.com/ayushjha2612/EventWisher.git
cd EventWisher
```
### Create a Virtual Environment

To keep dependencies isolated, create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
### Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```
### Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API
4. Go to **APIs & Services → Credentials**
5. Click **"Create Credentials" → "Service Account"**
6. After creation:
   - Note the **Service Account Email**
   - Click **"Add Key" → "Create new key" → JSON**
   - Download the JSON key file and place it in your project directory as `service_account.json`
7. Share your Google Sheet with the **Service Account Email** (with Editor access)

 This allows your script to access the sheet securely.
 ### Set Up Environment Variables (for Email)

Create a `.env` file in your project root (or set environment variables manually) with the following content:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_app_password
```
### Run the Script

Make sure your virtual environment is activated and all environment variables are set.

Run the script with:

```bash
python main.py
```
### (Optional) Schedule with GitHub Actions

To automate sending emails daily, set up a GitHub Actions workflow:

1. Add a `.github/workflows/scheduler.yml` file in your repo with a cron schedule.
2. Make sure your GitHub repository secrets include:
   - `EMAIL_USER`
   - `EMAIL_PASS`
   - `SERVICE_JSON` (your service account JSON contents)

The workflow will run the script automatically at the scheduled time every day.

---

You can manually trigger the workflow from the GitHub Actions tab as well.
