#!/usr/bin/env python3
"""
Script to fetch all API documentation pages listed in api.txt
and save them for analysis.
"""

import re
import urllib.request
import urllib.error
import json
import time
from pathlib import Path

# Parse api.txt to extract all documentation URLs
api_txt_path = Path("./openapi/api.txt")
output_dir = Path("./docs_fetched")
output_dir.mkdir(exist_ok=True)

# Read api.txt and extract URLs
urls = []
with open(api_txt_path, 'r') as f:
    content = f.read()
    # Extract all URLs from the markdown table
    url_pattern = r'https://novita\.ai/docs/api-reference/[^\s|)]+'
    urls = re.findall(url_pattern, content)

print(f"Found {len(urls)} documentation URLs")

# Fetch each URL
results = []
for i, url in enumerate(urls, 1):
    endpoint_name = url.split('/')[-1]
    print(f"[{i}/{len(urls)}] Fetching {endpoint_name}...")

    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8')

            # Save HTML file
            output_file = output_dir / f"{endpoint_name}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Check if it's a valid page (not 404)
            if "Page Not Found" in html_content or "404" in html_content[:1000]:
                status = "NOT_FOUND"
            else:
                status = "SUCCESS"

            results.append({
                "url": url,
                "endpoint": endpoint_name,
                "status": status,
                "file": str(output_file)
            })
            print(f"  ✓ {status}")

    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP Error {e.code}")
        results.append({
            "url": url,
            "endpoint": endpoint_name,
            "status": f"HTTP_{e.code}",
            "file": None
        })
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append({
            "url": url,
            "endpoint": endpoint_name,
            "status": f"ERROR",
            "error": str(e),
            "file": None
        })

    # Be nice to the server
    time.sleep(0.5)

# Save results summary
summary_file = output_dir / "fetch_summary.json"
with open(summary_file, 'w') as f:
    json.dump(results, f, indent=2)

# Print summary
success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
print(f"\n{'='*60}")
print(f"Summary: {success_count}/{len(results)} pages fetched successfully")
print(f"Results saved to: {output_dir}")
print(f"Summary: {summary_file}")
