"""
Test script for Washington DOT scraper.

This script tests the Washington DOT scraper independently to verify it works correctly.
"""

from scrapers.washington_dot import WashingtonDOTScraper
from main import create_dataframe, export_to_excel, filter_projects
import keywords
import pandas as pd


def test_washington_dot():
    """Test the Washington DOT scraper."""
    print("=" * 60)
    print("Testing Washington DOT Scraper")
    print("=" * 60)
    
    scraper = WashingtonDOTScraper()
    print(f"\nScraper initialized")
    print(f"Source: {scraper.get_source_name()}")
    print(f"URL: {scraper.projects_url}")
    
    print("\n" + "-" * 60)
    print("Starting scrape...")
    print("-" * 60)
    
    try:
        projects = scraper.scrape()
        
        print(f"\nScraping completed!")
        print(f"Found {len(projects)} total projects")
        
        if projects:
            # Apply keyword filtering (this adds Matched Keywords and RelevanceScore)
            print("\n" + "=" * 60)
            print("Filtering by keywords...")
            print("=" * 60)
            keyword_list = keywords.get_keywords()
            filtered_projects = filter_projects(projects, keyword_list)
            
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
                    print(f"\nMatched keywords breakdown:")
                    sorted_keywords = sorted(matched_keywords_count.items(), key=lambda x: x[1], reverse=True)
                    for kw, count in sorted_keywords:
                        print(f"  {kw}: {count} project(s)")
                
                print("\n" + "=" * 60)
                print("Sample Filtered Projects:")
                print("=" * 60)
                
                # Show first 3 filtered projects
                for i, project in enumerate(filtered_projects[:3], 1):
                    print(f"\n--- Project {i} (Relevance Score: {project.get('RelevanceScore', 0)}) ---")
                    print(f"Matched Keywords: {project.get('Matched Keywords', 'N/A')}")
                    print(f"Project Name: {project.get('Project Name', 'N/A')}")
                    print(f"Scope: {project.get('Scope', 'N/A')[:150]}...")
                    print(f"Location: {project.get('Project Location', 'N/A')}")
                    print(f"Bid Date: {project.get('Bid Date', 'N/A')}")
                    print(f"Quantities: {project.get('Quantities', 'N/A')}")
                
                # Create DataFrame to verify structure
                df = create_dataframe(filtered_projects)
                print("\n" + "=" * 60)
                print("DataFrame Info:")
                print("=" * 60)
                print(f"Shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                
                print("\nFirst project in DataFrame:")
                first_project = df.iloc[0].to_dict()
                for key, value in first_project.items():
                    if value and value != "N/A" and value != 0:
                        print(f"  {key}: {str(value)[:100]}")
                
                # Show summary statistics
                print("\n" + "=" * 60)
                print("Summary:")
                print("=" * 60)
                print(f"Total projects scraped: {len(projects)}")
                print(f"Projects matching keywords: {len(filtered_projects)}")
                print(f"Projects with names: {len([p for p in filtered_projects if p.get('Project Name') != 'N/A'])}")
                print(f"Projects with bid dates: {len([p for p in filtered_projects if p.get('Bid Date') != 'N/A'])}")
                print(f"Projects with locations: {len([p for p in filtered_projects if p.get('Project Location') != 'N/A'])}")
                print(f"Projects with quantities: {len([p for p in filtered_projects if p.get('Quantities') != 'N/A'])}")
                print(f"Average relevance score: {sum(p.get('RelevanceScore', 0) for p in filtered_projects) / len(filtered_projects):.1f}")
                
                # Export to Excel
                print("\n" + "=" * 60)
                print("Exporting to Excel...")
                print("=" * 60)
                try:
                    excel_path = export_to_excel(df, filename="washington_dot_test.xlsx", update_existing=False)
                    print(f"\n✓ Successfully exported to: {excel_path}")
                    print(f"  Exported {len(df)} filtered projects")
                except Exception as e:
                    print(f"\n✗ Error exporting to Excel: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("\n⚠ No projects matched the keyword criteria.")
                print("This could mean:")
                print("1. The projects don't contain foundation/geotechnical keywords")
                print("2. The keyword matching needs adjustment")
                print("3. The website content has changed")
        else:
            print("\nNo projects found. This could mean:")
            print("1. The website structure has changed")
            print("2. The parsing logic needs adjustment")
            print("3. There are no current projects")
            print("4. Network/access issues")
            
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_washington_dot()
