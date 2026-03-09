"""
Parser utilities for processing scraped data.
"""

import re
import hashlib
from datetime import datetime
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


def generate_automation_key(project_name: str, url: str, owner: str = "") -> str:
    """
    Generate a unique automation key for a project.
    
    Args:
        project_name: Name of the project
        url: Project URL
        owner: Owner/agency name
        
    Returns:
        Unique hash string for the project
    """
    # Combine project name, URL, and owner to create unique key
    key_string = f"{project_name}|{url}|{owner}"
    return hashlib.md5(key_string.encode()).hexdigest()


def get_current_timestamp() -> str:
    """
    Get current timestamp in a standard format.
    
    Returns:
        Current date/time as string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_project_data(
    project_name: Optional[str] = None,
    scope: Optional[str] = None,
    owner: Optional[str] = None,
    project_location: Optional[str] = None,
    bid_date_time: Optional[str] = None,
    website_link: Optional[str] = None,
    quantities: Optional[str] = None,
    gcs: Optional[str] = None,
    time_constraints: Optional[str] = None,
    distance: Optional[str] = None,
    site_access: Optional[str] = None,
    competition: Optional[str] = None,
    addendums: Optional[str] = None,
    wage_type: Optional[str] = None,
    automation_key: Optional[str] = None,
    last_seen: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse and structure project data into a standardized format.
    
    Args:
        project_name: Name of the project
        scope: Scope of work description
        owner: Owner/agency name
        project_location: Project location
        bid_date_time: Bid date and time
        website_link: Link to project page
        quantities: Project quantities if listed
        gcs: General contractors information
        time_constraints: Time constraints for the project
        distance: Distance (miles & time) to project
        site_access: Site access information
        competition: Competition level/type
        addendums: Addendums information
        wage_type: Wage type (prevailing wage, etc.)
        automation_key: Unique automation key (auto-generated if not provided)
        last_seen: Last seen timestamp (auto-generated if not provided)
        
    Returns:
        Dictionary with standardized project data matching Excel column structure
    """
    # Clean inputs
    clean_name = clean_text(project_name) or "N/A"
    clean_url = clean_text(website_link) or "N/A"
    clean_owner = clean_text(owner) or "N/A"
    
    # Generate automation key if not provided
    if not automation_key:
        automation_key = generate_automation_key(clean_name, clean_url, clean_owner)
    
    # Set last seen timestamp if not provided
    if not last_seen:
        last_seen = get_current_timestamp()
    
    return {
        "Bid Date & Time": clean_text(bid_date_time) or "N/A",
        "Scope": clean_text(scope) or "N/A",
        "Project Name": clean_name,
        "Project Location": clean_text(project_location) or "N/A",
        "Owner": clean_owner,
        "GCs": clean_text(gcs) or "N/A",
        "Quantities": clean_text(quantities) or "N/A",
        "Time Constraints": clean_text(time_constraints) or "N/A",
        "Distance (Miles & Time)": clean_text(distance) or "N/A",
        "Site Access": clean_text(site_access) or "N/A",
        "Competition": clean_text(competition) or "N/A",
        "Addendums": clean_text(addendums) or "N/A",
        "Wage Type": clean_text(wage_type) or "N/A",
        "Website Link": clean_url,
        "AutomationKey": automation_key,
        "LastSeen": last_seen,
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


def extract_datetime(text: Optional[str]) -> Optional[str]:
    """
    Extract date and time information from text.
    
    Args:
        text: Text containing date and time information
        
    Returns:
        Extracted date and time string or None
    """
    if not text:
        return None
    
    # Date and time patterns
    datetime_patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?',  # MM/DD/YYYY HH:MM
        r'\d{4}[/-]\d{1,2}[/-]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?',   # YYYY-MM-DD HH:MM
        r'[A-Za-z]+ \d{1,2}, \d{4}\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?',      # Month DD, YYYY HH:MM
    ]
    
    for pattern in datetime_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    # Fall back to date only
    return extract_date(text)
