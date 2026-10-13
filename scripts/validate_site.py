#!/usr/bin/env python3
"""Validate the production static site using only the Python standard library."""
from __future__ import annotations
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

PAGES = (
    'index.html', 'services.html', 'articles.html', 'about.html', 'contact.html',
    'moving.html', 'maintenance.html', 'air-conditioning.html', 'cleaning.html',
    'gas-ovens.html', 'faq.html', 'process.html', 'privacy.html',
)
BASE = 'https://abdo-q.github.io/alkhayal-website/'
NAV = {
    'index.html': 'الرئيسية', 'services.html': 'الخدمات', 'about.html': 'من نحن',
    'articles.html': 'المقالات', 'faq.html': 'الأسئلة الشائعة',
    'process.html': 'كيف نعمل', 'contact.html': 'تواصل معنا',
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ''
        self.in_title = False
        self.description = ''
        self.canonical = ''
        self.meta: dict[str, str] = {}
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.refs: list[str] = []
        self.images: list[tuple[str, str]] = []
        self.nav_links: list[tuple[str, str]] = []
        self.nav_depth = 0
        self.current_anchor: list[str] | None = None
        self.schemas: list[str] = []
        self.in_schema = False
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if d.get('id'):
            self.ids.add(d['id'])
        if tag == 'title':
            self.in_title = True
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'meta':
            if d.get('name') == 'description':
                self.description = d.get('content', '') or ''
            key = d.get('property') or d.get('name')
            if key:
                self.meta[key] = d.get('content', '') or ''
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonical = d.get('href', '') or ''
        if tag == 'nav' and d.get('aria-label') == 'التنقل الرئيسي':
            self.nav_depth += 1
        if tag == 'a':
            self.current_anchor = [d.get('href', '') or '', '']
        for attr in ('src', 'poster'):
            if d.get(attr):
                self.refs.append(d[attr] or '')
        if tag == 'img':
            self.images.append((d.get('src', '') or '', d.get('alt', '') or ''))
        if tag in ('a', 'link') and d.get('href'):
            self.links.append(d['href'] or '')
        if tag == 'script' and d.get('type') == 'application/ld+json':
            self.in_schema = True
            self.schemas.append('')

    def handle_endtag(self, tag: str) -> None:
        if tag == 'title':
            self.in_title = False
        if tag == 'nav' and self.nav_depth:
            self.nav_depth -= 1
        if tag == 'a' and self.current_anchor is not None:
            href, label = self.current_anchor
            if self.nav_depth:
                self.nav_links.append((href, ' '.join(label.split())))
            self.current_anchor = None
        if tag == 'script' and self.in_schema:
            self.in_schema = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.current_anchor is not None:
            self.current_anchor[1] += data
        if self.in_schema and self.schemas:
            self.schemas[-1] += data


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    parsed: dict[str, PageParser] = {}
    for name in PAGES:
        path = root / name
        if not path.is_file():
            fail(errors, f'{name}: required page missing')
            continue
        p = PageParser()
        try:
            p.feed(path.read_text(encoding='utf-8'))
        except Exception as exc:
            fail(errors, f'{name}: HTML parsing failed: {exc}')
            continue
        parsed[name] = p
        if not p.title.strip():
            fail(errors, f'{name}: title is empty')
        if not p.description.strip():
            fail(errors, f'{name}: meta description is empty')
        expected_url = BASE if name == 'index.html' else BASE + name
        if p.canonical != expected_url:
            fail(errors, f'{name}: canonical should be {expected_url}, got {p.canonical or "(missing)"}')
        for key in ('og:title', 'og:description', 'og:url', 'og:image', 'twitter:card'):
            if not p.meta.get(key):
                fail(errors, f'{name}: missing {key}')
        if p.meta.get('og:url') != expected_url:
            fail(errors, f'{name}: og:url must match its canonical URL')
        if p.h1_count != 1:
            fail(errors, f'{name}: expected exactly one h1, found {p.h1_count}')
        if name == 'services.html' and 'خدمات' not in p.title:
            fail(errors, 'services.html: title does not identify the services page')
        if name == 'articles.html' and 'مقالات' not in p.title:
            fail(errors, 'articles.html: title does not identify the articles page')
        if not p.nav_links:
            fail(errors, f'{name}: primary navigation is missing')
        elif len(p.nav_links) != len(NAV) or dict(p.nav_links) != NAV:
            fail(errors, f'{name}: primary navigation labels/targets do not match the site map')
        if not p.schemas:
            fail(errors, f'{name}: LocalBusiness JSON-LD is missing')
        else:
            for schema in p.schemas:
                try:
                    parsed_schema = json.loads(schema)
                    if parsed_schema.get('@type') != 'LocalBusiness':
                        fail(errors, f'{name}: JSON-LD is not LocalBusiness')
                except Exception as exc:
                    fail(errors, f'{name}: invalid JSON-LD: {exc}')
        for src, alt in p.images:
            if not alt.strip():
                fail(errors, f'{name}: image {src or "(no src)"} has no alt text')
        for ref in p.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc or not u.path:
                continue
            target = (path.parent / u.path).resolve()
            if not target.is_file():
                fail(errors, f'{name}: missing local resource {ref}')
        for href in p.links:
            u = urlsplit(href)
            if u.scheme or u.netloc:
                continue
            target_name = u.path or name
            target = (path.parent / target_name).resolve()
            if not target.is_file():
                fail(errors, f'{name}: broken local link {href}')
                continue
            if u.fragment and target.suffix.lower() == '.html':
                target_page = parsed.get(target.name)
                if target_page is None:
                    target_page = PageParser()
                    target_page.feed(target.read_text(encoding='utf-8'))
                    parsed[target.name] = target_page
                if u.fragment not in target_page.ids:
                    fail(errors, f'{name}: broken fragment {href}')

    # Verify every route and sitemap URL points to exactly the published page set.
    routes_path = root / 'manus-routes.json'
    sitemap_path = root / 'sitemap.xml'
    if routes_path.is_file():
        try:
            routes = json.loads(routes_path.read_text(encoding='utf-8'))['routes']
            route_paths = {item['path'] for item in routes}
            expected_paths = {'/' if n == 'index.html' else '/' + n for n in PAGES}
            if route_paths != expected_paths:
                fail(errors, f'manus-routes.json: routes differ from production pages (missing={sorted(expected_paths-route_paths)}, extra={sorted(route_paths-expected_paths)})')
            else:
                titles_by_path = {item['path']: item.get('title', '') for item in routes}
                for name, page in parsed.items():
                    route = '/' if name == 'index.html' else '/' + name
                    if titles_by_path.get(route) != page.title.strip():
                        fail(errors, f'manus-routes.json: title for {route} does not match the HTML title')
        except Exception as exc:
            fail(errors, f'manus-routes.json: invalid JSON: {exc}')
    else:
        fail(errors, 'manus-routes.json: missing')
    if sitemap_path.is_file():
        try:
            tree = ET.parse(sitemap_path)
            urls = {el.text or '' for el in tree.getroot().iter() if el.tag.endswith('loc')}
            expected_urls = {BASE if n == 'index.html' else BASE + n for n in PAGES}
            if urls != expected_urls:
                fail(errors, f'sitemap.xml: URLs differ from production pages (missing={sorted(expected_urls-urls)}, extra={sorted(urls-expected_urls)})')
        except Exception as exc:
            fail(errors, f'sitemap.xml: invalid XML: {exc}')
    else:
        fail(errors, 'sitemap.xml: missing')

    if 'index.html' in parsed:
        home = (root / 'index.html').read_text(encoding='utf-8')
        if 'fetchpriority="high"' not in home or 'loading="eager"' not in home:
            fail(errors, 'index.html: hero image must use high fetch priority and eager loading')
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1], help='site source or built output directory')
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        raise SystemExit(1)
    print(f'Validation passed: {len(PAGES)} production pages, links, metadata, JSON-LD, routes, and sitemap are consistent.')


if __name__ == '__main__':
    main()
