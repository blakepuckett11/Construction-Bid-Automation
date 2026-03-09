"""
Placeholder scrapers for future sources.

This module contains placeholder classes for future website sources that will be
implemented later, such as:
- City government procurement portals
- Federal procurement sites (SAM.gov, etc.)
- Bid aggregators
"""

from typing import List, Dict, Any
from .base_scraper import BaseScraper
from utils.parser import parse_project_data


class CityGovernmentScraper(BaseScraper):
    """
    Placeholder scraper for city government procurement portals.
    
    This will be implemented when specific city portals are identified.
    """
    
    def __init__(self, city_name: str, base_url: str):
        super().__init__(
            source_name=f"{city_name} Procurement",
            base_url=base_url
        )
        self.projects_url = base_url
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Placeholder scrape method.
        
        Returns:
            Empty list until implemented
        """
        # TODO: Implement city-specific scraping logic
        print(f"City government scraper for {self.source_name} not yet implemented")
        return []


class FederalProcurementScraper(BaseScraper):
    """
    Placeholder scraper for federal procurement sites (e.g., SAM.gov).
    
    This will be implemented when federal procurement sources are integrated.
    """
    
    def __init__(self):
        super().__init__(
            source_name="Federal Procurement",
            base_url="https://sam.gov"
        )
        self.projects_url = "https://sam.gov"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Placeholder scrape method.
        
        Returns:
            Empty list until implemented
        """
        # TODO: Implement federal procurement scraping logic
        print(f"Federal procurement scraper not yet implemented")
        return []


class BidAggregatorScraper(BaseScraper):
    """
    Placeholder scraper for bid aggregator websites.
    
    This will be implemented when specific aggregator sites are identified.
    """
    
    def __init__(self, aggregator_name: str, base_url: str):
        super().__init__(
            source_name=f"{aggregator_name} Aggregator",
            base_url=base_url
        )
        self.projects_url = base_url
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Placeholder scrape method.
        
        Returns:
            Empty list until implemented
        """
        # TODO: Implement aggregator-specific scraping logic
        print(f"Bid aggregator scraper for {self.source_name} not yet implemented")
        return []
