"""
Main script for construction bid automation scraper.

This script orchestrates the scraping process:
1. Loads keyword list
2. Calls each site scraper
3. Collects all project listings
4. Filters listings by keywords
5. Returns structured results as a pandas DataFrame
6. Exports results to Excel file
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
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
        pandas DataFrame with standardized columns matching Excel structure
    """
    if not projects:
        # Return empty DataFrame with correct columns
        columns = [
            "Bid Date & Time",
            "Bid Date",
            "Bid Time",
            "Timezone",
            "Scope",
            "Project Name",
            "Project Location",
            "Owner",
            "GCs",
            "Quantities",
            "Time Constraints",
            "Distance (Miles & Time)",
            "Site Access",
            "Competition",
            "Addendums",
            "Wage Type",
            "Website Link",
            "Source Website",
            "Matched Keywords",
            "RelevanceScore",
            "AutomationKey",
            "LastSeen"
        ]
        return pd.DataFrame(columns=columns)
    
    df = pd.DataFrame(projects)
    
    # Ensure all required columns exist
    required_columns = [
        "Bid Date & Time",
        "Bid Date",
        "Bid Time",
        "Timezone",
        "Scope",
        "Project Name",
        "Project Location",
        "Owner",
        "GCs",
        "Quantities",
        "Time Constraints",
        "Distance (Miles & Time)",
        "Site Access",
        "Competition",
        "Addendums",
        "Wage Type",
        "Website Link",
        "Source Website",
        "Matched Keywords",
        "RelevanceScore",
        "AutomationKey",
        "LastSeen"
    ]
    
    for col in required_columns:
        if col not in df.columns:
            if col == "RelevanceScore":
                df[col] = 0
            else:
                df[col] = "N/A"
    
    # Reorder columns
    df = df[required_columns]
    
    return df


def load_existing_excel(filepath: str) -> pd.DataFrame:
    """
    Load existing Excel file if it exists.
    
    Args:
        filepath: Path to Excel file
        
    Returns:
        DataFrame with existing data or empty DataFrame
    """
    if os.path.exists(filepath):
        try:
            return pd.read_excel(filepath, engine='openpyxl')
        except Exception as e:
            print(f"Warning: Could not load existing Excel file: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def merge_with_existing(new_df: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge new projects with existing ones, updating duplicates.
    
    Args:
        new_df: New projects DataFrame
        existing_df: Existing projects DataFrame
        
    Returns:
        Merged DataFrame with duplicates handled
    """
    if existing_df.empty:
        return new_df
    
    if new_df.empty:
        return existing_df
    
    # Ensure AutomationKey column exists
    if 'AutomationKey' not in existing_df.columns:
        return new_df
    
    # Find duplicates by AutomationKey
    existing_keys = set(existing_df['AutomationKey'].values)
    new_keys = set(new_df['AutomationKey'].values)
    
    # Update existing records (update LastSeen)
    duplicate_keys = existing_keys & new_keys
    if duplicate_keys:
        # Update LastSeen for existing records
        mask = existing_df['AutomationKey'].isin(duplicate_keys)
        from utils.parser import get_current_timestamp
        existing_df.loc[mask, 'LastSeen'] = get_current_timestamp()
    
    # Add new records (not in existing)
    new_records = new_df[~new_df['AutomationKey'].isin(existing_keys)]
    
    # Combine: existing (with updates) + new records
    if not new_records.empty:
        merged_df = pd.concat([existing_df, new_records], ignore_index=True)
    else:
        merged_df = existing_df.copy()
    
    return merged_df


def export_to_excel(df: pd.DataFrame, output_dir: str = "output", filename: Optional[str] = None, update_existing: bool = True) -> str:
    """
    Export DataFrame to Excel file with formatting.
    
    Args:
        df: DataFrame to export
        output_dir: Directory to save the Excel file
        filename: Optional filename. If None, generates timestamped filename.
        update_existing: If True, merge with existing file and update duplicates
        
    Returns:
        Path to the exported Excel file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        filename = "construction_bids.xlsx"  # Use consistent filename for updates
    
    # Ensure filename ends with .xlsx
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    
    filepath = os.path.join(output_dir, filename)
    
    # Handle existing file and deduplication
    if update_existing and os.path.exists(filepath):
        existing_df = load_existing_excel(filepath)
        df = merge_with_existing(df, existing_df)
    
    # Sort by RelevanceScore descending, then by Bid Date
    if 'RelevanceScore' in df.columns and len(df) > 1:
        df = df.sort_values(['RelevanceScore', 'Bid Date'], ascending=[False, True])
    
    # Create Excel writer with openpyxl engine
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Construction Bids', index=False)
        
        # Get the workbook and worksheet for formatting
        workbook = writer.book
        worksheet = writer.sheets['Construction Bids']
        
        # Auto-adjust column widths
        for idx, col in enumerate(df.columns, 1):
            # Get max length of content in column
            max_length = max(
                df[col].astype(str).map(len).max(),  # Max content length
                len(str(col))  # Header length
            )
            # Set column width (add some padding, max width 50)
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[worksheet.cell(1, idx).column_letter].width = adjusted_width
        
        # Freeze the header row
        worksheet.freeze_panes = 'A2'
        
        # Make header row bold
        from openpyxl.styles import Font
        header_font = Font(bold=True)
        for cell in worksheet[1]:
            cell.font = header_font
    
    return filepath


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
    
    # Filter by keywords (this also adds Matched Keywords and RelevanceScore)
    print("\n" + "=" * 60)
    print("Filtering projects by keywords...")
    print("=" * 60)
    filtered_projects = filter_projects(all_projects, keyword_list)
    
    print(f"Projects matching keywords: {len(filtered_projects)}")
    
    if filtered_projects:
        # Show keyword match statistics
        matched_keywords_count = {}
        for project in filtered_projects:
            keywords_str = project.get('Matched Keywords', '')
            if keywords_str:
                for kw in keywords_str.split(', '):
                    matched_keywords_count[kw] = matched_keywords_count.get(kw, 0) + 1
        
        if matched_keywords_count:
            print(f"\nTop matched keywords:")
            sorted_keywords = sorted(matched_keywords_count.items(), key=lambda x: x[1], reverse=True)
            for kw, count in sorted_keywords[:5]:
                print(f"  {kw}: {count} projects")
    
    # Create DataFrame
    df = create_dataframe(filtered_projects)
    
    # Display results
    if len(df) > 0:
        print("\n" + "=" * 60)
        print("Filtered Project Results")
        print("=" * 60)
        print(f"\nTotal matching projects: {len(df)}")
        print(f"\nFirst few projects:")
        print(df.head().to_string(index=False))
        
        # Export to Excel
        print("\n" + "=" * 60)
        print("Exporting to Excel...")
        print("=" * 60)
        try:
            excel_path = export_to_excel(df)
            print(f"\n✓ Successfully exported to: {excel_path}")
            print(f"  Total rows: {len(df)}")
            print(f"  Total columns: {len(df.columns)}")
        except Exception as e:
            print(f"\n✗ Error exporting to Excel: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\nNo projects matched the keyword criteria.")
        print("Excel file will not be created.")
    
    return df


if __name__ == "__main__":
    results_df = main()
