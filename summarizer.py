"""
AI News Summarizer: NewsDataHub + OpenAI

This script demonstrates how to build an AI-powered news summarization pipeline
that fetches articles from NewsDataHub and generates concise summaries using
OpenAI's GPT-4o-mini model.

Features:
- Fetches English news articles from NewsDataHub API
- Filters out low-quality content (< 300 characters)
- Generates abstractive AI summaries using OpenAI
- Processes multiple articles in batch
- Outputs structured JSON with metadata + summaries

Requirements:
    pip install requests openai

Usage:
    1. Add your API keys below
    2. Run: python summarizer.py
    3. Check summarized_articles.json for output

Author: NewsDataHub
License: MIT
"""

import requests
import json
import os
from openai import OpenAI

# ============================================================================
# CONFIGURATION
# ============================================================================

# Set your API keys here
NDH_API_KEY = ""  # NewsDataHub API key (or leave empty to use sample data)
OPENAI_API_KEY = ""  # Required for summarization

# Configuration parameters
MIN_CONTENT_LENGTH = 300  # Minimum characters for article content
NUM_ARTICLES_TO_PROCESS = 5  # Number of articles to summarize

# ============================================================================
# STEP 1: FETCH NEWS ARTICLES FROM NEWSDATAHUB
# ============================================================================

print("="*80)
print("AI NEWS SUMMARIZER: NewsDataHub + OpenAI")
print("="*80)

