"""
Scraper for LHTAC (Local Highway Technical Assistance Council) project plans and contracts.
"""

from typing import List, Dict, Any
from .base_scraper import BaseScraper
from utils.parser import parse_project_data, extract_datetime


class LHTACScraper(BaseScraper):
    """
    Scraper for LHTAC project plans and contracts website.
    """
    
    def __init__(self):
        super().__init__(
            source_name="LHTAC",
            base_url="https://www.lhtac.org"
        )
        self.projects_url = "https://www.lhtac.org/projects-contracts"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape LHTAC website for project listings.
        
        Returns:
            List of project dictionaries
        """
        projects = []
        
        try:
            soup = self.fetch_page(self.projects_url)
            self.delay()
            
            # Example parsing structure - adjust based on actual website structure
            # This is a template that needs to be customized for the actual site
            
            # Look for project listings (adjust selectors based on actual HTML)
            project_elements = soup.find_all(['div', 'tr', 'li'], class_=lambda x: x and 'project' in x.lower())
            
            # If no specific class found, try common patterns
            if not project_elements:
                project_elements = soup.find_all('a', href=lambda x: x and ('project' in x.lower() or 'bid' in x.lower()))
            
            for element in project_elements[:20]:  # Limit to first 20 for testing
                try:
                    project_data = self._parse_project_element(element)
                    if project_data:
                        projects.append(project_data)
                except Exception as e:
                    print(f"Error parsing project element: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping LHTAC: {e}")
        
        return projects
    
    def _parse_project_element(self, element) -> Dict[str, Any]:
        """
        Parse a single project element from the HTML.
        
        Args:
            element: BeautifulSoup element containing project information
            
        Returns:
            Project dictionary or None if parsing fails
        """
        try:
            # Extract project name
            name_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a', 'span'])
            project_name = name_elem.get_text(strip=True) if name_elem else None
            
            # Extract URL
            link_elem = element.find('a', href=True)
            url = None
            if link_elem:
                href = link_elem['href']
                url = href if href.startswith('http') else f"{self.base_url}{href}"
            
            # Extract other fields based on actual site structure
            # This is a template - customize based on actual HTML structure
            scope = None
            owner = "LHTAC"
            project_location = None
            bid_date_time = None
            quantities = None
            
            # Try to find additional information in nearby elements
            parent = element.parent if element.parent else element
            text_content = parent.get_text(separator=' ', strip=True)
            
            # Try to extract bid date and time
            if text_content:
                bid_date_time = extract_datetime(text_content)
            
            return parse_project_data(
                project_name=project_name,
                scope=scope or text_content[:200],  # Use text content as scope if not found
                owner=owner,
                project_location=project_location,
                bid_date_time=bid_date_time,
                website_link=url,
                quantities=quantities
            )
        except Exception as e:
            print(f"Error in _parse_project_element: {e}")
            return None
