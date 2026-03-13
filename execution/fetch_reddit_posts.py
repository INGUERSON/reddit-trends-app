import praw
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'script:trend_analyzer:v1.0 (by /u/yourusername)')

def get_reddit_instance():
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("Warning: Reddit API credentials not found in .env. Using fallback JSON method.")
        return None
    
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

def analyze_subreddit(reddit, subreddit_name, limit=100, top_count=5):
    print(f"Analyzing r/{subreddit_name} via PRAW...")
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        
        # Fetch top posts from this week
        for post in subreddit.top(time_filter='week', limit=limit):
            posts.append({
                'title': post.title,
                'url': "https://www.reddit.com" + post.permalink if hasattr(post, 'permalink') else post.url,
                'score': post.score,
                'num_comments': post.num_comments,
                'engagement': post.score + post.num_comments,
                'created_utc': post.created_utc,
                'selftext': post.selftext[:200] + "..." if post.selftext else ""
            })
            
        # Sort by engagement
        posts.sort(key=lambda x: x['engagement'], reverse=True)
        
        return posts[:top_count]
    except Exception as e:
        print(f"Error fetching r/{subreddit_name}: {e}")
        return []

def analyze_subreddit_fallback(subreddit_name, limit=100, top_count=5):
    print(f"Analyzing r/{subreddit_name} via fallback JSON...")
    url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t=week&limit={limit}"
    headers = {'User-Agent': REDDIT_USER_AGENT}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            posts.append({
                'title': post.get('title', ''),
                'url': "https://www.reddit.com" + post.get('permalink', ''),
                'score': post.get('score', 0),
                'num_comments': post.get('num_comments', 0),
                'engagement': post.get('score', 0) + post.get('num_comments', 0),
                'created_utc': post.get('created_utc', 0),
                'selftext': post.get('selftext', '')[:200] + "..." if post.get('selftext') else ""
            })
            
        posts.sort(key=lambda x: x['engagement'], reverse=True)
        return posts[:top_count]
    except Exception as e:
        print(f"Error fetching r/{subreddit_name} via fallback JSON: {e}")
        print("Attempting Firecrawl scrape fallback...")
        
        # Integrate Firecrawl Scraping Fallback
        try:
            import scrape_single_site
            firecrawl_url = f"https://www.reddit.com/r/{subreddit_name}/"
            saved_file = scrape_single_site.scrape_url(firecrawl_url)
            if saved_file:
                return [{
                    'title': f"[FIRECRAWL SCRAPED] r/{subreddit_name} Data",
                    'url': firecrawl_url,
                    'score': 0,
                    'num_comments': 0,
                    'engagement': 0,
                    'created_utc': 0,
                    'selftext': f"Raw contents fetched bypassing Reddit blocks. File saved to: {saved_file}"
                }]
        except ImportError as ie:
            print(f"Firecrawl script not found for integration: {ie}")
        except Exception as fc_e:
            print(f"Firecrawl scrape also failed: {fc_e}")
            
        return []

def main():
    reddit = get_reddit_instance()
    
    subreddits = ['n8n', 'automation']
    report_data = {}

    for sub in subreddits:
        if reddit:
            top_posts = analyze_subreddit(reddit, sub)
        else:
            top_posts = analyze_subreddit_fallback(sub)
            
        report_data[sub] = top_posts

    # Output to file
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"reddit_trends_{timestamp}.md"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Reddit Trends Report ({timestamp})\n\n")
        
        for sub, posts in report_data.items():
            f.write(f"## r/{sub}\n")
            if not posts:
                f.write("No posts found or error occurred.\n\n")
                continue
                
            for i, post in enumerate(posts, 1):
                f.write(f"### {i}. {post['title']}\n")
                f.write(f"- **Engagement**: {post['engagement']} (Score: {post['score']}, Comments: {post['num_comments']})\n")
                f.write(f"- [Link]({post['url']})\n")
                if post['selftext']:
                    f.write(f"- *Snippet*: {post['selftext']}\n")
                f.write("\n")

    print(f"Report generated: {output_filename}")

if __name__ == "__main__":
    main()
