"""
Keywords module for construction bid filtering.

This module contains the list of keywords related to foundation construction
and ground engineering that will be used to filter project listings.
"""

# Foundation and geotechnical keywords to search for
FOUNDATION_KEYWORDS = [
    "bridge",
    "dewatering",
    "drilled shaft",
    "CIDH",
    "pile foundation",
    "steel pile",
    "micropile",
    "tieback",
    "anchor",
    "soil nail",
    "ground improvement",
    "jet grout",
    "secant pile",
    "soldier pile",
    "earth retention",
]


def get_keywords():
    """
    Returns the list of foundation and geotechnical keywords.
    
    Returns:
        list: List of keyword strings
    """
    return FOUNDATION_KEYWORDS.copy()


def normalize_keyword(keyword):
    """
    Normalize a keyword for matching (lowercase, strip whitespace).
    
    Args:
        keyword (str): Keyword to normalize
        
    Returns:
        str: Normalized keyword
    """
    return keyword.lower().strip()
