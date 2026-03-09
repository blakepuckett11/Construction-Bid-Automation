"""
Scraper for Idaho Transportation Department advertised highway projects.
"""

from typing import List, Dict, Any
from .base_scraper import BaseScraper
from utils.parser import parse_project_data, extract_date


class IdahoDOTScraper(BaseScraper):
    """
    Scraper for Idaho Transportation Department website.
    """
    
    def __init__(self):
        super().__init__(
            source_name="Idaho DOT",
            base_url="https://itd.idaho.gov"
        )
        self.projects_url = "https://itd.idaho.gov/business/contracting-opportunities"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape Idaho DOT website for project listings.
        
        Returns:
            List of project dictionaries
        """
        projects = []
        
        try:
            soup = self.fetch_page(self.projects_url)
            self.delay()
            
            # Look for project listings
            # Common patterns: tables, divs with project info, links to project pages
            project_elements = soup.find_all(['tr', 'div', 'li'], class_=lambda x: x and ('project' in x.lower() or 'bid' in x.lower() or 'contract' in x.lower()))
            
            # Alternative: look for links that might lead to project pages
            if not project_elements:
                project_elements = soup.find_all('a', href=lambda x: x and ('project' in x.lower() or 'bid' in x.lower() or 'contract' in x.lower()))
            
            for element in project_elements[:20]:  # Limit for testing
                try:
                    project_data = self._parse_project_element(element)
                    if project_data:
                        projects.append(project_data)
                except Exception as e:
                    print(f"Error parsing project element: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping Idaho DOT: {e}")
        
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
            name_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a', 'strong', 'b'])
            project_name = name_elem.get_text(strip=True) if name_elem else None
            
            # Extract URL
            link_elem = element.find('a', href=True) if element.name != 'a' else element
            url = None
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                url = href if href.startswith('http') else f"{self.base_url}{href}"
            
            # Extract text content for parsing
            text_content = element.get_text(separator=' ', strip=True)
            
            # Try to extract bid date
            bid_date = extract_date(text_content)
            
            # Extract location (common patterns: "Location:", "Project Location:", etc.)
            location = None
            location_patterns = ['location:', 'project location:', 'site:']
            for pattern in location_patterns:
                if pattern in text_content.lower():
                    parts = text_content.lower().split(pattern, 1)
                    if len(parts) > 1:
                        location = parts[1].split('\n')[0].strip()[:100]
                        break
            
            owner = "Idaho Transportation Department"
            scope = text_content[:300] if text_content else None
            quantities = None
            
            return parse_project_data(
                project_name=project_name,
                scope=scope,
                owner=owner,
                location=location,
                bid_date=bid_date,
                source=self.source_name,
                url=url,
                quantities=quantities
            )
        except Exception as e:
            print(f"Error in _parse_project_element: {e}")
            return None
