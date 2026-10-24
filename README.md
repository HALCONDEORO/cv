# CV - Marco Tevar

One HTML file, no build. `index.html` is the whole site (inline CSS, system fonts, a 20-line language toggle). The PDF at `marco-tevar-cv.pdf` is printed from the same page on every deploy, so the two cannot drift apart.

- Bilingual ES/EN.
- `.github/workflows/pages.yml` deploys with GitHub Actions, refreshes the auto-generated top-repos block (`scripts/update_repos.py`) and prints the PDF with headless Chrome. It fails if the CV runs past three A4 pages.
- Edit `index.html` and push to `main`. To refresh the block by hand: `python3 scripts/update_repos.py index.html` (`--check` exits 1 if the page is behind).

## License

MIT (see LICENSE). Original work; architecture inspired by the single-file CV approach, no code copied.
