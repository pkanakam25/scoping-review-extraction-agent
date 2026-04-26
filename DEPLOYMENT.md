# Deployment Guide - GitHub Actions + OneDrive + Google Sheets

## Overview

Your scoping review extraction agent is now ready for cloud deployment with:
- ✅ Automated daily runs via GitHub Actions
- ✅ PDF input from OneDrive
- ✅ Results stored in Google Sheets
- ✅ Zero manual steps needed after setup

---

## Quick Setup (5 Steps)

### Step 1: Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial: scoping review extraction agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scoping-review-extraction-agent.git
git push -u origin main
```

### Step 2: Add GitHub Secrets

Go to **GitHub Repo → Settings → Secrets and variables → Actions** and add:

| Secret | Value | Source |
|--------|-------|--------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | https://console.anthropic.com |
| `ONEDRIVE_FOLDER_URL` | `https://1drv.ms/...` | OneDrive share link |
| `GOOGLE_SHEET_ID` | Sheet ID from URL | Google Sheets |
| `GOOGLE_CLOUD_CREDENTIALS` | JSON credentials | Google Cloud Console |

**See:** `GITHUB_SECRETS_SETUP.md` for detailed instructions

### Step 3: Create OneDrive Folder
- Create "Academic Papers" folder in OneDrive
- Share it publicly (or use OAuth for private)
- Add the link to GitHub Secrets

### Step 4: Set Up Google Sheet
- Create blank spreadsheet in Google Sheets
- Share with service account (from JSON credentials)
- Copy Sheet ID from URL to GitHub Secrets

### Step 5: Test the Workflow
- Go to **Actions** tab in GitHub
- Click **Daily PDF Extraction**
- Click **Run workflow**
- Monitor logs and verify Google Sheet updates

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                        │
│  (scoping-review-extraction-agent)                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                  ┌─────────────────────┐
                  │  GitHub Actions     │
                  │  (Daily at 8 AM)    │
                  └─────────────────────┘
                            ↓
              ┌─────────────────────────────┐
              │  1. Download PDFs           │
              │     from OneDrive           │
              └─────────────────────────────┘
                            ↓
              ┌─────────────────────────────┐
              │  2. Run Extraction Agent    │
              │     (24-field extraction)   │
              └─────────────────────────────┘
                            ↓
              ┌─────────────────────────────┐
              │  3. Upload to Google Sheets │
              │     (Results saved)         │
              └─────────────────────────────┘
```

---

## Files Created

```
.github/
  workflows/
    extract.yml              # GitHub Actions workflow (daily trigger)

scripts/
  download_from_onedrive.py  # Download PDFs from OneDrive
  upload_to_google_cloud.py  # Upload results to Google Sheets

.gitignore                   # Excludes local data, PDFs, Excel files

requirements.txt             # Updated with Google Cloud dependencies

Documentation:
  GITHUB_ACTIONS_SETUP.md    # Detailed setup guide
  GITHUB_SECRETS_SETUP.md    # GitHub Secrets quick reference
  DEPLOYMENT.md              # This file
```

---

## Workflow File Breakdown

**`.github/workflows/extract.yml`**

```yaml
schedule:
  - cron: '0 8 * * *'        # Runs daily at 8 AM UTC
```

Customize the time:
- `0 8 * * *` = Daily 8 AM
- `0 8 * * 1-5` = Weekdays only
- `0 */6 * * *` = Every 6 hours

Use [crontab.guru](https://crontab.guru) to verify cron expression.

---

## Data Flow

### Input (OneDrive)
```
OneDrive/Academic Papers/
  ├── Paper1.pdf
  ├── Paper2.pdf
  └── Paper3.pdf
