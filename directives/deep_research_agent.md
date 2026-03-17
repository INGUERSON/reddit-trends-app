# Deep Research Agent Directive

## Goal

Conduct deep, multi-layered research on any given niche to extract pain points, trends, competitors, and high-value opportunities for sales and product development.

## Inputs

- **Niche/Topic**: The core subject (e.g., "Beauty products for women").
- **Depth**: `shallow` (top results), `deep` (inner pages and sub-links).
- **Format**: `markdown` or `json`.

## Tools

- `execution/deep_research_engine.py`: The core script that orchestrates the Firecrawl API to crawl and scrape.

## Process
1. **Identify High-Value URLs**: Start by identifying 3-5 authority sites or forums in the given niche.
2. **Crawl & Extract**: Use Firecrawl to crawl the root URLs with a depth of 1 or 2, specifically targeting product reviews, complaints, and feature wishlists.
3. **Structured Breakdown**:

    - **Pain Points**: What are users complaining about?
    - **Trends**: What is "hot" right now in the niche?
    - **Competitors**: Who are the main players being discussed?
    - **Sales Angle**: How can we position a solution for this?

4. **Synthesis**: Save raw markdown in `.tmp/` and generate a concise executive summary.

## Output Format

- **Dossier**: A comprehensive Markdown file in `.tmp/deep_research_<niche>_<timestamp>.md`.
- **Actionable Insights**: A ready-to-use summary for sales outreach or copywriting.
