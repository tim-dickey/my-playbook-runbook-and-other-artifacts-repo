#!/usr/bin/env python3
"""
Generate a daily AI news summary using the Perplexity API
and write it to daily-ai-summary/YYYY/MM/YYYY-MM-DD.md
"""

import os
import requests
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.environ["PERPLEXITY_API_KEY"]
API_URL = "https://api.perplexity.ai/chat/completions"

SYSTEM_PROMPT = """You are an expert AI analyst. Produce a comprehensive daily morning briefing 
of global artificial intelligence news in clean markdown format. Organize with these sections:
1. Geopolitics & Policy
2. Business & Funding
3. R&D & AGI Timeline
4. New Research Highlights
5. Hardware & Semiconductors
6. Materials Science for AI
7. One to Watch

Be factual, cite sources inline where possible, and keep each section 2-4 paragraphs.
Format the output as a markdown document with H2 headers for each section.
"""

USER_PROMPT = """Daily morning summary of global artificial intelligence news, covering 
business-related AI topics, research and development (R&D), newly published AI research papers, 
engineering developments, materials science breakthroughs relevant to AI hardware and computation, 
and any related news that could influence or impact artificial intelligence. 
Today's date: {date}"""

def generate_summary(date_str: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT.format(date=date_str)}
        ],
        "temperature": 0.2,
        "max_tokens": 4000,
        "search_recency_filter": "day"
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    year = now.strftime("%Y")
    month = now.strftime("%m")

    print(f"Generating AI summary for {date_str}...")
    summary = generate_summary(date_str)

    # Build header
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    day_num = now.strftime("%-d")
    header = f"# Daily AI Summary \u2014 {day_name}, {month_name} {day_num}, {year}\n\n"
    footer = f"\n\n---\n\n*Summary auto-generated: {date_str} via Perplexity API (sonar-pro)*\n"
    full_content = header + summary + footer

    # Write file
    out_path = Path(f"daily-ai-summary/{year}/{month}/{date_str}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_content, encoding="utf-8")
    print(f"Summary written to {out_path}")

if __name__ == "__main__":
    main()
