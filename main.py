"""
Main script for construction bid automation scraper.

This script orchestrates the scraping process:
1. Loads keyword list
2. Calls each site scraper
3. Collects all project listings
4. Filters listings by keywords
5. Returns structured results as a pandas DataFrame
"""

import pandas as pd
from typing import List, Dict, Any
import keywords
from utils.filters import filter_by_keywords
from scrapers import (
    LHTACScraper,
    IdahoDOTScraper,
    WashingtonDOTScraper,
    OregonDOTScraper,
    MontanaDOTScraper,
    WyomingDOTScraper,
)


def scrape_all_sources() -> List[Dict[str, Any]]:
    """
    Scrape all configured sources and return combined project listings.
    
    Returns:
        List of all project dictionaries from all sources
    """
    all_projects = []
    
    # Initialize all scrapers
    scrapers = [
        LHTACScraper(),
        IdahoDOTScraper(),
        WashingtonDOTScraper(),
        OregonDOTScraper(),
        MontanaDOTScraper(),
        WyomingDOTScraper(),
    ]
    
    # Scrape each source
    for scraper in scrapers:
        print(f"\nScraping {scraper.get_source_name()}...")
        try:
            projects = scraper.scrape()
            print(f"Found {len(projects)} projects from {scraper.get_source_name()}")
            all_projects.extend(projects)
        except Exception as e:
            print(f"Error scraping {scraper.get_source_name()}: {e}")
            continue
    
    return all_projects


def filter_projects(projects: List[Dict[str, Any]], keyword_list: List[str] = None) -> List[Dict[str, Any]]:
    """
    Filter projects based on keyword matches.
    
    Args:
        projects: List of project dictionaries
        keyword_list: Optional list of keywords. If None, uses default keywords.
        
    Returns:
        Filtered list of projects matching keywords
    """
    if keyword_list is None:
        keyword_list = keywords.get_keywords()
    
    filtered = filter_by_keywords(projects, keyword_list)
    return filtered


def create_dataframe(projects: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert list of project dictionaries to pandas DataFrame.
    
    Args:
        projects: List of project dictionaries
        
    Returns:
        pandas DataFrame with standardized columns
    """
    if not projects:
        # Return empty DataFrame with correct columns
        columns = [
            "Project Name",
            "Scope",
            "Owner",
            "Location",
            "Bid Date",
            "Source",
            "URL",
            "Quantities"
        ]
        return pd.DataFrame(columns=columns)
    
    df = pd.DataFrame(projects)
    
    # Ensure all required columns exist
    required_columns = [
        "Project Name",
        "Scope",
        "Owner",
        "Location",
        "Bid Date",
        "Source",
        "URL",
        "Quantities"
    ]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = "N/A"
    
    # Reorder columns
    df = df[required_columns]
    
    return df


def main():
    """
    Main execution function.
    """
    print("=" * 60)
    print("Construction Bid Automation Scraper")
    print("=" * 60)
    
    # Load keywords
    keyword_list = keywords.get_keywords()
    print(f"\nLoaded {len(keyword_list)} keywords for filtering")
    print(f"Keywords: {', '.join(keyword_list[:5])}...")
    
    # Scrape all sources
    print("\n" + "=" * 60)
    print("Scraping all sources...")
    print("=" * 60)
    all_projects = scrape_all_sources()
    
    print(f"\nTotal projects found: {len(all_projects)}")
    
    # Filter by keywords
    print("\n" + "=" * 60)
    print("Filtering projects by keywords...")
    print("=" * 60)
    filtered_projects = filter_projects(all_projects, keyword_list)
    
    print(f"Projects matching keywords: {len(filtered_projects)}")
    
    # Create DataFrame
    df = create_dataframe(filtered_projects)
    
    # Display results
    if len(df) > 0:
        print("\n" + "=" * 60)
        print("Filtered Project Results")
        print("=" * 60)
        print(f"\n{df.to_string(index=False)}")
        print(f"\nTotal matching projects: {len(df)}")
    else:
        print("\nNo projects matched the keyword criteria.")
    
    return df


if __name__ == "__main__":
    results_df = main()
