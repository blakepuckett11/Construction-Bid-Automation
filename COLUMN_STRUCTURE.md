# Column Structure Documentation

This document describes the column structure used by the construction bid scraper, matching the Excel spreadsheet format.

## Column List

The scraper populates the following columns in order:

1. **Bid Date & Time** - Bid submission date and time
2. **Scope** - Description of work scope
3. **Project Name** - Name of the construction project
4. **Project Location** - Physical location of the project
5. **Owner** - Owner/agency name
6. **GCs** - General contractors information
7. **Quantities** - Project quantities if listed
8. **Time Constraints** - Time constraints for the project
9. **Distance (Miles & Time)** - Distance and travel time to project
10. **Site Access** - Site access information
11. **Competition** - Competition level/type
12. **Addendums** - Addendums information
13. **Wage Type** - Wage type (prevailing wage, etc.)
14. **Website Link** - Link to project page
15. **AutomationKey** - Unique identifier for the project (auto-generated MD5 hash)
16. **LastSeen** - Timestamp when project was last seen (auto-generated)

## Auto-Generated Fields

### AutomationKey
- Generated automatically using MD5 hash of: `project_name|website_link|owner`
- Ensures unique identification of each project
- Used for tracking and deduplication

### LastSeen
- Automatically set to current timestamp when project is scraped
- Format: `YYYY-MM-DD HH:MM:SS`
- Used for tracking when projects were last seen

## Field Mapping in Code

When implementing scrapers, use the `parse_project_data()` function from `utils.parser`:

```python
from utils.parser import parse_project_data

project_data = parse_project_data(
    project_name="Project Name",
    scope="Scope description",
    owner="Owner Name",
    project_location="City, State",
    bid_date_time="2024-01-15 10:00 AM",
    website_link="https://example.com/project",
    quantities="1000 CY",
    gcs="GC Information",  # Optional
    time_constraints="Time constraints",  # Optional
    distance="50 miles, 1 hour",  # Optional
    site_access="Access info",  # Optional
    competition="Competition level",  # Optional
    addendums="Addendum info",  # Optional
    wage_type="Prevailing Wage"  # Optional
)
```

## Default Values

If a field is not available or not provided:
- Most fields default to `"N/A"`
- `AutomationKey` is always auto-generated
- `LastSeen` is always auto-generated with current timestamp

## Notes

- All scrapers should use `parse_project_data()` to ensure consistent formatting
- Fields marked as "Optional" can be omitted and will default to "N/A"
- The `extract_datetime()` function can help extract bid dates from text
- Column order matches Excel spreadsheet structure for easy export
