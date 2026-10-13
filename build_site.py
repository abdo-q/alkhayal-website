#!/usr/bin/env python3
"""Publish the curated static HTML source tree into ./dist.

The HTML pages are the source of truth. This script intentionally does not
regenerate page content; it copies only the production allowlist and assets.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
PAGES = (
    'index.html', 'services.html', 'articles.html', 'about.html', 'contact.html',
    'moving.html', 'maintenance.html', 'air-conditioning.html', 'cleaning.html',
    'gas-ovens.html', 'faq.html', 'process.html', 'privacy.html',
)
ROOT_FILES = ('style.css', 'logo.svg', 'site.webmanifest', 'robots.txt', 'sitemap.xml', 'manus-routes.json')


def main() -> None:
    for name in (*PAGES, *ROOT_FILES):
        if not (ROOT / name).is_file():
            raise SystemExit(f'Missing required publish file: {name}')
    if DIST.exists():
        if DIST.parent != ROOT or DIST.name != 'dist':
            raise SystemExit(f'Refusing to remove unexpected output path: {DIST}')
        shutil.rmtree(DIST)
    DIST.mkdir()
    for name in (*PAGES, *ROOT_FILES):
        shutil.copy2(ROOT / name, DIST / name)
    shutil.copytree(ROOT / 'assets', DIST / 'assets')
    print(f'Built {len(PAGES)} pages and assets into {DIST}')


if __name__ == '__main__':
    main()
