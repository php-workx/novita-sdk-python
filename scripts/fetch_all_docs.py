#!/usr/bin/env python3
"""
Script to fetch all API documentation pages listed in api.txt
and save them for analysis.
"""

import contextlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def sanitize_filename(url: str, max_length: int = 200) -> str:
    """Sanitize a URL to create a safe filename.

    Args:
        url: The URL to sanitize
        max_length: Maximum length for the filename (default: 200)

    Returns:
        A safe filename containing only [A-Za-z0-9._-] characters
    """
    # Extract the last path component
    path = url.split("/")[-1]

    # Remove URL query parameters and fragments
    path = path.split("?")[0].split("#")[0]

    # Percent-decode the URL (e.g., %20 -> space)
    with contextlib.suppress(Exception):
        path = urllib.parse.unquote(path)

    # Replace characters not in [A-Za-z0-9._-] with underscore
    sanitized = re.sub(r"[^A-Za-z0-9._-]", "_", path)

    # Remove consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized)

    # Remove leading/trailing underscores and dots
    sanitized = sanitized.strip("_.")

    # Enforce max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip("_.")

    # Provide fallback if empty
    if not sanitized:
        sanitized = "unknown_endpoint"

    return sanitized


# Parse api.txt to extract all documentation URLs
api_txt_path = Path("./openapi/api.txt")
output_dir = Path("./docs_fetched")
output_dir.mkdir(exist_ok=True)

# Read api.txt and extract URLs
urls = []
with open(api_txt_path, encoding="utf-8") as f:
    content = f.read()
    # Extract all URLs from the markdown table
    url_pattern = r"https://novita\.ai/docs/api-reference/[^\s|)]+"
    urls = re.findall(url_pattern, content)

print(f"Found {len(urls)} documentation URLs")

# Fetch each URL
results = []
for i, url in enumerate(urls, 1):
    endpoint_name = sanitize_filename(url)
    print(f"[{i}/{len(urls)}] Fetching {endpoint_name}...")

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode("utf-8")

            # Save HTML file
            output_file = output_dir / f"{endpoint_name}.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Check if it's a valid page (not 404)
            if "Page Not Found" in html_content or "404" in html_content[:1000]:
                status = "NOT_FOUND"
            else:
                status = "SUCCESS"

            results.append(
                {"url": url, "endpoint": endpoint_name, "status": status, "file": str(output_file)}
            )
            print(f"  ✓ {status}")

    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP Error {e.code}")
        results.append(
            {"url": url, "endpoint": endpoint_name, "status": f"HTTP_{e.code}", "file": None}
        )
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append(
            {
                "url": url,
                "endpoint": endpoint_name,
                "status": "ERROR",
                "error": str(e),
                "file": None,
            }
        )

    # Be nice to the server
    time.sleep(0.5)

# Save results summary
summary_file = output_dir / "fetch_summary.json"
with open(summary_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# Print summary
success_count = sum(1 for r in results if r["status"] == "SUCCESS")
print(f"\n{'='*60}")
print(f"Summary: {success_count}/{len(results)} pages fetched successfully")
print(f"Results saved to: {output_dir}")
print(f"Summary: {summary_file}")
