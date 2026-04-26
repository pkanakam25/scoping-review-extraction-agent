# Scoping Review Data Extraction Agent

Automated extraction of academic data from PDFs into Excel for your coastal health scoping review.

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure the script
Edit `scoping_review_agent.py` and set:
```python
PAPERS_FOLDER = "/your/path/to/papers"  # Where your PDFs are
```

### 3. Set API key
```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

### 4. Run it
```bash
python scoping_review_agent.py
```

## What It Does

✅ Watches your papers folder daily  
✅ Finds new PDFs automatically  
✅ Extracts text using pdfplumber  
✅ Uses Claude AI to intelligently extract 24 fields  
✅ Populates your Excel sheet automatically  
✅ Never reprocesses the same paper  
✅ Logs everything for transparency  

## The 24 Fields

| # | Field | Notes |
|---|---|---|
| 1-2 | S.No., Source Type | Auto-filled / blank for manual entry |
| 3-7 | Authors, Country, Title, Publication Type, Year | Auto-extracted |
| 8-12 | Evidence Type, Aim, Research Questions, Design, Methodology | Auto-extracted (Methodology is detailed) |
| 13-18 | Population, Setting, Data Collection, Coastal Definition, Interventions, Outcomes | Auto-extracted |
| 19-24 | Key Findings, Knowledge Gaps, Barriers, Affiliation, Funding, Data Accessibility | Auto-extracted / blank for manual entry |

## Files

- **scoping_review_agent.py** — Main script (run this)
- **Data_Extraction_Form_1.xlsx** — Your Excel sheet (auto-updated)
- **processed_files.json** — Tracks processed PDFs (auto-created)
- **extraction_agent.log** — Activity log (auto-created)

## How It Works

```
1. Scan papers folder for new PDFs
2. Extract text from each PDF
3. Send to Claude API for intelligent extraction
4. Write structured data to Excel row
5. Mark PDF as processed (never run twice)
6. Log all activity
```

## Configuration

**Before first run, edit `scoping_review_agent.py`:**

```python
# Line ~8: Set your papers folder
PAPERS_FOLDER = "/Users/username/Documents/scoping_review/papers"

# Line ~10: Your Excel file (should be in same directory)
EXCEL_FILE = "Data_Extraction_Form_1.xlsx"
```

**Set API key (one-time):**

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

## Costs

- **~£0.01–0.05 per paper**
- 50 papers ≈ under £2.50
- Pay only for what you use

Get your API key: https://console.anthropic.com

## Troubleshooting

**"ANTHROPIC_API_KEY not set"**
```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
python scoping_review_agent.py
```

**"Papers folder does not exist"**
→ Update `PAPERS_FOLDER` path in the script

**Check the log**
```bash
cat extraction_agent.log
```

## Full Documentation

See `SETUP_GUIDE.md` for detailed setup and scheduling instructions.

## What Happens to Your Excel File

- ✅ Existing 41 rows (rows 3–43) remain untouched
- ✅ New papers append from row 44 onwards
- ✅ Guidance columns (even rows) stay as-is
- ✅ Saved after every paper (no data loss if script crashes)

## Expected Behavior

**First run (empty folder):**
```
No new PDFs found
```

**With 1 new PDF:**
```
Found 1 new PDF(s)
Processing: Smith_2023.pdf
Extracted 15234 characters from Smith_2023.pdf
Data written to Excel row 44: Smith_2023.pdf
✓ Successfully processed Smith_2023.pdf
1/1 successful
```

## Defaults (you can customize)

- ✅ **Source Type:** Left blank for you to fill manually
- ✅ **Data Accessibility:** Left blank for you to fill manually  
- ✅ **Methodology:** Detailed extraction (300–500 words target)

## Next Steps

1. Update `PAPERS_FOLDER` path in `scoping_review_agent.py`
2. Set your Anthropic API key
3. Create a `papers/` folder (or use your existing one)
4. Add 2–3 test PDFs
5. Run the script: `python scoping_review_agent.py`
6. Check your Excel file for new rows
7. Review the log: `cat extraction_agent.log`

---

**Need help?** Check `extraction_agent.log` — it logs everything that happens.
