# PDF Management for GitHub Actions

## Recommended Workflow

Since SharePoint requires OAuth for API access, here's the simple, effective approach:

---

## **Your OneDrive/SharePoint Link**

```
https://universityoflincoln-my.sharepoint.com/:f:/g/personal/pkanakam_lincoln_ac_uk/IgBRe7K39jHqRJCmyr_ZdtFWARO3kngpQjVAPqBnMOvilk8?e=QoHSlJ
```

---

## **Workflow: Local Management**

### **Step 1: Download PDFs from SharePoint**

1. Open your University of Lincoln SharePoint folder:
   ```
   https://universityoflincoln-my.sharepoint.com/:f:/g/personal/pkanakam_lincoln_ac_uk/IgBRe7K39jHqRJCmyr_ZdtFWARO3kngpQjVAPqBnMOvilk8?e=QoHSlJ
   ```

2. Download new PDFs to your computer

3. Move/copy them to your local `Academic Papers` folder:
   ```
   ./Academic Papers/
   ├── Paper1.pdf
   ├── Paper2.pdf
   └── Paper3.pdf
   ```

### **Step 2: Trigger Extraction**

**Option A: Local (Immediate Results)**
```bash
python3 scoping_review_agent.py
```

**Option B: GitHub Actions (Scheduled)**
- Commit the PDF changes:
  ```bash
  git add Academic\ Papers/*.pdf
  git commit -m "Add new papers for extraction"
  git push
  ```
- GitHub Actions runs automatically at 8 AM UTC
- Or manually trigger: GitHub → Actions → Daily PDF Extraction → Run workflow

### **Step 3: View Results**

Check your Google Sheet for automatically updated extraction results!

---

## **Why This Approach?**

✅ **Simple**: No OAuth setup needed  
✅ **Secure**: PDFs not in version control  
✅ **Flexible**: Run anytime (locally or GitHub Actions)  
✅ **Reliable**: Direct file access, no API limitations  
✅ **Controllable**: You decide when to process  

---

## **Important: .gitignore Settings**

The repo intentionally **excludes** the Academic Papers folder:

```bash
# .gitignore
Academic Papers/     # Local PDFs not versioned
*.xlsx               # Excel file not versioned
processed_files.json # Local tracking file
```

**Why?** These files change constantly and shouldn't bloat the repo.

---

## **Alternative: Commit PDFs to GitHub**

If you want PDFs in the repo:

1. **Remove from .gitignore:**
   ```bash
   # Edit .gitignore
   # Comment out: Academic Papers/
   ```

2. **Add PDFs:**
   ```bash
   git add Academic\ Papers/*.pdf
   git commit -m "Add academic papers"
   git push
   ```

3. **Pros:** PDFs always available in GitHub Actions, no manual download needed
4. **Cons:** Repo size grows with each PDF (~500KB-5MB per paper)

---

## **Alternative: Azure AD OAuth (Advanced)**

If you need full automation without manual file management:

### Setup Steps:
1. Register app in University of Lincoln Azure AD
2. Grant SharePoint API permissions
3. Store credentials in GitHub Secrets
4. Use OAuth token in download script

**Trade-off:** More setup (2-3 hours) but fully automated

---

## **Recommended: Start Simple**

1. **Week 1**: Manual file management (5 minutes per run)
2. **Month 1**: Evaluate if you want full automation
3. **Later**: Switch to OAuth if needed

Most users find manual management perfectly fine because:
- You naturally check the folder once a week
- Adding to GitHub is just one extra step
- Results appear in Google Sheets within seconds

---

## **Troubleshooting**

### PDFs not processing?
1. Verify they're in `./Academic Papers/` folder
2. Check file names don't have special characters
3. Ensure they're valid PDFs (not scanned images)
4. Check `extraction_agent.log` for errors

### Extraction seems incomplete?
- See `extraction_agent.log` for details
- Some fields may be N/A if not in the paper
- Manual review in Google Sheet recommended

### Want to re-extract?
1. Delete the PDF name from `processed_files.json`
2. Run extraction again
3. PDF will be reprocessed

---

## **Your Setup**

✅ PDF source: University of Lincoln SharePoint  
✅ Processing: Local or GitHub Actions  
✅ Results: Google Sheets  
✅ Method: Manual PDF management (simple & effective)

**Ready to start?**
1. Add `ONEDRIVE_FOLDER_URL` to GitHub Secrets (your SharePoint link)
2. Add PDFs to `./Academic Papers/`
3. Run GitHub Actions (manually or wait for 8 AM UTC)
4. Check Google Sheets for results

That's it! 🎉
