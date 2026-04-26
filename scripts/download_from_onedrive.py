#!/usr/bin/env python3
"""
Automatically download PDFs from Google Drive folder.
Uses Google Cloud service account credentials.
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
GOOGLE_CLOUD_CREDENTIALS = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
PAPERS_FOLDER = "./Academic Papers"

def ensure_folder_exists():
    """Create Academic Papers folder if it doesn't exist."""
    Path(PAPERS_FOLDER).mkdir(exist_ok=True)

def download_from_google_drive():
    """
    Download PDFs from Google Drive using service account credentials.
    """
    if not GOOGLE_DRIVE_FOLDER_ID:
        logger.warning("GOOGLE_DRIVE_FOLDER_ID not set in GitHub Secrets")
        logger.info("Set up: Go to GitHub Secrets and add GOOGLE_DRIVE_FOLDER_ID")
        return

    if not GOOGLE_CLOUD_CREDENTIALS:
        logger.warning("GOOGLE_CLOUD_CREDENTIALS not set in GitHub Secrets")
        return

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        import io

        logger.info("Connecting to Google Drive...")

        # Parse credentials from environment
        creds_dict = json.loads(GOOGLE_CLOUD_CREDENTIALS)
        credentials = Credentials.from_service_account_info(creds_dict)

        # Build Google Drive API client
        service = build('drive', 'v3', credentials=credentials)

        logger.info(f"Downloading PDFs from folder: {GOOGLE_DRIVE_FOLDER_ID}")

        # Query for PDF files in the folder
        query = f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and mimeType='application/pdf' and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, modifiedTime)',
            pageSize=100
        ).execute()

        files = results.get('files', [])

        if not files:
            logger.info("✓ No PDFs found in Google Drive folder")
            return

        logger.info(f"✓ Found {len(files)} PDF(s) in Google Drive")

        # Download each file
        downloaded_count = 0
        for file in files:
            file_name = file['name']
            file_id = file['id']
            file_path = Path(PAPERS_FOLDER) / file_name

            # Skip if already downloaded
            if file_path.exists():
                logger.info(f"  ↷ Already exists: {file_name}")
                continue

            try:
                logger.info(f"  ↓ Downloading: {file_name}")

                # Download file
                request = service.files().get_media(fileId=file_id)
                file_obj = io.BytesIO()
                downloader = MediaIoBaseDownload(file_obj, request)

                done = False
                while not done:
                    status, done = downloader.next_chunk()

                # Save file
                with open(file_path, 'wb') as f:
                    f.write(file_obj.getvalue())

                logger.info(f"  ✓ Downloaded: {file_name}")
                downloaded_count += 1

            except Exception as e:
                logger.error(f"  ✗ Failed to download {file_name}: {e}")

        logger.info(f"\n✓ Downloaded {downloaded_count} new PDF(s)")

    except ImportError:
        logger.warning("Google Drive API library not installed")
        logger.info("Install: pip install google-api-python-client")
    except json.JSONDecodeError:
        logger.error("Invalid GOOGLE_CLOUD_CREDENTIALS JSON")
    except Exception as e:
        logger.error(f"Failed to download from Google Drive: {e}")

def main():
    logger.info("=" * 70)
    logger.info("PDF Download from Google Drive")
    logger.info("=" * 70)

    ensure_folder_exists()
    download_from_google_drive()

    # Check final count
    pdf_count = len(list(Path(PAPERS_FOLDER).glob("*.pdf")))
    logger.info(f"\n✓ Total PDFs in ./Academic Papers: {pdf_count}")

    if pdf_count == 0:
        logger.info("\n⚠️  No PDFs found")
        logger.info("\nTo set up Google Drive integration:")
        logger.info("  1. Create folder in Google Drive: 'Academic Papers - Scoping Review'")
        logger.info("  2. Get folder ID from URL")
        logger.info("  3. Share with service account email")
        logger.info("  4. Add GOOGLE_DRIVE_FOLDER_ID to GitHub Secrets")

if __name__ == "__main__":
    main()
