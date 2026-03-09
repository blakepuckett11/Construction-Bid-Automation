"""
Example usage script demonstrating how to use the scraper components.

This script shows how to:
1. Use individual scrapers
2. Filter projects by keywords
3. Work with the results as a DataFrame
"""

import pandas as pd
from scrapers import IdahoDOTScraper, WashingtonDOTScraper
from utils.filters import filter_by_keywords
import keywords


def example_single_scraper():
    """Example: Scrape a single source."""
    print("Example 1: Scraping a single source")
    print("-" * 60)
    
    scraper = IdahoDOTScraper()
    projects = scraper.scrape()
    
    print(f"Found {len(projects)} projects from {scraper.get_source_name()}")
    if projects:
        print(f"\nFirst project:")
        for key, value in projects[0].items():
            print(f"  {key}: {value}")
    print()


def example_keyword_filtering():
    """Example: Filter projects by keywords."""
    print("Example 2: Filtering projects by keywords")
    print("-" * 60)
    
    # Get some sample projects (in real usage, these would come from scrapers)
    sample_projects = [
        {
            "Project Name": "Bridge Foundation Repair Project",
            "Scope": "Repair and replace bridge foundations with drilled shafts",
            "Owner": "Idaho DOT",
            "Location": "Boise, ID",
            "Bid Date": "2024-01-15",
            "Source": "Idaho DOT",
            "URL": "https://example.com/project1",
            "Quantities": "N/A"
        },
        {
            "Project Name": "Highway Resurfacing",
            "Scope": "Resurface 10 miles of highway",
            "Owner": "Idaho DOT",
            "Location": "Twin Falls, ID",
            "Bid Date": "2024-01-20",
            "Source": "Idaho DOT",
            "URL": "https://example.com/project2",
            "Quantities": "N/A"
        },
        {
            "Project Name": "Micropile Installation",
            "Scope": "Install micropiles for building foundation",
            "Owner": "City of Boise",
            "Location": "Boise, ID",
            "Bid Date": "2024-01-25",
            "Source": "City Portal",
            "URL": "https://example.com/project3",
            "Quantities": "N/A"
        }
    ]
    
    # Filter by keywords
    keyword_list = keywords.get_keywords()
    filtered = filter_by_keywords(sample_projects, keyword_list)
    
    print(f"Total projects: {len(sample_projects)}")
    print(f"Projects matching keywords: {len(filtered)}")
    print(f"\nMatching projects:")
    for project in filtered:
        print(f"  - {project['Project Name']}")
    print()


def example_dataframe():
    """Example: Convert projects to DataFrame."""
    print("Example 3: Working with DataFrames")
    print("-" * 60)
    
    sample_projects = [
        {
            "Project Name": "Bridge Foundation Project",
            "Scope": "Drilled shaft foundation installation",
            "Owner": "Idaho DOT",
            "Location": "Boise, ID",
            "Bid Date": "2024-01-15",
            "Source": "Idaho DOT",
            "URL": "https://example.com/project1",
            "Quantities": "N/A"
        }
    ]
    
    df = pd.DataFrame(sample_projects)
    print("DataFrame:")
    print(df.to_string(index=False))
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Construction Bid Scraper - Usage Examples")
    print("=" * 60)
    print()
    
    # Note: These examples use sample data to avoid making actual web requests
    # In production, you would use the actual scrapers
    
    example_keyword_filtering()
    example_dataframe()
    
    print("\nNote: To run actual scrapers, use main.py:")
    print("  python main.py")
