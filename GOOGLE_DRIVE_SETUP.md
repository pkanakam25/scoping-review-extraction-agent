# Google Drive Automated PDF Download Setup

## Overview

Fully automated PDF download from Google Drive. Your workflow:

```
You upload PDF to Google Drive
    ↓ (Daily at 8 AM UTC)
GitHub Actions triggers
    ↓
Automatically downloads from Google Drive
    ↓
Extracts 24 fields
    ↓
Updates Google Sheets
    ↓
Done! ✅
```

---

## **Step 1: Create Google Drive Folder**

1. Go to https://drive.google.com
2. Click **+ New** → **Folder**
3. Name it: `Academic Papers - Scoping Review`
4. Click **Create**
5. Open the folder
6. Copy the **Folder ID** from the URL:
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
   ```
   Everything after `/folders/` is your folder ID

**Save your Folder ID!** You'll need it in the next step.

---

## **Step 2: Share Folder with Service Account**

1. In Google Drive, right-click your folder → **Share**
2. Copy this email (from your JSON credentials file):
   ```
   scoping-review-bot@scoping-review-extraction.iam.gserviceaccount.com
   ```
3. Paste it into the share dialog
4. Give **Editor** access
5. Click **Share**

✅ Service account now has access to download PDFs

---

## **Step 3: Add Folder ID to GitHub Secrets**

1. Go to your GitHub repo: https://github.com/pkanakam25/scoping-review-extraction-agent
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Fill in:
   - **Name:** `GOOGLE_DRIVE_FOLDER_ID`
   - **Value:** (Your folder ID from Step 1)
5. Click **Add secret**

✅ GitHub now knows which Google Drive folder to check

---

## **Step 4: Update Code and Push**

The code is already updated to use Google Drive. Just commit:

```bash
git add -A
git commit -m "Switch to Google Drive for automatic PDF download"
git push
```

---

## **Step 5: Test Locally**

First, test that it works locally:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the download script
python3 scripts/download_from_onedrive.py
```

Expected output:
```
✓ Connecting to Google Drive...
✓ Found X PDF(s) in Google Drive
✓ Downloaded X new PDF(s)
```

---

## **Step 6: Test on GitHub Actions**

1. Go to your GitHub repo → **Actions**
2. Click **Daily PDF Extraction**
3. Click **Run workflow**
4. Click **Run workflow** again
5. Wait 2-3 minutes
6. Check logs for:
   ```
   ✓ Downloaded X PDF(s)
   ✓ Successfully synced X rows to Google Sheets
   ```

✅ Check your Google Sheet for the extracted data!

---

## **How to Use - Ongoing**

Once set up, using the system is simple:

### **To add new papers:**

1. Upload PDFs to your Google Drive folder:
   ```
   Google Drive → Academic Papers - Scoping Review → Upload PDFs
   ```

2. Either:
   - **Wait for daily run** (8 AM UTC) 
   - **OR manually trigger** GitHub Actions → Run workflow

3. **Check Google Sheet** for extracted data in ~2-3 minutes

---

## **Your Google Drive Folder Structure**

```
Google Drive
└── Academic Papers - Scoping Review/
    ├── Paper1.pdf
    ├── Paper2.pdf
    ├── Paper3.pdf
    └── ... (add more PDFs here)
```

---

## **What Gets Extracted**

For each PDF, the system extracts 24 fields:

| Field | Example |
|-------|---------|
| S.No. | 1, 2, 3... |
| Author(s) | Smith et al. |
| Country/Location | UK |
| Title | Title of the paper |
| Year | 2023 |
| Study Design | Randomized controlled trial |
| Methodology | Detailed methods... |
| Population | n=100 participants |
| Key Findings | Main results... |
| ... | (and 14 more fields) |

---

## **How GitHub Actions Tracks Progress**

The system creates a file: `processed_files.json`

```json
{
  "processed_files": [
    "Paper1.pdf",
    "Paper2.pdf",
    "Paper3.pdf"
  ]
}
```

This prevents the same PDF from being processed twice.

---

## **GitHub Secrets You Need**

Your GitHub repo should have these 5 secrets:

```
✅ ANTHROPIC_API_KEY
✅ GOOGLE_CLOUD_CREDENTIALS
✅ GOOGLE_DRIVE_FOLDER_ID          ← NEW
✅ GOOGLE_SHEET_ID
✅ (ONEDRIVE_FOLDER_URL - can be deleted)
```

---

## **Daily Schedule**

GitHub Actions runs automatically every day at **8 AM UTC**.

To change the time, edit: `.github/workflows/extract.yml`

```yaml
schedule:
  - cron: '0 8 * * *'  # Change these numbers
```

Common examples:
- `'0 9 * * *'` = 9 AM UTC
- `'0 14 * * *'` = 2 PM UTC
- `'30 8 * * 1-5'` = 8:30 AM UTC, weekdays only

---

## **Troubleshooting**

### "Can't access Google Drive folder"

- Verify folder ID is correct (check URL in Google Drive)
- Verify service account is shared with Editor access
- Wait 5 minutes for sharing permissions to propagate

### "Downloaded 0 PDFs"

- Check that PDFs are in the Google Drive folder
- Make sure they're actually PDFs (not images)
- Verify folder path in GitHub Secrets

### "GitHub Actions fails"

- Check logs: GitHub → Actions → Latest run → Expand step logs
- Look for error messages
- Verify all GitHub Secrets are present and correct

### "Google Sheet doesn't update"

- Check that service account is shared with Editor access to the sheet
- Verify GOOGLE_SHEET_ID is correct
- Check GitHub Actions logs for upload errors

---

## **Security & Privacy**

✅ **Service Account:** Limited to file read/write only  
✅ **No passwords stored:** Uses OAuth credentials  
✅ **GitHub Secrets:** All credentials encrypted  
✅ **.gitignore:** Sensitive files never in code  
✅ **Audit trail:** All actions logged in GitHub  

---

## **What's Happening Behind the Scenes**

When GitHub Actions runs:

1. **Authenticate** with Google using service account
2. **List files** in your Google Drive folder
3. **Filter** for PDFs not yet processed
4. **Download** new PDFs to `./Academic Papers/`
5. **Extract** all 24 fields using NLP
6. **Authenticate** with Google Sheets
7. **Upload** results to your spreadsheet
8. **Record** processed filenames (to avoid re-processing)

All done automatically! ✅

---

## **Next Steps**

1. ✅ Create Google Drive folder
2. ✅ Share with service account
3. ✅ Add GOOGLE_DRIVE_FOLDER_ID to GitHub Secrets
4. ✅ Commit code changes
5. ✅ Test locally: `python3 scripts/download_from_onedrive.py`
6. ✅ Test on GitHub Actions
7. ✅ Upload PDFs to Google Drive
8. ✅ Watch the magic happen! ✨

---

## **You're all set!**

Your scoping review extraction system is now fully automated with Google Drive! 🎉

**Questions?** Check this guide or GitHub Actions logs.