# Check if NewsDataHub API key is provided
if NDH_API_KEY and NDH_API_KEY != "your_ndh_api_key_here":
    print("\n✓ Using live NewsDataHub API data...")

    url = "https://api.newsdatahub.com/v1/news"
    headers = {"x-api-key": NDH_API_KEY}

    # Fetch 100 English articles (single page, no pagination)
    params = {
        "per_page": 100,
        "language": "en",  # English articles only
        "country": "US,GB,CA,AU",  # English-speaking countries
        "source_type": "mainstream_news"  # Quality sources
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    articles = data.get("data", [])
    print(f"✓ Fetched {len(articles)} English articles from NewsDataHub API")

else:
    print("\n⚠ No NewsDataHub API key provided. Loading sample data...")

    # Download sample data if not already present
    sample_file = "sample-news-data.json"

    if not os.path.exists(sample_file):
        print("  Downloading sample data from GitHub...")
        sample_url = "https://raw.githubusercontent.com/newsdatahub/newsdatahub-ai-news-summarizer/refs/heads/main/data/sample-news-data.json"
        response = requests.get(sample_url)
        response.raise_for_status()
        with open(sample_file, "w") as f:
            json.dump(response.json(), f)
        print(f"  ✓ Sample data saved to {sample_file}")

    # Load sample data
    with open(sample_file, "r") as f:
        data = json.load(f)

    # Handle both formats: raw array or API response with 'data' key
    if isinstance(data, dict) and "data" in data:
        articles = data["data"]
    elif isinstance(data, list):
        articles = data
    else:
        raise ValueError("Unexpected sample data format")

    print(f"✓ Loaded {len(articles)} articles from sample data")

# ============================================================================
# STEP 2: FILTER ARTICLES WITH SUFFICIENT CONTENT
# ============================================================================

print(f"\nFiltering articles (minimum content length: {MIN_CONTENT_LENGTH} characters)...")

filtered_articles = []
for article in articles:
    content = article.get("content", "")
    if content and len(content) >= MIN_CONTENT_LENGTH:
        filtered_articles.append(article)

print(f"✓ Kept {len(filtered_articles)} articles with sufficient content")
print(f"✗ Removed {len(articles) - len(filtered_articles)} articles with low/no content")

if len(filtered_articles) == 0:
    print("\n⚠ ERROR: No articles with sufficient content found!")
    print("  Try lowering MIN_CONTENT_LENGTH or using different filters.")
    exit(1)

# ============================================================================
# STEP 3: INITIALIZE OPENAI CLIENT & SUMMARIZATION FUNCTION
# ============================================================================

print(f"\nInitializing OpenAI client (model: gpt-4o-mini)...")

# Validate OpenAI API key
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    print("\n⚠ ERROR: OpenAI API key not set!")
    print("  Please add your OpenAI API key to the OPENAI_API_KEY variable.")
    print("  Get your key at: https://platform.openai.com/api-keys")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

print("✓ OpenAI client initialized")


def summarize_article(content, title):
    """
    Generate an abstractive summary of a news article using OpenAI GPT-4o-mini.

    Args:
        content (str): The full article content
        title (str): The article title (provides context to the AI)

    Returns:
        str: A 2-3 sentence summary, or error message if summarization fails
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional news summarizer. Create concise, accurate 2-3 sentence summaries that capture the key information and main points of articles."
                },
                {
                    "role": "user",
                    "content": f"Summarize this news article in 2-3 sentences:\n\nTitle: {title}\n\nContent: {content}"
                }
            ],
            max_tokens=150,  # ~100-150 words for 2-3 sentences
            temperature=0.3  # Lower temperature for consistent, focused summaries
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"Error generating summary: {str(e)}"


# ============================================================================
# STEP 4: CREATE STRUCTURED OUTPUT FUNCTION
# ============================================================================

def create_summary_output(article, summary):
    """
    Combine NewsDataHub article metadata with AI-generated summary.

    Args:
        article (dict): Original article from NewsDataHub
        summary (str): AI-generated summary

    Returns:
        dict: Structured output with metadata and summary
    """
    return {
        "id": article.get("id"),
        "title": article.get("title"),
        "source": article.get("source_title"),
        "published": article.get("pub_date"),
        "url": article.get("article_link"),
        "language": article.get("language"),
        "topics": article.get("topics", []),
        "original_content_length": len(article.get("content", "")),
        "ai_summary": summary
    }


# ============================================================================
# STEP 5: PROCESS ARTICLES AND GENERATE SUMMARIES
# ============================================================================

print("\n" + "="*80)
print(f"PROCESSING {NUM_ARTICLES_TO_PROCESS} ARTICLES")
print("="*80)

summarized_articles = []

for i, article in enumerate(filtered_articles[:NUM_ARTICLES_TO_PROCESS], 1):
    # Display progress
    title_preview = article.get("title", "N/A")[:60]
    print(f"\n[{i}/{NUM_ARTICLES_TO_PROCESS}] Processing: {title_preview}...")

    # Generate AI summary
    summary = summarize_article(
        content=article.get("content", ""),
        title=article.get("title", "")
    )

    # Create structured output
    output = create_summary_output(article, summary)
    summarized_articles.append(output)

    # Display result
    print(f"              ✓ Summary generated ({len(summary)} characters)")

print(f"\n{'='*80}")
print(f"✓ Successfully processed {len(summarized_articles)} articles")
print("="*80)

# ============================================================================
# STEP 6: SAVE RESULTS TO JSON FILE
# ============================================================================

output_file = "summarized_articles.json"

with open(output_file, "w") as f:
    json.dump(summarized_articles, f, indent=2)

print(f"\n✓ Results saved to {output_file}")
print(f"  Total articles: {len(summarized_articles)}")
print(f"  File size: {os.path.getsize(output_file):,} bytes")

# ============================================================================
# STEP 7: DISPLAY SUMMARY REPORT
# ============================================================================

print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)

for i, article in enumerate(summarized_articles, 1):
    print(f"\n📰 Article {i}")
    print(f"   Title: {article['title']}")
    print(f"   Source: {article['source']} | Published: {article['published'][:10]}")

    # Display topics if available
    if article['topics']:
        topics_str = ', '.join(article['topics'])
        print(f"   Topics: {topics_str}")

    # Display AI summary
    print(f"\n   📝 AI Summary:")
    print(f"   {article['ai_summary']}\n")

    # Display full article link
    print(f"   🔗 Read full article: {article['url']}")
    print(f"   {'-'*76}")

# ============================================================================
# FINAL OUTPUT
# ============================================================================

print(f"\n{'='*80}")
print(f"✅ Generated {len(summarized_articles)} AI summaries using NewsDataHub + OpenAI")
print(f"{'='*80}\n")

# Display cost estimation
print("💰 Estimated OpenAI API Cost:")
print("   GPT-4o-mini pricing: ~$0.15/1M input tokens, ~$0.60/1M output tokens")
print(f"   Approximate cost for {len(summarized_articles)} summaries: < $0.01")
print("\n⚠️  Reminder: AI-generated summaries may occasionally contain inaccuracies.")
print("   Always review outputs for critical applications.\n")
