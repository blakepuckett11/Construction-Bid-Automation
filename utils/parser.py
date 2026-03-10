"""
Parser utilities for processing scraped data.
"""

import re
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, Tuple


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


def clean_scope(scope: Optional[str], max_length: int = 500) -> str:
    """
    Clean and normalize the scope field.
    
    Removes:
    - Ellipsis (...)
    - Extra whitespace
    - Duplicate phrases
    - Limits length to max_length
    
    Args:
        scope: Raw scope text
        max_length: Maximum length for scope text
        
    Returns:
        Cleaned scope text
    """
    if not scope or scope == "N/A":
        return "N/A"
    
    # Remove ellipsis
    scope = re.sub(r'\.{2,}', ' ', str(scope))
    
    # Normalize whitespace
    scope = re.sub(r'\s+', ' ', scope)
    
    # Remove duplicate phrases (simple approach: remove repeated 3+ word phrases)
    words = scope.split()
    seen_phrases = set()
    cleaned_words = []
    
    for i in range(len(words) - 2):
        phrase = ' '.join(words[i:i+3]).lower()
        if phrase not in seen_phrases:
            seen_phrases.add(phrase)
            if i == len(words) - 3:
                cleaned_words.extend(words[i:])
        elif i < len(words) - 3:
            # Skip this phrase if it's a duplicate
            continue
    
    if not cleaned_words:
        cleaned_words = words
    
    scope = ' '.join(cleaned_words)
    
    # Limit length
    if len(scope) > max_length:
        scope = scope[:max_length].rsplit(' ', 1)[0] + '...'
    
    return scope.strip()


def extract_quantities(text: Optional[str]) -> str:
    """
    Extract meaningful quantities from text.
    
    Looks for:
    - Working days
    - Bid items
    - Linear feet
    - Pile counts
    - Structure counts
    
    Args:
        text: Text to search for quantities
        
    Returns:
        Extracted quantities string or "N/A"
    """
    if not text:
        return "N/A"
    
    text_lower = text.lower()
    quantities = []
    
    # Working days pattern
    working_days_match = re.search(r'(\d+)\s+working\s+days?', text_lower)
    if working_days_match:
        quantities.append(f"{working_days_match.group(1)} working days")
    
    # Items pattern
    items_match = re.search(r'involves\s+(\d+)\s+items?', text_lower)
    if items_match:
        quantities.append(f"{items_match.group(1)} items")
    
    # Linear feet pattern
    lf_match = re.search(r'(\d+(?:,\d+)?)\s*(?:linear\s+)?feet?\b', text_lower)
    if lf_match:
        quantities.append(f"{lf_match.group(1)} LF")
    
    # Pile counts
    pile_match = re.search(r'(\d+)\s+piles?', text_lower)
    if pile_match:
        quantities.append(f"{pile_match.group(1)} piles")
    
    # Structure counts
    struct_match = re.search(r'(\d+)\s+structures?', text_lower)
    if struct_match:
        quantities.append(f"{struct_match.group(1)} structures")
    
    # Cubic yards
    cy_match = re.search(r'(\d+(?:,\d+)?)\s*(?:CY|cubic\s+yards?)', text_lower)
    if cy_match:
        quantities.append(f"{cy_match.group(1)} CY")
    
    if quantities:
        return ', '.join(quantities)
    
    return "N/A"


def extract_location_from_text(text: Optional[str], project_name: Optional[str] = None) -> str:
    """
    Extract location information from text.
    
    Looks for:
    - County names
    - State abbreviations
    - City names
    - Highway/route numbers
    
    Args:
        text: Text to search
        project_name: Project name (also searched for location clues)
        
    Returns:
        Extracted location or "N/A"
    """
    if not text and not project_name:
        return "N/A"
    
    search_text = f"{project_name or ''} {text or ''}".lower()
    
    # Common state abbreviations
    states = {
        'wa': 'Washington', 'id': 'Idaho', 'or': 'Oregon', 
        'mt': 'Montana', 'wy': 'Wyoming', 'ca': 'California',
        'nv': 'Nevada', 'ut': 'Utah'
    }
    
    # Extract county names
    county_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+County', search_text, re.IGNORECASE)
    if county_match:
        county = county_match.group(1)
        
        # Try to determine state from context
        state = None
        for abbrev, full_name in states.items():
            if abbrev in search_text or full_name.lower() in search_text:
                state = full_name
                break
        
        if state:
            return f"{county} County, {state}"
        return f"{county} County"
    
    # Extract state from highway/route patterns
    route_match = re.search(r'(SR|US|I-|Route)\s*(\d+)', search_text, re.IGNORECASE)
    if route_match:
        # Try to infer state from route context or project name
        # This is a simplified approach - could be enhanced
        if 'washington' in search_text or 'wa' in search_text:
            return "Washington"
        elif 'idaho' in search_text or 'id' in search_text:
            return "Idaho"
        elif 'oregon' in search_text or 'or' in search_text:
            return "Oregon"
        elif 'montana' in search_text or 'mt' in search_text:
            return "Montana"
        elif 'wyoming' in search_text or 'wy' in search_text:
            return "Wyoming"
    
    return "N/A"


