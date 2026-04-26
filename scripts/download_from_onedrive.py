#!/usr/bin/env python3
"""
Ensure 'Academic Papers' folder exists.
Note: PDFs should be added manually to './Academic Papers' folder
GitHub Actions will process any PDFs in this folder automatically.
"""

import logging
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PAPERS_FOLDER = "./Academic Papers"

def ensure_folder_exists():
    """Create Academic Papers folder if it doesn't exist."""
    Path(PAPERS_FOLDER).mkdir(exist_ok=True)

    # Check if folder is empty
    pdf_count = len(list(Path(PAPERS_FOLDER).glob("*.pdf")))

    logger.info("=" * 70)
    logger.info("PDF Management")
    logger.info("=" * 70)
    logger.info(f"✓ Folder ready: {PAPERS_FOLDER}")
    logger.info(f"✓ PDFs in folder: {pdf_count}")

    if pdf_count == 0:
        logger.info("\n📋 No PDFs found. To add PDFs:")
        logger.info("   1. Download PDFs from your OneDrive/SharePoint folder:")
        logger.info("      https://universityoflincoln-my.sharepoint.com/:f:/g/.../...")
        logger.info("   2. Save them to: ./Academic Papers/")
        logger.info("   3. Commit and push (or just run locally)")
        logger.info("   4. GitHub Actions will automatically process them")
    else:
        logger.info(f"\n✓ Ready to extract {pdf_count} PDF(s)")
        pdfs = list(Path(PAPERS_FOLDER).glob("*.pdf"))
        for pdf in pdfs:
            logger.info(f"   - {pdf.name}")

def main():
    ensure_folder_exists()
    logger.info("\n" + "=" * 70)

if __name__ == "__main__":
    main()
