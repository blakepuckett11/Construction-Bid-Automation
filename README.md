# Construction Bid Automation Scraper

A modular Python web scraper for automatically finding construction bid opportunities that match foundation and geotechnical keywords from public infrastructure bidding websites.

## Project Overview

This tool searches multiple public works and government procurement websites for new project listings, filters them based on specific foundation construction and ground engineering keywords, and returns structured data ready for Excel export.

## Features

- **Modular Architecture**: Easy to add new website scrapers
- **Keyword Filtering**: Automatically filters projects based on foundation/geotechnical keywords
- **Structured Data Output**: Returns standardized pandas DataFrame with project information
- **Extensible Design**: Built to support future features like PDF parsing and AI extraction

## Project Structure

```
project_scraper/
├── main.py                 # Main orchestrator script
├── keywords.py             # Keyword definitions
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── scrapers/              # Website-specific scrapers
│   ├── __init__.py
│   ├── base_scraper.py    # Base scraper class
│   ├── lhtac.py          # LHTAC scraper
│   ├── idaho_dot.py      # Idaho DOT scraper
│   ├── washington_dot.py # Washington DOT scraper
│   ├── oregon_dot.py     # Oregon DOT scraper
│   ├── montana_dot.py    # Montana DOT scraper
│   ├── wyoming_dot.py    # Wyoming DOT scraper
│   └── future_sources.py # Placeholders for future sources
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── parser.py         # Data parsing utilities
│   └── filters.py        # Keyword filtering utilities
└── output/               # Output directory (for future Excel exports)
```

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python main.py
```

The script will:
1. Load the keyword list
2. Scrape all configured websites
3. Filter projects by keywords
4. Display results as a pandas DataFrame
5. Export filtered results to an Excel file in the `output/` directory

The Excel file will be automatically named with a timestamp (e.g., `construction_bids_20240115_143022.xlsx`) and includes:
- All 16 columns matching your Excel structure
- Auto-adjusted column widths
- Frozen header row
- Bold headers

## Keywords

The scraper searches for the following foundation and geotechnical keywords:

- bridge
- dewatering
- drilled shaft
- CIDH
- pile foundation
- steel pile
- micropile
- tieback
- anchor
- soil nail
- ground improvement
- jet grout
- secant pile
- soldier pile
- earth retention

## Data Structure

Each project listing includes the following columns (matching Excel structure):

- **Bid Date & Time**: Bid date and time
- **Scope**: Description of work scope
- **Project Name**: Name of the construction project
- **Project Location**: Project location
- **Owner**: Owner/agency name
- **GCs**: General contractors information
- **Quantities**: Project quantities if listed
- **Time Constraints**: Time constraints for the project
- **Distance (Miles & Time)**: Distance and travel time to project
- **Site Access**: Site access information
- **Competition**: Competition level/type
- **Addendums**: Addendums information
- **Wage Type**: Wage type (prevailing wage, etc.)
- **Website Link**: Link to project page
- **AutomationKey**: Unique identifier for the project (auto-generated)
- **LastSeen**: Timestamp when project was last seen (auto-generated)

## Current Sources

- LHTAC (Local Highway Technical Assistance Council)
- Idaho Transportation Department
- Washington State DOT
- Oregon DOT
- Montana DOT
- Wyoming DOT

## Future Sources (Placeholders)

- City government procurement portals
- Federal procurement sites (SAM.gov, etc.)
- Bid aggregators

## Adding New Scrapers

To add a new website scraper:

1. Create a new file in the `scrapers/` directory (e.g., `new_source.py`)
2. Create a class that inherits from `BaseScraper`
3. Implement the `scrape()` method
4. Add the scraper to `scrapers/__init__.py`
5. Add an instance to the `scrapers` list in `main.py`

Example:

```python
from scrapers.base_scraper import BaseScraper
from utils.parser import parse_project_data

class NewSourceScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="New Source",
            base_url="https://example.com"
        )
    
    def scrape(self):
        # Implement scraping logic
        projects = []
        # ... scraping code ...
        return projects
```

## Excel Export

The scraper automatically exports results to Excel files in the `output/` directory. Each file includes:

- **Timestamped filename**: `construction_bids_YYYYMMDD_HHMMSS.xlsx`
- **Formatted columns**: Auto-adjusted widths, frozen header row, bold headers
- **All 16 columns**: Matching your Excel spreadsheet structure
- **Filtered results**: Only projects matching foundation/geotechnical keywords

To customize the export location or filename, modify the `export_to_excel()` function call in `main.py`.

## Notes

- Website structures vary, so each scraper may need customization based on the actual HTML structure
- The scrapers include delays between requests to be respectful to servers
- Error handling is included to continue scraping even if one source fails
- Excel files are saved in the `output/` directory (created automatically if it doesn't exist)

## Dependencies

- `requests`: HTTP library for web requests
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation and DataFrame creation
- `openpyxl`: Excel file support (for future export feature)
- `lxml`: Fast XML/HTML parser

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
