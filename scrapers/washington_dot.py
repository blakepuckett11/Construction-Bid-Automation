"""
Scraper for Washington State DOT contracting opportunities.

Website: https://wsdot.wa.gov/business-wsdot/contracts/search-contracting-opportunities
"""

from typing import List, Dict, Any, Optional
from .base_scraper import BaseScraper
from utils.parser import parse_project_data, extract_datetime
import re


class WashingtonDOTScraper(BaseScraper):
    """
    Scraper for Washington State Department of Transportation website.
    """
    
    def __init__(self):
        super().__init__(
            source_name="Washington DOT",
            base_url="https://wsdot.wa.gov"
        )
        self.projects_url = "https://wsdot.wa.gov/business-wsdot/contracts/search-contracting-opportunities"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape Washington DOT website for project listings.
        
        Returns:
            List of project dictionaries
        """
        projects = []
        
        try:
            soup = self.fetch_page(self.projects_url)
            self.delay()
            
            # Find project cards - they have class "views-row" or contain "publication-date" div
            # Primary selector: divs with class containing "views-row"
            project_elements = soup.find_all('div', class_=lambda x: x and 'views-row' in str(x))
            
            # Fallback: find divs containing publication-date class
            if not project_elements:
                publication_divs = soup.find_all('div', class_='publication-date')
                project_elements = []
                for pub_div in publication_divs:
                    # Get the parent container that holds all project info
                    parent = pub_div.find_parent('div', class_=lambda x: x and 'views-row' in str(x))
                    if parent and parent not in project_elements:
                        project_elements.append(parent)
            
            # Another fallback: find divs with overview class (scope/description)
            if not project_elements:
                overview_divs = soup.find_all('div', class_='overview')
                project_elements = []
                for overview_div in overview_divs:
                    parent = overview_div.find_parent('div')
                    if parent and parent not in project_elements:
                        project_elements.append(parent)
            
            print(f"Found {len(project_elements)} project elements")
            
            for element in project_elements:
                try:
                    project_data = self._parse_project_element(element)
                    if project_data and project_data.get('Project Name') != 'N/A':
                        projects.append(project_data)
                except Exception as e:
                    print(f"Error parsing project element: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping Washington DOT: {e}")
            import traceback
            traceback.print_exc()
        
        return projects
    
    def _parse_project_element(self, element) -> Dict[str, Any]:
        """
        Parse a single project element from the HTML.
        
        HTML structure:
        <div class="views-row">
          <h2><a href="...">Project Name</a></h2>
          <div class="publication-date">...</div>
          <div class="contract-number">...</div>
          <div class="submittal-date">...</div>
          <div class="news-tags"><ul><li>...</li></ul></div>
          <div class="overview">Scope description</div>
        </div>
        
        Args:
            element: BeautifulSoup element containing project information
            
        Returns:
            Project dictionary or None if parsing fails
        """
        try:
            # Extract project name from h2 > a tag
            project_name = None
            h2_elem = element.find('h2')
            if h2_elem:
                link_elem = h2_elem.find('a')
                if link_elem:
                    project_name = link_elem.get_text(strip=True)
                    # Extract URL from the same link
                    url = None
                    href = link_elem.get('href', '')
                    if href:
                        url = href if href.startswith('http') else f"{self.base_url}{href}"
                else:
                    project_name = h2_elem.get_text(strip=True)
                    url = None
            else:
                # Fallback: try to find any link
                link_elem = element.find('a', href=True)
                if link_elem:
                    project_name = link_elem.get_text(strip=True)
                    href = link_elem.get('href', '')
                    url = href if href.startswith('http') else f"{self.base_url}{href}"
            
            # Extract submittal due date (bid date) from submittal-date div
            bid_date_time = None
            submittal_div = element.find('div', class_='submittal-date')
            if submittal_div:
                # Try to get the time element first (has datetime attribute)
                time_elem = submittal_div.find('time')
                if time_elem:
                    # Get the text content of the time element
                    bid_date_time = time_elem.get_text(strip=True)
                else:
                    # Fallback: get text and extract date
                    text = submittal_div.get_text(strip=True)
                    # Remove "Submittal due:" prefix
                    bid_date_time = re.sub(r'^Submittal due[:\s]+', '', text, flags=re.IGNORECASE).strip()
            
            # Extract contract number from contract-number div
            contract_number = None
            contract_div = element.find('div', class_='contract-number')
            if contract_div:
                text = contract_div.get_text(strip=True)
                # Remove "Contract number:" prefix
                contract_number = re.sub(r'^Contract number[:\s]+', '', text, flags=re.IGNORECASE).strip()
            
            # Extract county/location from news-tags div
            project_location = None
            counties = []
            tags_div = element.find('div', class_='news-tags')
            if tags_div:
                # Find all list items
                list_items = tags_div.find_all('li')
                for li in list_items:
                    text = li.get_text(strip=True)
                    # Check if it's a county (contains "County")
                    if 'County' in text:
                        counties.append(text)
                    # Also capture other location info if needed
            
            if counties:
                project_location = ', '.join(set(counties))  # Remove duplicates
            
            # Extract scope/description from overview div
            scope = None
            overview_div = element.find('div', class_='overview')
            if overview_div:
                scope = overview_div.get_text(strip=True)
            
            # Extract quantities from scope text
            quantities = None
            if scope:
                # Look for patterns like "24 items" or "30 working days"
                quantity_patterns = [
                    r'involves\s+(\d+\s+items?[^\n]*)',
                    r'(\d+\s+working\s+days?)',
                    r'(\d+\s+items?)',
                ]
                for pattern in quantity_patterns:
                    match = re.search(pattern, scope, re.IGNORECASE)
                    if match:
                        quantities = match.group(0).strip()
                        break
            
            owner = "Washington State Department of Transportation"
            
            # If we don't have a project name, skip this entry
            if not project_name:
                return None
            
            return parse_project_data(
                project_name=project_name,
                scope=scope,
                owner=owner,
                project_location=project_location,
                bid_date_time=bid_date_time,
                website_link=url or self.projects_url,
                quantities=quantities
            )
        except Exception as e:
            print(f"Error in _parse_project_element: {e}")
            import traceback
            traceback.print_exc()
            return None
