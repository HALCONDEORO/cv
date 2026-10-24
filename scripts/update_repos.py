#!/usr/bin/env python3
"""Refresh the auto-generated 'top repos' block in index.html.
Fetches the account's top public repos by stars and rewrites ONLY the
marked block. Hand-written content is never touched.
Usage: python3 scripts/update_repos.py index.html [--check]
"""
import json, re, sys, urllib.request

USER = "HALCONDEORO"
BEGIN = "<!-- TOPREPOS:BEGIN -->"
END = "<!-- TOPREPOS:END -->"

def fetch_repos():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=updated",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "cv-updater"})
    with urllib.request.urlopen(req, timeout=30) as r:
        repos = json.load(r)
    repos = [r for r in repos if not r.get("fork") and r["name"] != USER]
    repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return repos[:5]

def render_block(repos):
    items = []
    for r in repos:
        desc = (r.get("description") or "").strip()
        items.append(
            f'  <div class="proj"><span class="name"><a href="{r["html_url"]}">{r["name"]}</a></span>'
            f' <span class="stars">({r.get("stargazers_count", 0)} stars)</span>'
            + (f' - {desc}' if desc else '') + '</div>')
    body = "\n".join(items) if items else "  <!-- no repos found -->"
    return f'{BEGIN}\n<p class="muted-small">Top public repositories by stars (auto-updated):</p>\n{body}\n{END}'

def main():
    path = sys.argv[1]
    check = "--check" in sys.argv
    html = open(path, encoding="utf-8").read()
    new_block = render_block(fetch_repos())
    pattern = re.compile(re.escape(BEGIN) + ".*?" + re.escape(END), re.S)
    if not pattern.search(html):
        print("markers not found; nothing to do"); return 0
    updated = pattern.sub(lambda _: new_block, html)
    if check:
        if updated != html:
            print("STALE: top-repos block is behind"); return 1
        print("up to date"); return 0
    if updated != html:
        open(path, "w", encoding="utf-8").write(updated)
        print("updated")
    else:
        print("no change")
    return 0

if __name__ == "__main__":
    sys.exit(main())
