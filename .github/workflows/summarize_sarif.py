"""
Parses SARIF files from a directory and prints a formatted summary of the findings.

This script is designed to be used in a GitHub Actions workflow. It reads all
SARIF files from a specified directory, aggregates the results, and prints
a markdown-formatted summary that can be posted as a pull request comment.

Usage:
    python summarize_sarif.py <directory_with_sarif_files>
"""

import json
import os
import sys
from collections import defaultdict


def parse_sarif(file_path):
    """Parses a single SARIF file and returns a list of results."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sarif_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading or parsing {file_path}: {e}", file=sys.stderr)
        return []

    results = []
    for run in sarif_data.get("runs", []):
        tool_name = run.get("tool", {}).get("driver", {}).get("name", "Unknown Tool")
        for result in run.get("results", []):
            rule_id = result.get("ruleId", "N/A")
            message = result.get("message", {}).get("text", "No message")
            level = result.get("level", "note")
            locations = result.get("locations", [])
            location_str = "N/A"
            if locations:
                artifact_location = locations[0].get("physicalLocation", {}).get("artifactLocation", {})
                location_str = artifact_location.get("uri", "N/A")

            results.append({"tool": tool_name, "ruleId": rule_id, "message": message, "level": level.upper(), "location": location_str})
    return results

def main(sarif_dir):
    """Main function to process all SARIF files in a directory."""
    all_results = defaultdict(list)
    for filename in os.listdir(sarif_dir):
        if filename.endswith(".sarif"):
            file_path = os.path.join(sarif_dir, filename)
            for res in parse_sarif(file_path):
                all_results[res['tool']].append(res)

    print("## 🛡️ Container Security Scan Summary")
    for tool, results in all_results.items():
        print(f"\n### {tool} found {len(results)} issues:\n")
        print("| Severity | Rule ID | Location | Message |")
        print("|----------|---------|----------|---------|")
        for res in sorted(results, key=lambda x: x['level']):
            print(f"| {res['level']} | `{res['ruleId']}` | `{res['location']}` | {res['message'].splitlines()[0]} |")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python summarize_sarif.py <directory_with_sarif_files>", file=sys.stderr)
        sys.exit(1)