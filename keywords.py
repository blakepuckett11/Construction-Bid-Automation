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

# Keyword relevance weights for scoring
KEYWORD_WEIGHTS = {
    "bridge": 1,
    "dewatering": 2,
    "drilled shaft": 3,
    "CIDH": 3,
    "pile foundation": 3,
    "steel pile": 2,
    "micropile": 3,
    "tieback": 2,
    "anchor": 2,
    "soil nail": 2,
    "ground improvement": 3,
    "jet grout": 3,
    "secant pile": 3,
    "soldier pile": 2,
    "earth retention": 2,
}


def get_keywords():
    """
    Returns the list of foundation and geotechnical keywords.
    
    Returns:
        list: List of keyword strings
    """
    return FOUNDATION_KEYWORDS.copy()


def get_keyword_weights():
    """
    Returns the dictionary of keyword weights for relevance scoring.
    
    Returns:
        dict: Dictionary mapping keywords to their weights
    """
    return KEYWORD_WEIGHTS.copy()


def get_keyword_weight(keyword: str) -> int:
    """
    Get the weight/relevance score for a specific keyword.
    
    Args:
        keyword: Keyword to get weight for
        
    Returns:
        int: Weight value (defaults to 1 if not found)
    """
    return KEYWORD_WEIGHTS.get(keyword.lower().strip(), 1)


def normalize_keyword(keyword):
    """
    Normalize a keyword for matching (lowercase, strip whitespace).
    
    Args:
        keyword (str): Keyword to normalize
        
    Returns:
        str: Normalized keyword
    """
    return keyword.lower().strip()
