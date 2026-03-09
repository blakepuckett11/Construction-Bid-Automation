"""
Filter utilities for keyword matching and project filtering.
"""

from typing import List, Dict, Any
import keywords


def contains_keyword(text: str, keyword_list: List[str]) -> bool:
    """
    Check if text contains any of the keywords (case-insensitive).
    
    Args:
        text: Text to search in
        keyword_list: List of keywords to search for
        
    Returns:
        True if any keyword is found, False otherwise
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    for keyword in keyword_list:
        normalized_keyword = keywords.normalize_keyword(keyword)
        if normalized_keyword in text_lower:
            return True
    
    return False


def filter_by_keywords(
    projects: List[Dict[str, Any]],
    keyword_list: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter projects based on keyword matches in project name or scope.
    
    Args:
        projects: List of project dictionaries
        keyword_list: List of keywords to filter by. If None, uses default keywords.
        
    Returns:
        Filtered list of projects that match keywords
    """
    if keyword_list is None:
        keyword_list = keywords.get_keywords()
    
    filtered_projects = []
    
    for project in projects:
        # Check project name and scope for keywords
        project_text = f"{project.get('Project Name', '')} {project.get('Scope', '')}"
        
        if contains_keyword(project_text, keyword_list):
            filtered_projects.append(project)
    
    return filtered_projects


def get_matching_keywords(text: str, keyword_list: List[str] = None) -> List[str]:
    """
    Get list of keywords that match in the given text.
    
    Args:
        text: Text to search in
        keyword_list: List of keywords to search for. If None, uses default keywords.
        
    Returns:
        List of matching keywords
    """
    if keyword_list is None:
        keyword_list = keywords.get_keywords()
    
    matches = []
    text_lower = text.lower()
    
    for keyword in keyword_list:
        normalized_keyword = keywords.normalize_keyword(keyword)
        if normalized_keyword in text_lower:
            matches.append(keyword)
    
    return matches