def normalize_owner_name(owner: Optional[str]) -> str:
    """
    Normalize owner/agency names to short identifiers.
    
    Examples:
    - Washington State Department of Transportation -> WSDOT
    - Idaho Transportation Department -> ITD
    - Oregon Department of Transportation -> ODOT
    
    Args:
        owner: Full owner name
        
    Returns:
        Normalized short identifier
    """
    if not owner or owner == "N/A":
        return "N/A"
    
    owner_lower = owner.lower().strip()
    
    # Mapping of common agency names to abbreviations
    owner_mappings = {
        'washington state department of transportation': 'WSDOT',
        'washington state dot': 'WSDOT',
        'wsdot': 'WSDOT',
        'idaho transportation department': 'ITD',
        'idaho dot': 'ITD',
        'itd': 'ITD',
        'oregon department of transportation': 'ODOT',
        'oregon dot': 'ODOT',
        'odot': 'ODOT',
        'montana department of transportation': 'MDT',
        'montana dot': 'MDT',
        'mdt': 'MDT',
        'wyoming department of transportation': 'WYDOT',
        'wyoming dot': 'WYDOT',
        'wydot': 'WYDOT',
        'local highway technical assistance council': 'LHTAC',
        'lhtac': 'LHTAC',
    }
    
    # Check for exact or partial matches
    for key, abbrev in owner_mappings.items():
        if key in owner_lower:
            return abbrev
    
    # Return original if no match found
    return owner.strip()


def split_bid_datetime(bid_datetime: Optional[str]) -> Tuple[str, str, str]:
    """
    Split bid date and time into separate components.
    
    Converts: "Wednesday, April 1, 2026 - 11:00am PDT"
    Into: ("2026-04-01", "11:00", "PDT")
    
    Args:
        bid_datetime: Combined date and time string
        
    Returns:
        Tuple of (date YYYY-MM-DD, time HH:MM, timezone)
    """
    if not bid_datetime or bid_datetime == "N/A":
        return ("N/A", "N/A", "N/A")
    
    try:
        # Try to parse common formats
        # Format: "Wednesday, April 1, 2026 - 11:00am PDT"
        datetime_match = re.search(
            r'([A-Za-z]+),\s+([A-Za-z]+)\s+(\d+),\s+(\d{4})\s*[-–]\s*(\d{1,2}):(\d{2})(am|pm)?\s*([A-Z]{2,4})?',
            bid_datetime,
            re.IGNORECASE
        )
        
        if datetime_match:
            month_name = datetime_match.group(2)
            day = datetime_match.group(3)
            year = datetime_match.group(4)
            hour = int(datetime_match.group(5))
            minute = datetime_match.group(6)
            am_pm = datetime_match.group(7)
            timezone = datetime_match.group(8) or "N/A"
            
            # Convert month name to number
            months = {
                'january': '01', 'february': '02', 'march': '03', 'april': '04',
                'may': '05', 'june': '06', 'july': '07', 'august': '08',
                'september': '09', 'october': '10', 'november': '11', 'december': '12'
            }
            month = months.get(month_name.lower(), '01')
            
            # Convert to 24-hour format
            if am_pm:
                if am_pm.lower() == 'pm' and hour != 12:
                    hour += 12
                elif am_pm.lower() == 'am' and hour == 12:
                    hour = 0
            
            date_str = f"{year}-{month}-{day.zfill(2)}"
            time_str = f"{str(hour).zfill(2)}:{minute}"
            
            return (date_str, time_str, timezone)
        
        # Try simpler date-time format: "2024-01-15 14:30"
        datetime_simple_match = re.search(
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})\s+(\d{1,2}):(\d{2})',
            bid_datetime
        )
        if datetime_simple_match:
            year = datetime_simple_match.group(1)
            month = datetime_simple_match.group(2).zfill(2)
            day = datetime_simple_match.group(3).zfill(2)
            hour = datetime_simple_match.group(4).zfill(2)
            minute = datetime_simple_match.group(5)
            date_str = f"{year}-{month}-{day}"
            time_str = f"{hour}:{minute}"
            # Try to extract timezone
            tz_match = re.search(r'([A-Z]{2,4})$', bid_datetime)
            timezone = tz_match.group(1) if tz_match else "N/A"
            return (date_str, time_str, timezone)
        
        # Try simpler date-only format
        date_match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', bid_datetime)
        if date_match:
            year = date_match.group(1)
            month = date_match.group(2).zfill(2)
            day = date_match.group(3).zfill(2)
            return (f"{year}-{month}-{day}", "N/A", "N/A")
        
    except Exception:
        pass
    
    return ("N/A", "N/A", "N/A")


