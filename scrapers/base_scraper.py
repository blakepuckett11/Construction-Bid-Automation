"""
Base scraper class for all website scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import time


class BaseScraper(ABC):
    """
    Base class for all website scrapers.
    
    Provides common functionality for making requests, parsing HTML,
    and handling errors. Each specific scraper should inherit from this class.
    """
    
    def __init__(self, source_name: str, base_url: str):
        """
        Initialize the base scraper.
        
        Args:
            source_name: Name of the source website
            base_url: Base URL of the website
        """
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: str, timeout: int = 30) -> BeautifulSoup:
        """
        Fetch a web page and return parsed BeautifulSoup object.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object of the parsed HTML
            
        Raises:
            requests.RequestException: If the request fails
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            raise
    
    def delay(self, seconds: float = 1.0):
        """
        Add a delay between requests to be respectful to the server.
        
        Args:
            seconds: Number of seconds to delay
        """
        time.sleep(seconds)
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape the website and return a list of project dictionaries.
        
        Each dictionary should have the following keys:
        - Project Name
        - Scope
        - Owner
        - Location
        - Bid Date
        - Source
        - URL
        - Quantities
        
        Returns:
            List of project dictionaries
        """
        pass
    
    def get_source_name(self) -> str:
        """
        Get the source website name.
        
        Returns:
            Source name string
        """
        return self.source_name
