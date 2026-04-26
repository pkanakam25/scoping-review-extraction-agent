# GitHub Actions + Cloud Setup Guide

This guide walks you through setting up automated daily PDF extraction with GitHub Actions, OneDrive, and Google Cloud.

## Architecture

```
GitHub Actions (daily trigger)
    ↓
Download PDFs from OneDrive
    ↓
Run extraction agent
    ↓
Upload Excel results to Google Sheets
```

---

## Step 1: Initialize GitHub Repository

```bash
cd /path/to/scoping-review-extraction-agent
git init
git add .
git commit -m "Initial commit: scoping review extraction agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scoping-review-extraction-agent.git
git push -u origin main
```

---

## Step 2: Set Up OneDrive Integration

### Option A: OneDrive Public Folder (Simple)

1. Create a folder in your OneDrive (e.g., "Scoping Review PDFs")
2. Right-click → Share → Get a link
3. Copy the public link
4. Add to GitHub Secrets (see Step 4)

### Option B: OneDrive with Microsoft Graph API (Advanced)

For programmatic access:

1. Go to [Azure Portal](https://portal.azure.com)
2. Create an App Registration:
   - App registrations → New registration
   - Name: "Scoping Review Extraction"
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: `https://localhost`
3. Get credentials:
   - Client ID (Application ID)
   - Client Secret (create a new one)
4. Grant API permissions:
   - API permissions → Add → Microsoft Graph
   - Delegated permissions: `Files.Read.All`, `Files.ReadWrite.All`
5. Store credentials securely in GitHub Secrets

**Recommended:** Use Option A (public link) for simplicity.

---

## Step 3: Set Up Google Cloud / Google Sheets

### Option A: Google Sheets (Recommended - Free)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project: "Scoping Review Extraction"
3. Enable APIs:
   - Go to APIs & Services → Library
   - Enable "Google Sheets API"
   - Enable "Google Drive API"
4. Create a Service Account:
   - APIs & Services → Credentials
   - Create → Service Account
   - Fill in details and create
5. Create a key:
   - Click the service account
   - Keys → Add Key → Create new JSON key
   - **Download and save securely**
6. Create a Google Sheet:
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new blank spreadsheet
   - Name it "Scoping Review Extraction Results"
   - Share it with the service account email (from the JSON key)
   - Copy the Sheet ID from the URL (the long alphanumeric string)

### Option B: Google Cloud Storage

If you prefer to store the Excel file in cloud storage:

1. Enable "Cloud Storage" API
2. Create a bucket: `gs://scoping-review-extraction`
3. Service account automatically gets access

---

## Step 4: Add GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add the following secrets:

| Secret Name | Value | Source |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | https://console.anthropic.com |
| `ONEDRIVE_FOLDER_URL` | Public OneDrive folder link | OneDrive share link (Step 2) |
| `GOOGLE_SHEET_ID` | Google Sheet ID | Google Sheets URL |
| `GOOGLE_CLOUD_CREDENTIALS` | JSON credentials content | Download from Step 3 |

**To add `GOOGLE_CLOUD_CREDENTIALS`:**
1. Open the downloaded JSON key file
2. Copy the entire contents
3. Paste into GitHub Secrets as a single-line JSON string

---

## Step 5: Customize GitHub Actions Schedule

Edit `.github/workflows/extract.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Daily at 8 AM UTC
```

Common cron patterns:
- `0 8 * * *` = Daily at 8 AM UTC
- `0 8 * * 1-5` = Weekdays at 8 AM UTC
- `0 */6 * * *` = Every 6 hours
- Use [crontab.guru](https://crontab.guru) to verify

---

## Step 6: First Test Run

1. Go to GitHub Actions tab
2. Select "Daily PDF Extraction" workflow
3. Click "Run workflow" → "Run workflow" (manual trigger)
4. Monitor the logs
5. Check Google Sheets for results

---

## Troubleshooting

### GitHub Actions workflow fails

Check logs:
1. GitHub repo → Actions → Latest run
2. Click the failed job
3. Expand each step to see error messages

### PDFs not downloading from OneDrive

- Verify `ONEDRIVE_FOLDER_URL` is correct
- Check if the link is still public
- Alternatively, use Microsoft Graph API (Option B)

### Google Sheets not updating

- Verify `GOOGLE_SHEET_ID` is correct
- Check if service account email has access to the sheet
- Verify JSON credentials are in GitHub Secrets correctly

### Anthropic API errors

- Check `ANTHROPIC_API_KEY` is correct
- Verify account has available credit
- Check API usage at https://console.anthropic.com/account/usage

---

## Manual Workflow (without GitHub Actions)

If you want to run locally:

```bash
# Download from OneDrive (if available)
python scripts/download_from_onedrive.py

# Run extraction
python scoping_review_agent.py

# Upload to Google Sheets
python scripts/upload_to_google_cloud.py
```

---

## Security Best Practices

1. **Never commit secrets** - Always use GitHub Secrets
2. **Rotate keys** - Regenerate service account keys periodically
3. **Limit permissions** - Service account should only have access to specific bucket/sheet
4. **Use public OneDrive link** - Don't expose OAuth tokens in workflows
5. **Monitor usage** - Check API quotas and costs regularly

---

## Next Steps

1. Set up all secrets in GitHub
2. Test the workflow manually
3. Monitor the first automated run
4. Adjust cron schedule if needed
5. Set up alerts if extraction fails

For questions, check the logs in GitHub Actions!
