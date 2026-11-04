
import re
import html
import unicodedata

import pandas as pd


def clean_text(text):
    """
    Clean civic complaint text while preserving multilingual content.

    Operations:
    1. Handle missing values.
    2. Convert input to string.
    3. Decode HTML entities.
    4. Normalize Unicode using NFC.
    5. Standardize whitespace.
    6. Remove leading and trailing whitespace.
    """

    # Handle missing or non-string values safely
    if pd.isna(text):
        return ""

    # Convert input into a string
    text = str(text)

    # Decode HTML entities such as &amp; and &nbsp;
    text = html.unescape(text)

    # Normalize Unicode without removing language characters
    text = unicodedata.normalize("NFC", text)

    # Replace line breaks, tabs and repeated whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary leading and trailing whitespace
    text = text.strip()

    return text
