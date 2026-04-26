# Automated OneDrive PDF Download - OAuth Setup

## Overview

Set up Microsoft OAuth authentication to automatically download PDFs from your OneDrive/SharePoint folder and update Google Sheets.

**After setup:** GitHub Actions will automatically:
1. ✅ Check OneDrive for new PDFs
2. ✅ Download them
3. ✅ Extract data
4. ✅ Update Google Sheets

---

## **Step 1: Create Azure AD App Registration**

### In Azure Portal:

1. Go to https://portal.azure.com
2. Sign in with your University of Lincoln credentials
3. Search for **Azure Active Directory**
4. Click **App registrations** (left sidebar)
5. Click **+ New registration**

### Fill in the form:

- **Name:** `Scoping Review OneDrive Bot`
- **Account types:** Select "Accounts in this organizational directory only (University of Lincoln AD)"
- **Redirect URI:** 
  - Platform: **Web**
  - URI: `https://localhost:8000/auth/callback`
- Click **Register**

---

## **Step 2: Get Client ID & Tenant ID**

On the app page you just created:

1. Copy **Application (client) ID** - you'll need this
2. Copy **Directory (tenant) ID** - you'll need this

**Save these somewhere safe!**

---

## **Step 3: Create Client Secret**

1. Click **Certificates & secrets** (left sidebar)
2. Click **+ New client secret**
3. Set:
   - **Description:** `OneDrive API access`
   - **Expires:** `24 months`
4. Click **Add**
5. **Immediately copy the VALUE** (the secret itself, not the ID)
6. Save it safely - you won't see it again!

---

## **Step 4: Grant API Permissions**

1. Click **API permissions** (left sidebar)
2. Click **+ Add a permission**
3. Click **Microsoft Graph**
4. Select **Delegated permissions**
5. Search for and select:
   - `Files.Read.All` (read all files in OneDrive)
   - `Files.ReadWrite.All` (read/write files)
   - `User.Read` (read user info)
6. Click **Add permissions**
7. Click **Grant admin consent for [University]**
8. Click **Yes** to confirm

---

## **Step 5: Add GitHub Secrets**

You now have 3 values to add to GitHub:

1. Go to your GitHub repo
2. Settings → **Secrets and variables** → **Actions**
3. Add these 3 new secrets:

| Secret Name | Value |
|---|---|
| `MICROSOFT_CLIENT_ID` | From Step 2 (Application ID) |
| `MICROSOFT_CLIENT_SECRET` | From Step 3 (Secret value) |
| `MICROSOFT_TENANT_ID` | From Step 2 (Directory ID) |

---

## **Step 6: Update the Download Script**

Now the automated download script will use OAuth. Here's what it will do:

```python
# The script will:
1. Authenticate using your credentials
2. List files in your OneDrive folder
3. Find all PDFs
4. Download new ones not yet processed
5. Extract data
6. Update Google Sheets
```

---

## **Testing the Automated Setup**

### **Test Locally:**

```bash
python3 scripts/download_from_onedrive.py
```

Should output:
```
✓ Authenticating with Microsoft Graph...
✓ Connected to OneDrive
✓ Found X PDFs
✓ Downloaded X new PDFs
```

### **Test on GitHub Actions:**

1. Go to GitHub → **Actions**
2. Click **Daily PDF Extraction**
3. Click **Run workflow**
4. Wait 2-3 minutes
5. Check your **Google Sheet** for new data

---

## **How It Works - Daily Automated Flow**

```
Every day at 8 AM UTC:
    ↓
GitHub Actions runs
    ↓
1. Authenticate with Microsoft (using OAuth credentials)
    ↓
2. Connect to OneDrive folder
    ↓
3. List all PDFs in folder
    ↓
4. Check which ones are new (not yet processed)
    ↓
5. Download new PDFs
    ↓
6. Run extraction agent
    ↓
7. Extract 24 fields per PDF
    ↓
8. Upload results to Google Sheets
    ↓
9. Mark PDFs as processed
    ↓
Done! Results in Google Sheets ✅
```

---

## **What Gets Stored**

The script tracks processed files in `processed_files.json`:

```json
{
  "processed_files": [
    "Paper1.pdf",
    "Paper2.pdf",
    "Paper3.pdf"
  ]
}
```

This prevents re-processing the same PDF twice.

---

## **Troubleshooting OAuth Setup**

### "Authentication failed"

- Verify Client ID is correct
- Verify Client Secret is correct
- Verify Tenant ID is correct
- Check permissions are granted (Step 4)

### "Access denied to OneDrive"

- Make sure you selected "Accounts in this organizational directory" (not "Multi-tenant")
- Grant admin consent to the app permissions
- Wait 5 minutes for permissions to propagate

### "Can't find OneDrive folder"

- Verify the folder URL in GitHub Secrets is correct
- Make sure the folder is in your personal OneDrive (not a shared drive)
- Check folder permissions in SharePoint

---

## **Security Notes**

✅ **GitHub Secrets** - Store OAuth credentials safely  
✅ **No passwords** - Uses OAuth tokens, not your password  
✅ **Minimal permissions** - Only access to files, not other data  
✅ **.gitignore** - Credentials never in code  
✅ **Scoped access** - Limited to OneDrive folder only  

---

## **Next Steps**

1. Create Azure AD app registration (Steps 1-4)
2. Add 3 GitHub Secrets (Step 5)
3. Test locally: `python3 scripts/download_from_onedrive.py`
4. Test on GitHub Actions
5. Verify results in Google Sheet

---

## **Support**

If stuck on any step:
1. Check the troubleshooting section above
2. Review Azure documentation: https://docs.microsoft.com/en-us/azure/active-directory
3. Review Microsoft Graph: https://docs.microsoft.com/en-us/graph

---

**Once set up:** Fully automated daily PDF extraction! 🚀
