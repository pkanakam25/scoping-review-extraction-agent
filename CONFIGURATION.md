# Configuration Guide

Before running the script for the first time, you need to configure two things:

## 1. PDF Folder Path

**What it is:** The folder on your computer where you'll place PDF files for extraction.

**How to set it:**

Open `scoping_review_agent.py` in a text editor and find this line (~line 8):

```python
PAPERS_FOLDER = "./papers"  # Change to your folder path when ready
```

Replace with your actual folder path:

### Example 1: Relative Path (if PDFs are in a subfolder)

```python
PAPERS_FOLDER = "./papers"  # Folder called "papers" in the same directory as the script
```

Create the folder:
```bash
mkdir papers
```

### Example 2: Absolute Path (macOS/Linux)

```python
PAPERS_FOLDER = "/Users/YourName/Documents/scoping_review/papers"
```

### Example 3: Absolute Path (Windows)

```python
PAPERS_FOLDER = "C:\\Users\\YourName\\Documents\\scoping_review\\papers"
```

## 2. API Key

**What it is:** Your Anthropic API key for using Claude (costs ~£0.01–0.05 per paper).

**How to get it:**
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key (copy the full key starting with `sk-ant-`)

**How to set it:**

Run this command in your terminal (one time):

```bash
export ANTHROPIC_API_KEY="sk-ant-YOUR_ACTUAL_KEY_HERE"
```

Then run the script in the same terminal window:

```bash
python scoping_review_agent.py
```

**Verify it worked:**

The script will either:
- ✅ Run successfully (logs to `extraction_agent.log`)
- ❌ Error with "ANTHROPIC_API_KEY environment variable not set" (means the key wasn't found)

---

## Checklist Before First Run

- [ ] Updated `PAPERS_FOLDER` path in `scoping_review_agent.py`
- [ ] Created the papers folder (or verified it exists)
- [ ] Set `ANTHROPIC_API_KEY` environment variable
- [ ] Installed dependencies with `pip install -r requirements.txt`
- [ ] Verified `Data_Extraction_Form_1.xlsx` is in the same directory as the script
- [ ] Added 1–2 test PDFs to your papers folder
- [ ] Run: `python scoping_review_agent.py`

---

## After Configuration

Once both are set:

```bash
# Terminal 1: Set the API key (one time)
export ANTHROPIC_API_KEY="sk-ant-YOUR_KEY"

# Terminal 1: Run the script
python scoping_review_agent.py
```

You should see output in the terminal and in `extraction_agent.log`.

---

## Tips

- **API Key expires?** Generate a new one in the console and update it
- **Changing the folder?** Just edit the `PAPERS_FOLDER` line and re-run
- **Want to schedule it?** See `SETUP_GUIDE.md` for macOS/Linux cron and Windows Task Scheduler instructions
- **Unsure about your folder path?** Run this in terminal to get the full path:

```bash
# macOS/Linux
pwd  # Shows current directory path
ls -la  # Shows contents

# Windows (PowerShell)
Get-Location  # Shows current directory
ls  # Shows contents
```

---

## Important Notes

### Column Mapping

The script assumes your Excel sheet has this structure:
- Row 1–2: Headers (data fields + guidance columns)
- Row 3–43: Existing extracted data (41 papers)
- Row 44+: Where new data will be appended

**If your sheet structure is different**, you'll need to verify the column mapping in `scoping_review_agent.py` (lines ~180–205). Let me know if adjustments are needed after you share your Excel file.

### Excel File

The script expects your file to be named `Data_Extraction_Form_1.xlsx` in the same directory as the script. If your file has a different name, update this line in the script:

```python
EXCEL_FILE = "Data_Extraction_Form_1.xlsx"  # Change if needed
```

---

## Environment Variables (Optional)

If you prefer not to set the API key via command line each time, you can create a `.env` file:

1. Create a file named `.env` in the same directory as the script
2. Add this line:

```
ANTHROPIC_API_KEY=sk-ant-YOUR_ACTUAL_KEY
```

3. Modify `scoping_review_agent.py` to load it by adding these lines at the top:

```python
from dotenv import load_dotenv
load_dotenv()
```

4. Install python-dotenv:

```bash
pip install python-dotenv
```

Then you can just run `python scoping_review_agent.py` without setting the environment variable each time.

---

## Ready?

Once you've completed the checklist, you're ready to run the script. Start with 1–2 test papers to verify everything works.