```

### Processing (GitHub Actions)
1. Download PDFs from OneDrive
2. Extract text using pdfplumber
3. Parse 24 fields using local NLP:
   - S.No., Authors, Country, Title
   - Publication details, Study design
   - Methodology, Population, Setting
   - Results, Findings, Barriers, Funding
   - ... and 11 more fields

### Output (Google Sheets)
```
Google Sheet "Scoping Review Extraction Results"
┌─────┬──────────┬─────────┬────────┬─────────────┬──────┐
│ No. │ Authors  │ Country │ Title  │ Year │ Findings │ ...  │
├─────┼──────────┼─────────┼────────┼──────┼──────────┼──────┤
│  1  │ Smith J  │ UK      │ Title1 │ 2023 │ Finding1 │ ...  │
│  2  │ Jones A  │ USA     │ Title2 │ 2024 │ Finding2 │ ...  │
└─────┴──────────┴─────────┴────────┴──────┴──────────┴──────┘
```

---

## Daily Workflow Schedule

Your workflow will run **every day at 8 AM UTC** (or your configured time):

1. **GitHub Actions** detects scheduled trigger
2. **Spins up Ubuntu runner** with Python 3.10
3. **Downloads latest PDFs** from OneDrive
4. **Runs extraction agent** on new PDFs
5. **Uploads results** to Google Sheets
6. **Logs execution** for monitoring

---

## Monitoring & Logging

### GitHub Actions Logs
- Go to **Actions** tab in GitHub
- Click **Daily PDF Extraction**
- View logs for each run
- Check for errors in step outputs

### Google Sheets
- Your sheet updates automatically after each run
- New rows appended with extracted data
- Check last row for most recent extraction

### Local Logs (in workflow)
Last 20 lines of `extraction_agent.log` printed at end of each run

---

## Customization

### Change Extraction Schedule
Edit `.github/workflows/extract.yml`:
```yaml
schedule:
  - cron: '0 8 * * 1-5'  # Weekdays only
```

### Change Extraction Time
```yaml
schedule:
  - cron: '30 14 * * *'  # 2:30 PM UTC instead of 8 AM
```

### Add Manual Trigger
Already included! Go to **Actions → Daily PDF Extraction → Run workflow**

### Add Slack/Email Notifications
Add step to workflow:
```yaml
- name: Notify on failure
  if: failure()
  run: |
    # Send email or Slack message
```

---

## Costs

### Google Cloud (FREE tier covers your needs)
- Google Sheets API: **Free** (unlimited reads/writes to 1 sheet)
- Google Drive API: **Free** (part of free tier)
- Service account: **Free**

### GitHub Actions
- **Free** for public repos
- 2,000 minutes/month free for private repos
- Daily run = ~30 min/month (well under limit)

### OneDrive
- **Free** (1TB Microsoft 365 account)
- Public sharing: **Free**

### Anthropic API
- **Pay-as-you-go** (~$0.01-0.05 per paper)
- Free tier available at sign-up

**Total monthly cost: ~$1-2** (only for API usage)

---

## Troubleshooting

### Workflow doesn't run at scheduled time
- GitHub Actions may have slight delay (5-10 min)
- Check GitHub Status page
- Verify cron expression on [crontab.guru](https://crontab.guru)

### PDFs not downloading
- Verify OneDrive link is public
- Check `ONEDRIVE_FOLDER_URL` secret
- Ensure PDFs are in the shared folder

### Google Sheets not updating
- Verify service account email is shared with **Editor** access
- Check `GOOGLE_SHEET_ID` is correct
- Verify JSON credentials in `GOOGLE_CLOUD_CREDENTIALS`

### Extraction fails
- Check GitHub Actions logs for error messages
- Verify `ANTHROPIC_API_KEY` has available credits
- Check Anthropic account at https://console.anthropic.com

---

## Security Checklist

- [ ] No secrets committed to repository
- [ ] `.gitignore` includes PDFs and Excel files
- [ ] GitHub Secrets are set (not in code)
- [ ] OneDrive link is intentionally public
- [ ] Google service account has minimal permissions
- [ ] Credentials file is secure (not in repo)

---

## Next Steps

1. **Set up GitHub repository** (push code to GitHub)
2. **Create GitHub Secrets** (follow `GITHUB_SECRETS_SETUP.md`)
3. **Test manually** (GitHub Actions → Run workflow)
4. **Monitor first run** (check logs and Google Sheet)
5. **Adjust schedule if needed** (edit cron in `.yml`)
6. **Let it run!** (fully automated from day 2)

---

## Support

- **GitHub Actions docs:** https://docs.github.com/en/actions
- **Google Sheets API:** https://developers.google.com/sheets/api
- **OneDrive sharing:** https://support.microsoft.com/en-us/office
- **Anthropic API:** https://docs.anthropic.com

---

**Your extraction agent is production-ready! 🚀**

Questions? Check the detailed guides:
- `GITHUB_ACTIONS_SETUP.md` - Full setup instructions
- `GITHUB_SECRETS_SETUP.md` - Secret management