def extract_source_website(url: Optional[str], owner: Optional[str] = None) -> str:
    """
    Extract source website name from URL or owner.
    
    Args:
        url: Project URL
        owner: Owner name (used as fallback)
        
    Returns:
        Source website identifier
    """
    if url and url != "N/A":
        url_lower = url.lower()
        
        # Extract from URL patterns
        if 'wsdot' in url_lower or 'washington' in url_lower:
            return 'WSDOT'
        elif 'itd.idaho' in url_lower or 'idaho' in url_lower:
            return 'ITD'
        elif 'oregon.gov/odot' in url_lower or 'odot' in url_lower:
            return 'ODOT'
        elif 'mdt.mt.gov' in url_lower or 'montana' in url_lower:
            return 'MDT'
        elif 'dot.state.wy.us' in url_lower or 'wyoming' in url_lower:
            return 'WYDOT'
        elif 'lhtac' in url_lower:
            return 'LHTAC'
        elif 'sam.gov' in url_lower:
            return 'SAM.gov'
    
    # Fallback to normalized owner name
    if owner:
        return normalize_owner_name(owner)
    
    return "N/A"


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
    clean_owner = normalize_owner_name(owner)  # Normalize owner name
    
    # Generate automation key if not provided
    if not automation_key:
        automation_key = generate_automation_key(clean_name, clean_url, clean_owner)
    
    # Set last seen timestamp if not provided
    if not last_seen:
        last_seen = get_current_timestamp()
    
    # Clean and enhance scope
    cleaned_scope = clean_scope(scope)
    
    # Extract quantities from scope if not provided
    extracted_quantities = quantities if quantities and quantities != "N/A" else extract_quantities(scope)
    
    # Improve location detection
    final_location = project_location if project_location and project_location != "N/A" else extract_location_from_text(scope, project_name)
    
    # Split bid date and time
    bid_date, bid_time, timezone = split_bid_datetime(bid_date_time)
    
    # Extract source website
    source_website = extract_source_website(clean_url, owner)
    
    return {
        "Bid Date & Time": clean_text(bid_date_time) or "N/A",  # Keep original for reference
        "Bid Date": bid_date,
        "Bid Time": bid_time,
        "Timezone": timezone,
        "Scope": cleaned_scope,
        "Project Name": clean_name,
        "Project Location": final_location,
        "Owner": clean_owner,
        "GCs": clean_text(gcs) or "N/A",
        "Quantities": extracted_quantities,
        "Time Constraints": clean_text(time_constraints) or "N/A",
        "Distance (Miles & Time)": clean_text(distance) or "N/A",
        "Site Access": clean_text(site_access) or "N/A",
        "Competition": clean_text(competition) or "N/A",
        "Addendums": clean_text(addendums) or "N/A",
        "Wage Type": clean_text(wage_type) or "N/A",
        "Website Link": clean_url,
        "Source Website": source_website,
        "Matched Keywords": "",  # Will be filled by filter function
        "RelevanceScore": 0,  # Will be filled by filter function
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
