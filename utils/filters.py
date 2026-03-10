"""
Filter utilities for keyword matching and project filtering.
"""

import re
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
    
    Supports partial and fuzzy matching:
    - "structure component" matches "structure"
    - "structural work" matches "structural"
    - Case-insensitive matching
    
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
    # This ensures "bridge replacement" matches before "bridge"
    sorted_keywords = sorted(keyword_list, key=len, reverse=True)
    
    for keyword in sorted_keywords:
        normalized_keyword = keywords.normalize_keyword(keyword)
        
        # Check for exact match or partial match (word boundary aware)
        # This handles cases like "structure component" matching "structure"
        # Use word boundaries for single words, but allow partial matches for multi-word phrases
        if ' ' in normalized_keyword:
            # Multi-word keyword: check if it appears in text
            if normalized_keyword in text_lower:
                matches.append(keyword)
        else:
            # Single word: use word boundary or check if it's part of a compound word
            # Pattern: word boundary OR part of compound word (e.g., "structural" in "structural work")
            pattern = r'\b' + re.escape(normalized_keyword) + r'\b|' + re.escape(normalized_keyword)
            if re.search(pattern, text_lower):
                matches.append(keyword)
    
    # Remove duplicates and handle overlapping keywords
    # Keep the most specific (longest) keyword when there's overlap
    unique_matches = []
    for keyword in matches:
        normalized = keywords.normalize_keyword(keyword)
        is_substring = False
        
        # Check if this keyword is a substring of another matched keyword
        for existing in unique_matches:
            existing_normalized = keywords.normalize_keyword(existing)
            if normalized in existing_normalized and normalized != existing_normalized:
                # This keyword is less specific, skip it
                is_substring = True
                break
            elif existing_normalized in normalized and normalized != existing_normalized:
                # This keyword is more specific, replace the existing one
                unique_matches.remove(existing)
                unique_matches.append(keyword)
                is_substring = True
                break
        
        if not is_substring and keyword not in unique_matches:
            unique_matches.append(keyword)
    
    return unique_matches


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
    
    Scans keywords across multiple fields:
    - Project name/title
    - Scope text
    - Project description
    - Page body text (if available)
    - Additional text fields (if available)
    
    Supports partial and fuzzy matching:
    - "structure component" matches "structure"
    - "structural work" matches "structural"
    - Case-insensitive matching
    
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
        # Collect all text fields to search (multi-field scanning)
        project_name = project.get('Project Name', '') or ''
        scope = project.get('Scope', '') or ''
        description = project.get('Description', '') or ''
        page_text = project.get('Page Text', '') or ''  # Additional page body text
        overview = project.get('Overview', '') or ''  # Additional overview text
        
        # Combine all searchable text fields
        # This ensures keywords are found even if they only appear in description/scope
        search_text = f"{project_name} {scope} {description} {page_text} {overview}".strip()
        
        # Get matching keywords (supports partial/fuzzy matching)
        matched_keywords = get_matching_keywords(search_text, keyword_list)
        
        # Only include projects with at least one keyword match
        if matched_keywords:
            # Add matched keywords as comma-separated string
            project['Matched Keywords'] = ', '.join(matched_keywords)
            
            # Calculate and add relevance score
            project['RelevanceScore'] = calculate_relevance_score(matched_keywords)
            
            filtered_projects.append(project)
    
    return filtered_projects
