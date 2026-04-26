# Scoping Review Data Extraction Agent — Setup Guide

## Overview

This guide walks you through setting up and running the automated PDF data extraction tool for your coastal health scoping review.

---

## Step 1: Prerequisites

Ensure you have:
- **Python 3.8 or higher** installed (`python3 --version`)
- **pip** (usually comes with Python)
- **Your Excel file** (`Data_Extraction_Form_1.xlsx`) in the working directory
- **An Anthropic API key** (free to sign up at https://console.anthropic.com)

---

## Step 2: Install Required Libraries

Open a terminal in your working directory and run:

```bash
pip install pdfplumber pypdf openpyxl anthropic
```

This installs:
- **pdfplumber**: Extract text from PDFs
- **pypdf**: Fallback PDF extraction
- **openpyxl**: Read and write Excel files
- **anthropic**: Official Anthropic Python SDK (uses Claude API)

---

## Step 3: Configure the Script

### 3a. Set Your PDF Folder Path

Open `scoping_review_agent.py` in a text editor and find this line (near the top):

```python
PAPERS_FOLDER = "./papers"  # Change to your folder path when ready
```

Replace `"./papers"` with the actual path to your PDF folder. Examples:

**macOS/Linux:**
```python
PAPERS_FOLDER = "/Users/YourUsername/Documents/scoping_review/papers"
```

**Windows:**
```python
PAPERS_FOLDER = "C:\\Users\\YourUsername\\Documents\\scoping_review\\papers"
```

**Or relative to the script's location:**
```python
PAPERS_FOLDER = "./papers"  # If you create a 'papers' folder in the same directory
```

### 3b. Set Your Anthropic API Key

You have two options:

**Option A: Set environment variable (recommended)**

In your terminal, run:

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"  # Replace with your actual key
```

Then run the script in the same terminal session.

**Option B: Store in a `.env` file**

Create a `.env` file in your working directory with:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

Then modify `scoping_review_agent.py` to load it:

```python
from dotenv import load_dotenv
load_dotenv()
```

And add `pip install python-dotenv` to your dependencies.

---

## Step 4: Verify Setup

Before processing real papers, run a test:

```bash
python scoping_review_agent.py
```

You should see:

```
2026-04-26 12:00:00,000 - INFO - ============================================================
2026-04-26 12:00:00,000 - INFO - Starting extraction agent at 2026-04-26 12:00:00.000000
2026-04-26 12:00:00,000 - INFO - ============================================================
2026-04-26 12:00:00,000 - INFO - No new PDFs found
```

This is normal if your papers folder is empty.

---

## Step 5: Running the Script

### Manual Run

Simply execute:

```bash
python scoping_review_agent.py
```

The script will:
1. Scan your papers folder for new PDFs
2. Extract text from each PDF
3. Send to Claude API for data extraction
4. Populate your Excel sheet
5. Log all activity to `extraction_agent.log`

### Scheduling (Optional)

To run automatically once per day, use:

**macOS/Linux (cron):**

Open your crontab editor:

```bash
crontab -e
```

Add this line to run at 8:00 AM every day:

```
0 8 * * * /usr/bin/python3 /path/to/scoping_review_agent.py
```

Make sure the path matches where you saved `scoping_review_agent.py`.

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task → name it "Scoping Review Extraction"
3. Set trigger to "Daily" at 8:00 AM
4. Set action to "Start a program": `python.exe`
5. Add arguments: `C:\path\to\scoping_review_agent.py`

---

## Step 6: Add Your First Papers

1. Place your PDF files in the `PAPERS_FOLDER` you configured
2. Run the script
3. Check `extraction_agent.log` for progress
4. Open your Excel file to see the new rows

---

## Files Created and Used

| File | Purpose |
|---|---|
| `scoping_review_agent.py` | Main script — run this |
| `Data_Extraction_Form_1.xlsx` | Your Excel sheet (script appends to this) |
| `processed_files.json` | Tracks which PDFs have been processed — auto-created |
| `extraction_agent.log` | Log file with detailed progress and errors |

---

## Costs

Claude API usage is pay-as-you-go:

- **~£0.01–0.05 per paper** (typically ~3,000–5,000 tokens)
- 50 papers ≈ under £2.50
- You are only charged for API calls made (no hidden fees)

Monitor your usage at: https://console.anthropic.com/account/usage

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY environment variable not set"

**Solution:** Set your API key before running:

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
python scoping_review_agent.py
```

### Issue: "Papers folder does not exist"

**Solution:** Update `PAPERS_FOLDER` in the script to the correct path.

### Issue: "Excel file not found"

**Solution:** Ensure `Data_Extraction_Form_1.xlsx` is in the same directory as the script.

### Issue: Script runs but produces no output

**Solution:** Check `extraction_agent.log` for errors:

```bash
cat extraction_agent.log
```

### Issue: PDF extraction returns mostly blank

**Your PDF might be a scanned image** (not text-based). The script logs a warning — you'll need to:
- Check if the PDF is readable as text in your viewer
- If it's an image scan, you'll need OCR (can be added later)

### Issue: Excel file shows "N/A" for expected data

**Solution:** Claude may not have found the information. Check:
- Is the field actually in the PDF?
- Review the log to see what text was extracted
- You can manually fill in missing fields

### Issue: Script crashes or hangs

**Solution:**
1. Check `extraction_agent.log` for the error
2. Verify your API key is correct
3. Check your internet connection
4. Try processing just one PDF to isolate the issue

---

## What to Expect

When the script runs:

1. **No new PDFs:** Script finishes silently (logs "No new PDFs found")
2. **Processing PDF:** Logs show progress for each file
3. **Data extracted:** New row appears in Excel with all 24 fields populated
4. **Blank fields:** Some fields may be "N/A" or blank — fill manually as needed
5. **Already processed:** Same PDF twice = skipped automatically

---

## Support & Logs

All activity is logged to `extraction_agent.log`. Review this file if:
- Papers aren't being processed
- Data looks incomplete
- You want to verify what happened

Example log output:

```
2026-04-26 12:00:00,000 - INFO - Starting extraction agent at 2026-04-26 12:00:00.000000
2026-04-26 12:00:00,000 - INFO - Found 1 new PDF(s)
2026-04-26 12:00:00,000 - INFO - Processing: Smith_2023.pdf
2026-04-26 12:00:05,000 - INFO - Extracted 15234 characters from Smith_2023.pdf
2026-04-26 12:00:10,000 - INFO - Data written to Excel row 44: Smith_2023.pdf
2026-04-26 12:00:10,000 - INFO - ✓ Successfully processed Smith_2023.pdf
```

---

## Next Steps

1. **Update PAPERS_FOLDER path** in the script
2. **Set your API key** (environment variable or .env file)
3. **Run the script:** `python scoping_review_agent.py`
4. **Add 2-3 test papers** to your PDF folder
5. **Check the results** in your Excel file
6. **Let me know if adjustments are needed** (e.g., field extraction depth, column mappings)

---

## Questions?

If something doesn't work:
1. Check `extraction_agent.log` for detailed error messages
2. Verify the path configuration and API key
3. Try running with just one PDF to isolate the issue
4. Share the relevant log lines and I'll help debug

---

*Happy extracting!*
