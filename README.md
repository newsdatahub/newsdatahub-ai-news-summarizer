# AI News Summarizer: NewsDataHub + OpenAI

> **Automate news summarization using NewsDataHub API and OpenAI GPT models**

Build an AI-powered pipeline that fetches news articles and generates concise, human-readable summaries in seconds. Perfect for news monitoring, content aggregation, research briefs, and automated reporting systems.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NewsDataHub](https://img.shields.io/badge/API-NewsDataHub-green.svg)](https://newsdatahub.com)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI-orange.svg)](https://platform.openai.com)

---

## ![Overview](https://img.shields.io/badge/📋-Overview-blue?style=flat-square) What This Does

**Pipeline workflow:**
1. Fetches English news articles from NewsDataHub API (or uses sample data)
2. Filters out low-quality content (< 300 characters)
3. Generates 2-3 sentence AI summaries using OpenAI GPT-4o-mini
4. Outputs structured JSON with article metadata + summaries

**Use cases:** News aggregation, automated briefings, content monitoring, research platforms, media intelligence dashboards.

**Key features:**
- ✅ Abstractive summarization (AI rewrites content naturally, not just extraction)
- ✅ Ultra-low cost (~$0.01 per 100 summaries with GPT-4o-mini)
- ✅ Sample data fallback (works without NewsDataHub API key)
- ✅ Batch processing ready (easily scale to thousands of articles)

**⚠️ AI Disclaimer:** AI-generated summaries may occasionally contain inaccuracies, omit details, or misinterpret nuanced information. Always review outputs for critical applications and treat AI as an assistive tool, not a definitive source.

---

## ![Quick Start](https://img.shields.io/badge/🚀-Quick_Start-green?style=flat-square)

### Prerequisites

- Python 3.7+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- NewsDataHub API key ([get one here](https://newsdatahub.com/login)) — **Optional:** uses sample data if not provided

### Installation

```bash
# Clone and install
git clone https://github.com/newsdatahub/newsdatahub-ai-news-summarizer.git
cd newsdatahub-ai-news-summarizer
pip install requests openai

# Configure API keys in summarizer.py
NDH_API_KEY = ""  # Optional - leave empty for sample data
OPENAI_API_KEY = "your_openai_api_key_here"  # Required

# Run
python summarizer.py

# Or use Jupyter notebook
jupyter notebook summarizer.ipynb
```

**⚠️ Security Note:** Never commit notebooks with real API keys to GitHub or share them publicly. If using Google Colab, use Colab Secrets (🔑 icon in sidebar) instead of hardcoding keys.

---

## ![Files](https://img.shields.io/badge/📂-Files-orange?style=flat-square)

| File | Description |
|------|-------------|
| `summarizer.py` | Complete Python script for command-line usage |
| `summarizer.ipynb` | Jupyter notebook with interactive code cells |
| `sample_article.json` | Example NewsDataHub article structure |
| `summarized_output.json` | Example output with AI summaries |
| `README.md` | This file — setup and usage guide |

---

## ![Example](https://img.shields.io/badge/📊-Example_Output-purple?style=flat-square)

**Input (NewsDataHub):**
```json
{
  "title": "Major Technology Breakthrough Announced in Quantum Computing",
  "source_title": "TechCrunch",
  "content": "Scientists at leading research institutions have announced...",
  "topics": ["technology", "science"]
}
```

**Output (with AI summary):**
```json
{
  "title": "Major Technology Breakthrough Announced in Quantum Computing",
  "source": "TechCrunch",
  "topics": ["technology", "science"],
  "ai_summary": "Researchers at MIT have achieved a significant breakthrough in quantum computing by developing a new error-correction technique that reduces error rates by 40%. This advancement brings quantum computers closer to commercial viability and could accelerate applications in drug discovery, climate modeling, and cryptography."
}
```

---

## ![Cost](https://img.shields.io/badge/💰-Cost_Estimation-yellow?style=flat-square)

**OpenAI (GPT-4o-mini):**
- Input: ~$0.15 per 1M tokens
- Output: ~$0.60 per 1M tokens
- **100 articles ≈ $0.01** (one cent!)

**NewsDataHub:**
- Free: 100 requests/day
- Developer: 10,000 requests/month
- See [pricing](https://newsdatahub.com/plans) for details

---

## ![Configuration](https://img.shields.io/badge/⚙️-Configuration-lightgrey?style=flat-square)

**Adjust summary length:**
```python
max_tokens=150,  # 2-3 sentences (default)
max_tokens=75,   # 1-2 sentences
max_tokens=300,  # 4-5 sentences
```

**Process more articles:**
```python
NUM_ARTICLES_TO_PROCESS = 10  # Process 10 instead of 5
```

**Filter by topic/country:**
```python
params = {
    "per_page": 100,
    "language": "en",
    "country": "US",
    "topic": "technology"
}
```

---

## ![Advanced](https://img.shields.io/badge/🛠️-Advanced_Usage-red?style=flat-square)

**Retry logic with exponential backoff:**
```python
from time import sleep

def summarize_with_retry(content, title, max_retries=3):
    for attempt in range(max_retries):
        try:
            return summarize_article(content, title)
        except Exception as e:
            if attempt < max_retries - 1:
                sleep(2 ** attempt)
                continue
            return f"Failed: {str(e)}"
```

**Cache summaries to avoid redundant calls:**
```python
import os, json

def get_cached_summary(article_id, content, title):
    cache_file = f"cache/{article_id}.json"
    if os.path.exists(cache_file):
        return json.load(open(cache_file))["summary"]
    summary = summarize_article(content, title)
    json.dump({"summary": summary}, open(cache_file, "w"))
    return summary
```

**Process non-English articles:**
```python
# Remove language filter - GPT-4o-mini auto-detects language
params = {"per_page": 100, "country": "FR,DE,ES"}
```

---

## ![Troubleshooting](https://img.shields.io/badge/🔧-Troubleshooting-orange?style=flat-square)

**"OpenAI API key not valid"**
- Verify key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Ensure billing info is added to OpenAI account

**"NewsDataHub rate limit exceeded"**
- Free tier: 100 requests/day
- Add delays: `time.sleep(1)` between requests

**"No articles with sufficient content"**
- Lower `MIN_CONTENT_LENGTH` (default: 300)
- Try different topics or date ranges

**No summaries generated**
- Verify OpenAI API key is set correctly
- Check console for error messages

---

## ![Resources](https://img.shields.io/badge/📚-Resources-blue?style=flat-square)

- [Full Tutorial](https://newsdatahub.com/learning-center/article/ai-summarization-pipeline) — Step-by-step guide
- [NewsDataHub API Docs](https://newsdatahub.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [GitHub Issues](https://github.com/newsdatahub/newsdatahub-ai-news-summarizer/issues) — Report bugs

---

## ![License](https://img.shields.io/badge/📝-License-lightgrey?style=flat-square)

MIT License - see LICENSE file for details.

---

**Ready to automate your news summarization?**

[Get NewsDataHub API Key](https://newsdatahub.com/login) | [Get OpenAI API Key](https://platform.openai.com/api-keys) | [Read Full Tutorial](https://newsdatahub.com/learning-center)
