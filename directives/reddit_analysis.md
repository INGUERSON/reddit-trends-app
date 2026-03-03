# Reddit Trend Analysis Directive

## Goal
Identify trending discussions and high-engagement posts in specific subreddits (r/n8n, r/automation) to understand current interests and pain points.

## Inputs
- **Subreddits**: `['n8n', 'automation']`
- **Time Filter**: `week`
- **Limit**: `100` posts per subreddit
- **Top Count**: `5` posts per subreddit

## Tools
- `execution/fetch_reddit_posts.py`

## Process
1.  **Fetch Posts**: Use the execution script to fetch the top 100 posts from the last week for each subreddit.
2.  **Filter & Sort**:
    -   Calculate an "Engagement Score" (e.g., Score + Comments).
    -   Sort by Engagement Score descending.
3.  **Extract Top 5**: Select the top 5 posts from the sorted list.
4.  **Output**: Generate a Markdown report summarizing these posts with links, titles, and engagement metrics.

## Output Format
A Markdown file (e.g., `reddit_trends_report.md`) containing:
-   **Subreddit Name**
-   **List of Top 5 Posts**:
    -   Title
    -   Link
    -   Score / Comments
    -   Brief Summary (if available/possible)
