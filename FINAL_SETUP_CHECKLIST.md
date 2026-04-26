# Final Setup Checklist - Your Deployment

## ✅ Your Setup Details

**GitHub Secrets to Add:**

| Secret Name | Your Value | Status |
|---|---|---|
| `ANTHROPIC_API_KEY` | Get from https://console.anthropic.com | ⏳ TODO |
| `ONEDRIVE_FOLDER_URL` | `https://universityoflincoln-my.sharepoint.com/:f:/g/personal/pkanakam_lincoln_ac_uk/IgBRe7K39jHqRJCmyr_ZdtFWARO3kngpQjVAPqBnMOvilk8?e=QoHSlJ` | ✅ READY |
| `GOOGLE_SHEET_ID` | `1w_LVupbgUukUf8b4wLt-aACuDwXiR9YWoQY0NI1ZlvM` | ✅ READY |
| `GOOGLE_CLOUD_CREDENTIALS` | Download from Google Cloud Console | ⏳ TODO |

---

## 📋 Step-by-Step Setup

### **Step 1: Get Anthropic API Key** (2 minutes)

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to **API Keys**
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)
6. Save it safely

✅ You'll have: `sk-ant-xxxxxxxxxxxxxxx`

---

### **Step 2: Set Up Google Cloud & Get Credentials** (10 minutes)

#### **2a. Create Google Cloud Project**

1. Go to https://console.cloud.google.com
2. Click **Select a Project** (top)
3. Click **NEW PROJECT**
4. Name it: `Scoping Review Extraction`
5. Click **CREATE**
6. Wait for it to be created

#### **2b. Enable Required APIs**

1. Go to **APIs & Services** → **Library**
2. Search for **"Google Sheets API"**
   - Click it → **ENABLE**
3. Search for **"Google Drive API"**
   - Click it → **ENABLE**

#### **2c. Create Service Account**

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **Service Account**
3. Fill in the form:
   - Service account name: `scoping-review-bot`
   - Service account ID: (auto-filled)
   - Description: "Bot for scoping review extraction"
4. Click **CREATE AND CONTINUE**
5. Skip "Grant this service account access to project" (optional)
6. Skip "Grant users access to this service account" 
7. Click **DONE**

#### **2d. Create JSON Key**

1. You should see the service account listed
2. Click on the service account **`scoping-review-bot`**
3. Go to **KEYS** tab
4. Click **ADD KEY** → **Create new key**
5. Choose **JSON**
6. Click **CREATE**
7. A file will download: `scoping-review-bot-xxxxx.json`

**IMPORTANT:** Save this file safely! This is your credential.

✅ You'll have a JSON file with your credentials

---

### **Step 3: Share Google Sheet with Service Account** (3 minutes)

1. Open the downloaded JSON file in a text editor
2. Find the line: `"client_email": "scoping-review-bot@xxxx.iam.gserviceaccount.com"`
3. Copy that email address

4. Go to your Google Sheet:
   https://docs.google.com/spreadsheets/d/1w_LVupbgUukUf8b4wLt-aACuDwXiR9YWoQY0NI1ZlvM/edit

5. Click **SHARE** (top right)
6. Paste the service account email
7. Give **Editor** access
8. Click **SHARE**

✅ Service account now has access to your sheet

---

### **Step 4: Prepare GitHub Secrets** (5 minutes)

You now have everything needed. Convert the JSON credentials to a single line:

1. Open the `scoping-review-bot-xxxxx.json` file
2. Copy the entire contents
3. You'll paste this as the `GOOGLE_CLOUD_CREDENTIALS` secret

---

### **Step 5: Create GitHub Repository** (5 minutes)

```bash
# Navigate to your project directory
cd /Users/pujithakanakam/Desktop/scoping-review-extraction-agent

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Scoping review extraction agent with GitHub Actions"

# Rename branch to main
git branch -M main

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/scoping-review-extraction-agent.git

# Push to GitHub
git push -u origin main
```

✅ Your code is now on GitHub

---

### **Step 6: Add GitHub Secrets** (5 minutes)

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret**

**Add these 4 secrets:**

#### Secret 1: ANTHROPIC_API_KEY
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-xxxxxxxxxxxxxxx` (from Step 1)
- Click **Add secret**

#### Secret 2: ONEDRIVE_FOLDER_URL
- Name: `ONEDRIVE_FOLDER_URL`
- Value: `https://universityoflincoln-my.sharepoint.com/:f:/g/personal/pkanakam_lincoln_ac_uk/IgBRe7K39jHqRJCmyr_ZdtFWARO3kngpQjVAPqBnMOvilk8?e=QoHSlJ`
- Click **Add secret**

