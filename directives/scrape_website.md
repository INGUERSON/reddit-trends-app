# Website Scrape Directive

## Goal
Retrieve and extract clean markdown or structured data from any given webpage without relying on complex browser automation unless necessary. This is primarily used by Coruja-bot to bypass standard API constraints (like Reddit's constraints) or to rapidly parse niche content.

## Inputs
- **Target URL**: The web address to be scraped (e.g., `https://www.reddit.com/r/automation/`).
- **Mode**: Can be `scrape` (single page) or `crawl` (spider through links).
- **Format**: `markdown` (default) or `json` (if looking for structured output).

## Tools
- `execution/scrape_single_site.py`

## Process
1. **Initialize App**: Read the `.env` file for the `FIRECRAWL_API_KEY`.
2. **Execute Scraper**: Run `scrape_single_site.py` passing the `URL` as an argument.
3. **Parse Result**: The script uses the Firecrawl API to extract content, bypassing captchas and JS-rendering automatically.
4. **Output**: Save the retrieved metadata and markdown content into the `.tmp/` directory for analytical processing.

## Output Format
A Markdown or JSON payload saved in `.tmp/` (e.g., `.tmp/scraped_data_<timestamp>.md`).
The payload contains:
- The Page Title
- Meta Description
- Full Markdown textual content
