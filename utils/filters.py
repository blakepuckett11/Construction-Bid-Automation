"""
Filter utilities for keyword matching and project filtering.
"""

from typing import List, Dict, Any, Tuple
import keywords


def contains_keyword(text: str, keyword_list: List[str] = None) -> bool:
    """
    Check if text contains any of the keywords (case-insensitive).
    
    Args:
        text: Text to search in
        keyword_list: List of keywords to search for. If None, uses default keywords.
        
    Returns:
        True if any keyword is found, False otherwise
    """
    if not text:
        return False
    
    if keyword_list is None:
        keyword_list = keywords.get_keywords()
    
    text_lower = text.lower()
    
    for keyword in keyword_list:
        normalized_keyword = keywords.normalize_keyword(keyword)
        if normalized_keyword in text_lower:
            return True
    
    return False


def get_matching_keywords(text: str, keyword_list: List[str] = None) -> List[str]:
    """
    Get list of keywords that match in the given text.
    
    Args:
        text: Text to search in
        keyword_list: List of keywords to search for. If None, uses default keywords.
        
    Returns:
        List of matching keywords (preserves original case)
    """
    if not text:
        return []
    
    if keyword_list is None:
        keyword_list = keywords.get_keywords()
    
    matches = []
    text_lower = text.lower()
    
    # Sort keywords by length (longest first) to match multi-word keywords first
    sorted_keywords = sorted(keyword_list, key=len, reverse=True)
    
    for keyword in sorted_keywords:
        normalized_keyword = keywords.normalize_keyword(keyword)
        if normalized_keyword in text_lower:
            # Avoid duplicates and substrings
            if keyword not in matches:
                # Check if this keyword is a substring of an already matched keyword
                is_substring = False
                for existing_match in matches:
                    if normalized_keyword in existing_match.lower() or existing_match.lower() in normalized_keyword:
                        # Keep the longer/more specific keyword
                        if len(keyword) > len(existing_match):
                            matches.remove(existing_match)
                            matches.append(keyword)
                        is_substring = True
                        break
                if not is_substring:
                    matches.append(keyword)
    
    return matches


def calculate_relevance_score(matched_keywords: List[str]) -> int:
    """
    Calculate relevance score based on matched keywords and their weights.
    
    Args:
        matched_keywords: List of matched keywords
        
    Returns:
        int: Relevance score
    """
    if not matched_keywords:
        return 0
    
    weights = keywords.get_keyword_weights()
    score = 0
    
    for keyword in matched_keywords:
        score += keywords.get_keyword_weight(keyword)
    
    return score


def filter_by_keywords(
    projects: List[Dict[str, Any]],
    keyword_list: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter projects based on keyword matches and add matched keywords and relevance scores.
    
    Checks keywords in:
    - Project name
    - Scope text
    - Project description (if available)
    
    Args:
        projects: List of project dictionaries
        keyword_list: List of keywords to filter by. If None, uses default keywords.
        
    Returns:
        Filtered list of projects that match keywords, with added 'Matched Keywords' and 'RelevanceScore' fields
    """
    if keyword_list is None:
        keyword_list = keywords.get_keywords()
    
    filtered_projects = []
    
    for project in projects:
        # Collect all text fields to search
        project_name = project.get('Project Name', '') or ''
        scope = project.get('Scope', '') or ''
        description = project.get('Description', '') or ''
        
        # Combine all searchable text
        search_text = f"{project_name} {scope} {description}".strip()
        
        # Get matching keywords
        matched_keywords = get_matching_keywords(search_text, keyword_list)
        
        # Only include projects with at least one keyword match
        if matched_keywords:
            # Add matched keywords as comma-separated string
            project['Matched Keywords'] = ', '.join(matched_keywords)
            
            # Calculate and add relevance score
            project['RelevanceScore'] = calculate_relevance_score(matched_keywords)
            
            filtered_projects.append(project)
    
    return filtered_projects
