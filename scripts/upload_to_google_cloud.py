#!/usr/bin/env python3
"""
Upload extraction results to Google Cloud Storage and Google Sheets.
Options:
- Option A: Upload Excel file to Google Cloud Storage
- Option B: Sync data to Google Sheets (recommended)
"""

import os
import json
import logging
from pathlib import Path
import openpyxl

# Google Cloud imports
from google.cloud import storage
from google.oauth2 import service_account
import gspread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXCEL_FILE = "Data Extraction Form_1.xlsx"
GOOGLE_CLOUD_CREDENTIALS_JSON = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GCS_BUCKET = os.getenv("GCS_BUCKET_NAME", "scoping-review-extraction")

def get_credentials():
    """Load Google Cloud credentials from environment."""
    if not GOOGLE_CLOUD_CREDENTIALS_JSON:
        logger.warning("GOOGLE_CLOUD_CREDENTIALS not set. Skipping upload.")
        return None

    try:
        # Parse JSON credentials from GitHub Secrets
        credentials_dict = json.loads(GOOGLE_CLOUD_CREDENTIALS_JSON)
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        logger.info("✓ Google Cloud credentials loaded")
        return credentials
    except Exception as e:
        logger.error(f"Failed to load credentials: {e}")
        return None

def upload_to_google_cloud_storage(credentials):
    """Upload Excel file to Google Cloud Storage."""
    if not os.path.exists(EXCEL_FILE):
        logger.warning(f"Excel file not found: {EXCEL_FILE}")
        return

    try:
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(GCS_BUCKET)
        blob = bucket.blob(f"extractions/{EXCEL_FILE}")

        logger.info(f"Uploading to GCS: gs://{GCS_BUCKET}/extractions/{EXCEL_FILE}")
        blob.upload_from_filename(EXCEL_FILE)
        logger.info("✓ Successfully uploaded to Google Cloud Storage")
    except Exception as e:
        logger.error(f"Failed to upload to GCS: {e}")

def upload_to_google_sheets(credentials):
    """Sync extraction data to Google Sheets (recommended method)."""
    if not GOOGLE_SHEET_ID:
        logger.warning("GOOGLE_SHEET_ID not set. Skipping Google Sheets sync.")
        return

    if not os.path.exists(EXCEL_FILE):
        logger.warning(f"Excel file not found: {EXCEL_FILE}")
        return

    try:
        # Authenticate with gspread
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(GOOGLE_SHEET_ID)
        worksheet = sheet.get_worksheet(0)

        # Load data from Excel
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active

        # Prepare data (headers + rows)
        data = []
        for row in ws.iter_rows(min_row=1, values_only=True):
            data.append(list(row))

        # Clear existing data and write new data
        logger.info(f"Syncing data to Google Sheet (ID: {GOOGLE_SHEET_ID})")
        worksheet.clear()
        worksheet.update(data)

        logger.info(f"✓ Successfully synced {len(data)} rows to Google Sheets")
    except Exception as e:
        logger.error(f"Failed to sync to Google Sheets: {e}")

def main():
    credentials = get_credentials()
    if not credentials:
        logger.info("Skipping cloud upload (no credentials)")
        return

    # Option A: Upload to Google Cloud Storage
    # upload_to_google_cloud_storage(credentials)

    # Option B: Sync to Google Sheets (recommended)
    upload_to_google_sheets(credentials)

if __name__ == "__main__":
    main()
