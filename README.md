# Site Monitoring with Selenium Python + SMS Notifications (Twilio)

This project uses GitHub Actions to monitor a website twice daily using Selenium Python. It performs a search on the target page, checks the target locator value, compares it with the previous run, and sends an SMS using Twilio if there's a change.

## File Structure

```
site-monitoring-sms/
├── .github/
│   └── workflows/
│       └── check-site.yml       # GitHub Actions workflow
├── results/
│   └── past_results.json        # Persisted result data (managed by artifact)
├── src/
│   ├── check.py                 # Main script for Selenium search and comparison
│   └── notify.py                # Twilio SMS integration
├── requirements.txt
├── .env                         # Environment variables (local use only)
```

## Tech Stack

- Python + Selenium
- Twilio for SMS
- GitHub Actions for automation

## Getting Started

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add a `.env` file (for local testing only)

```env
TARGET_URL=https://example.com
RESULT_SELECTOR=result-item
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1xxxxxxx
TWILIO_TO_NUMBER=+1yyyyyyy
```

### 3. Test Locally

```bash
python src/check.py
```

## Required GitHub Secrets

Set these under your repository's **Settings > Secrets and variables > Actions**:

- `TARGET_URL`
- `RESULT_SELECTOR`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`
- `TWILIO_TO_NUMBER`

## GitHub Action Schedule

The job is configured to run **twice daily**:

```yaml
on:
  schedule:
    - cron: "0 6 * * *" # 06:00 UTC
    - cron: "0 18 * * *" # 18:00 UTC
```

You can modify the schedule in `.github/workflows/check-site.yml`.

## Future Enhancements & Ideas

Here are some ways to expand the project:

### Monitoring Scope

- Monitor multiple websites or APIs.
- Check for text presence or specific element content.

### Notification Options

- Add support for Slack, Discord, Telegram, or email.
- Create daily summaries instead of instant alerts.

### Result Intelligence

- Store a full list of result data, not just count.
- Add diff comparisons and historical graphs.

### Dashboard & APIs

- Build a simple dashboard UI to display trends.
- Add user triggers for manual re-checks.

### Backend/Data Layer

- Use a real database (SQLite/PostgreSQL).
- Store result history per target and visualize it.
