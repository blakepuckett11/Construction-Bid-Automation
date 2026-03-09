"""
Parser utilities for processing scraped data.
"""

import re
from typing import Dict, Any, Optional


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text string or None
        
    Returns:
        Cleaned text string
    """
    if text is None:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()


def parse_project_data(
    project_name: Optional[str] = None,
    scope: Optional[str] = None,
    owner: Optional[str] = None,
    location: Optional[str] = None,
    bid_date: Optional[str] = None,
    source: Optional[str] = None,
    url: Optional[str] = None,
    quantities: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse and structure project data into a standardized format.
    
    Args:
        project_name: Name of the project
        scope: Scope of work description
        owner: Owner/agency name
        location: Project location
        bid_date: Bid date and time
        source: Source website name
        url: Link to project page
        quantities: Project quantities if listed
        
    Returns:
        Dictionary with standardized project data
    """
    return {
        "Project Name": clean_text(project_name) or "N/A",
        "Scope": clean_text(scope) or "N/A",
        "Owner": clean_text(owner) or "N/A",
        "Location": clean_text(location) or "N/A",
        "Bid Date": clean_text(bid_date) or "N/A",
        "Source": clean_text(source) or "N/A",
        "URL": clean_text(url) or "N/A",
        "Quantities": clean_text(quantities) or "N/A",
    }


def extract_date(text: Optional[str]) -> Optional[str]:
    """
    Extract date information from text.
    
    Args:
        text: Text containing date information
        
    Returns:
        Extracted date string or None
    """
    if not text:
        return None
    
    # Common date patterns
    date_patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # MM/DD/YYYY or MM-DD-YYYY
        r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',   # YYYY/MM/DD or YYYY-MM-DD
        r'[A-Za-z]+ \d{1,2}, \d{4}',      # Month DD, YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None