#### Secret 3: GOOGLE_SHEET_ID
- Name: `GOOGLE_SHEET_ID`
- Value: `1w_LVupbgUukUf8b4wLt-aACuDwXiR9YWoQY0NI1ZlvM`
- Click **Add secret**

#### Secret 4: GOOGLE_CLOUD_CREDENTIALS
- Name: `GOOGLE_CLOUD_CREDENTIALS`
- Value: Copy the entire contents of `scoping-review-bot-xxxxx.json`
- Click **Add secret**

✅ All secrets are now configured

---

### **Step 7: Add Your First PDFs** (5 minutes)

1. Download some PDFs from your SharePoint:
   https://universityoflincoln-my.sharepoint.com/:f:/g/personal/pkanakam_lincoln_ac_uk/IgBRe7K39jHqRJCmyr_ZdtFWARO3kngpQjVAPqBnMOvilk8?e=QoHSlJ

2. Save them to your local folder:
   ```
   ./Academic Papers/
   ```

3. Commit them to GitHub:
   ```bash
   git add "Academic Papers/"
   git commit -m "Add academic papers for extraction"
   git push
   ```

✅ PDFs are now in your repository

---

### **Step 8: Test the Workflow** (2 minutes)

1. Go to your GitHub repository
2. Click **Actions** tab (top)
3. Click **Daily PDF Extraction** (left sidebar)
4. Click **Run workflow** button
5. Select **main** branch (if asked)
6. Click **Run workflow**

Wait 2-3 minutes for it to complete...

✅ Check the logs:
- Click the running workflow
- Expand each step to see details
- Look for "✓ Successfully synced X rows to Google Sheets"

---

### **Step 9: Verify Results in Google Sheets** (1 minute)

1. Go to your Google Sheet:
   https://docs.google.com/spreadsheets/d/1w_LVupbgUukUf8b4wLt-aACuDwXiR9YWoQY0NI1ZlvM/edit

2. Check the last rows for new data
3. You should see extracted fields:
   - S.No., Author(s), Country, Title, Year, etc.

✅ If you see data, everything is working! 🎉

---

## 🎯 Summary

### Total Time: ~45 minutes (mostly waiting)

**What you're setting up:**
- ✅ Code on GitHub (version controlled)
- ✅ Automated daily runs at 8 AM UTC
- ✅ Automatic upload to Google Sheets
- ✅ Manual PDF management (simple & effective)

### How it works after setup:
1. **Every day at 8 AM UTC**: GitHub Actions runs automatically
2. **Processes PDFs** in `./Academic Papers/` folder
3. **Uploads results** to your Google Sheet
4. **You review** the extracted data in Google Sheets

### To add new papers:
1. Download from SharePoint
2. Save to `./Academic Papers/`
3. Commit: `git add . && git commit -m "Add new papers" && git push`
4. Wait for next scheduled run (or manually trigger)
5. Check Google Sheets for results

---

## 🚀 Launch Checklist

- [ ] Got Anthropic API key (`sk-ant-...`)
- [ ] Created Google Cloud project
- [ ] Enabled Google Sheets & Drive APIs
- [ ] Created service account
- [ ] Downloaded JSON credentials
- [ ] Shared Google Sheet with service account email
- [ ] Created GitHub repository
- [ ] Added 4 GitHub Secrets
- [ ] Added PDFs to `./Academic Papers/`
- [ ] Committed and pushed to GitHub
- [ ] Tested workflow manually
- [ ] Verified results in Google Sheet

✅ **Everything complete!** Your system is live.

---

## 📞 Support

All documentation is in your repository:
- `PDF_MANAGEMENT.md` — How to manage PDFs
- `GITHUB_ACTIONS_SETUP.md` — Detailed setup guide
- `DEPLOYMENT.md` — Architecture overview
- `GITHUB_SECRETS_SETUP.md` — Secret configuration reference

---

## 🎉 You're Ready!

Your scoping review extraction agent is now:
- **Automated** (runs daily)
- **Scalable** (processes any number of PDFs)
- **Cloud-integrated** (results in Google Sheets)
- **Zero-cost** (GitHub + Google free tier)
- **Secure** (secrets, not code)

**Questions? Check the docs or review the logs in GitHub Actions!**
