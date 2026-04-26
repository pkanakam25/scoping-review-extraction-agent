# GitHub Secrets Setup - Quick Reference

## Where to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret**

---

## Required Secrets

### 1. ANTHROPIC_API_KEY

**What:** Your Anthropic API key for Claude AI

**How to get:**
1. Go to https://console.anthropic.com
2. Navigate to **API Keys**
3. Create a new API key
4. Copy the key (starts with `sk-ant-`)

**Add to GitHub:**
- Name: `ANTHROPIC_API_KEY`
- Secret: `sk-ant-xxxxxxxxxxxxx`

---

### 2. ONEDRIVE_FOLDER_URL

**What:** Public link to your OneDrive folder with PDFs

**How to get:**
1. Go to OneDrive
2. Create/navigate to your "Academic Papers" folder
3. Right-click → **Share**
4. Select **Anyone with the link can view**
5. Copy the link

**Add to GitHub:**
- Name: `ONEDRIVE_FOLDER_URL`
- Secret: `https://1drv.ms/f/s!xxxxxxx`

---

### 3. GOOGLE_SHEET_ID

**What:** ID of your Google Sheet where results will be stored

**How to get:**
1. Go to https://sheets.google.com
2. Create a new blank spreadsheet
3. Name it "Scoping Review Results"
4. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID_HERE]/edit
   ```

**Add to GitHub:**
- Name: `GOOGLE_SHEET_ID`
- Secret: `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

---

### 4. GOOGLE_CLOUD_CREDENTIALS

**What:** JSON credentials for Google Cloud service account

**How to get:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select or create a project: "Scoping Review Extraction"
3. Enable APIs:
   - Search for "Google Sheets API" → Enable
   - Search for "Google Drive API" → Enable
4. Create Service Account:
   - Go to **APIs & Services** → **Credentials**
   - Click **+ Create Credentials** → **Service Account**
   - Fill in: Name = "scoping-review-bot"
   - Create and continue (skip optional steps)
5. Create a Key:
   - Click the service account you created
   - Go to **Keys** tab
   - Click **Add Key** → **Create new key**
   - Choose **JSON**
   - A file will download automatically
6. Share Google Sheet with service account:
   - Open the JSON file
   - Copy the `client_email` value (looks like: `xxxx@xxxx.iam.gserviceaccount.com`)
   - Go to your Google Sheet
   - Click **Share** button
   - Paste the email and give **Editor** access
   - Click **Share**

**Add to GitHub:**
- Name: `GOOGLE_CLOUD_CREDENTIALS`
- Secret: Copy the entire contents of the downloaded JSON file as a single line

---

## Verification Checklist

- [ ] ANTHROPIC_API_KEY - API key starts with `sk-ant-`
- [ ] ONEDRIVE_FOLDER_URL - Link starts with `https://1drv.ms`
- [ ] GOOGLE_SHEET_ID - Long alphanumeric string from URL
- [ ] GOOGLE_CLOUD_CREDENTIALS - Valid JSON format (paste as-is from downloaded file)

---

## Testing

After adding all secrets:

1. Go to **Actions** tab in GitHub
2. Select **Daily PDF Extraction** workflow
3. Click **Run workflow** button
4. Select **Run workflow**
5. Wait for the workflow to complete
6. Check your Google Sheet for extracted data

---

## Troubleshooting

### Secret not working?
- Double-check the secret name matches exactly (case-sensitive)
- Delete and re-add the secret
- Clear your browser cache

### Google Sheet not updating?
- Verify service account email is shared with **Editor** access
- Check Google Sheet ID is correct (copy from URL)
- Look at GitHub Actions logs for error messages

### OneDrive not downloading?
- Verify link is public (anyone with link can view)
- Try creating a test file in the folder and check if it's accessible via the link

---

## Security Notes

⚠️ **IMPORTANT:**
- Never commit these secrets to the repository
- Never paste secrets in GitHub Issues or discussions
- If a secret is accidentally exposed, regenerate it immediately
- Keep credentials file safe when downloading from Google Cloud

✅ **Best practices:**
- Review GitHub Actions logs to ensure secrets aren't printed
- Rotate credentials every 3-6 months
- Use the principle of least privilege (only grant necessary permissions)
