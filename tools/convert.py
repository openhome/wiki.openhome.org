#!/usr/bin/env python3
"""Convert the wiki.openhome.org MediaWiki export into a Jekyll site.

Point-in-time conversion: reads export/pages.json (current revision of every
page, from api.php prop=revisions) and export/images.json + export/files/,
writes wiki/*.md and mediawiki/images/. Run in Docker with pandoc on PATH:

  see "Re-running the conversion" in README.md
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = os.path.join(ROOT, 'export')
OUT_PAGES = os.path.join(ROOT, 'wiki')
OUT_IMAGES = os.path.join(ROOT, 'mediawiki', 'images')

MAIN_PAGE = 'Oh:Overview'  # MediaWiki:Mainpage
# Real MediaWiki namespaces; "Av:", "Oh:" etc. are just titles in the main namespace.
SKIP_NAMESPACES = ('Template:', 'MediaWiki:')
# Stub or installer pages with nothing worth keeping; their URLs redirect to the main page.
DROP_TO_MAIN = {'Main Page', 'What is it', 'Temp', 'Help:Editing'}

NAV = {
    'nav_openhome': 'oh',
    'nav_openhome_av': 'ohMedia',
    'nav_openhome_ohmediaplayer': 'ohMediaPlayer',
    'nav_openhome_ohnet': 'ohNet',
}

# MediaWiki 1.16's HTML whitelist (Sanitizer.php), less tags pandoc already converts.
HTML_TAGS = set('''b del i ins u font big small sub sup h1 h2 h3 h4 h5 h6 cite code em s strike
strong tt var div center blockquote ol ul dl table caption pre ruby rt rb rp p span abbr dfn kbd
samp hr li dt dd td th tr br'''.split())

problems = []  # content was lost or broken: non-zero exit
notes = []  # mirrors the wiki's own behaviour (red links etc.)


def canonical(title):
    t = unquote(title).replace('_', ' ').strip()
    t = re.sub(r'\s+', ' ', t)
    return t[:1].upper() + t[1:] if t else t


def page_url(title):
    return '/wiki/' + quote(canonical(title).replace(' ', '_'), safe=":()_-.,!'*~")


def file_page_url(name):
    # A trailing slash builds File:X.png/index.html, so Pages serves it as HTML rather than
    # guessing image/png from the extension; Pages redirects the old slashless URL to it.
    return page_url('File:' + name) + '/'


def source_name(title):
    return re.sub(r'[^A-Za-z0-9._-]+', '_', canonical(title)).strip('_') + '.md'


def load():
    pages = json.load(open(os.path.join(EXPORT, 'pages.json')))
    images = json.load(open(os.path.join(EXPORT, 'images.json')))['query']['allimages']
    return {canonical(t): r['*'] for t, r in pages.items()}, images


def preprocess(text):
    # MediaWiki runs an unclosed <syntaxhighlight> to the end of the page; pandoc rejects it.
    unclosed = len(re.findall(r'<syntaxhighlight[\s>]', text, re.I)) - len(re.findall(r'</syntaxhighlight>', text, re.I))
    text += '\n</syntaxhighlight>' * max(unclosed, 0)
    # Multi-line <code> blocks render as preformatted text on the wiki; pandoc emits them as raw
    # HTML, which swallows the following code block when kramdown renders the page.
    text = re.sub(r'<code>\s*\n(.*?)\n\s*</code>', lambda m: '<pre>' + m.group(1) + '</pre>', text, flags=re.S | re.I)
    # pandoc sizes a wiki table from its first row and drops cells beyond it, so a leading
    # full-width title row (! colspan="N" | Title) moves above the table as a bold line.
    text = re.sub(r'(\{\|[^\n]*\n)(?:\|-[^\n]*\n)?![^\n|]*colspan="?\d+"?[^\n|]*\|\s*([^\n!]*)\n',
                  lambda m: "'''" + m.group(2).strip() + "'''\n\n" + m.group(1), text)
    # Behaviour switches such as __NOTOC__ are invisible on the wiki; pandoc keeps them as text.
    text = re.sub(r'__(NOTOC|TOC|FORCETOC|NOEDITSECTION|NEWSECTIONLINK|NOGALLERY|HIDDENCAT|INDEX|NOINDEX)__', '', text)
    # Trac-style [[br]] rendered as a red link on the wiki; the intent is a line break.
    text = re.sub(r'\[\[br\]\]', '<br>', text, flags=re.I)
    text = re.sub(r'\{\{\s*Notebox\s*\}\}', '<blockquote>', text, flags=re.I)
    text = re.sub(r'\{\{\s*Noteboxend\s*\}\}', '</blockquote>', text, flags=re.I)

    def nav(m):
        prefix = NAV[m.group(1).strip().lower().replace(' ', '_')]
        links = ' · '.join(f'[[{prefix}:{p}|{label}]]' for p, label in
                           (('What', 'What is it?'), ('How', 'How do I get it?'), ('Developer', 'Developers')))
        header = m.group(2)
        return links + (f"\n\n'''{header.strip()}'''" if header and header.strip() else '')

    text = re.sub(r'\{\{\s*(nav[ _]openhome(?:[ _](?:av|ohmediaplayer|ohnet))?)\s*(?:\|([^}]*))?\}\}',
                  nav, text, flags=re.I)
    if '{{' in text:
        problems.append(f'unexpanded template: {re.findall(r"{{[^}]*}}", text)[:3]}')
    return text


def pandoc(args, data):
    r = subprocess.run(['pandoc'] + args, input=data, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout


def walk(node, fn):
    if isinstance(node, dict):
        if 't' in node:
            fn(node)
        for v in node.values():
            walk(v, fn)
    elif isinstance(node, list):
        for v in node:
            walk(v, fn)


def stringify(inlines):
    out = []

    def collect(node):
        if node['t'] in ('Str', 'Code'):
            out.append(node['c'] if node['t'] == 'Str' else node['c'][1])
        elif node['t'] in ('Space', 'SoftBreak'):
            out.append(' ')

    walk(inlines, collect)
    return ''.join(out)


def anchor_id(text):
    """MediaWiki 1.16 Sanitizer::escapeId: urlencode, keep ':', then '%' becomes '.'."""
    encoded = quote(text.strip().replace(' ', '_'), safe='').replace('~', '%7E')
    return encoded.replace('%3A', ':').replace('%', '.')


def convert(title, text, resolve, image_url):
    ast = json.loads(pandoc(['-f', 'mediawiki', '-t', 'json'], preprocess(text)))
    seen_anchors = {}

    def fix(node):
        if node['t'] == 'Link':
            target = node['c'][2]
            url, ltitle = target
            if ltitle == 'wikilink':
                target[0] = resolve(url, title)
                target[1] = ''
            else:
                p = urlparse(url)
                if p.scheme not in ('http', 'https', 'ftp', 'mailto', 'irc', 'news'):
                    # pandoc autolinks things like std::filesystem::x or av-openhome-org:service:Product:2.
                    target[0] = None
                elif p.netloc == 'wiki.openhome.org' and p.path.startswith('/wiki/'):
                    target[0] = resolve(p.path[len('/wiki/'):] + ('#' + p.fragment if p.fragment else ''), title)
        elif node['t'] in ('RawInline', 'RawBlock') and node['c'][0] == 'html':
            # MediaWiki shows tags outside its HTML whitelist as literal text; kramdown would
            # treat them as an HTML block and swallow the rest of the page.
            m = re.match(r'</?([a-zA-Z][a-zA-Z0-9]*)', node['c'][1])
            if m and m.group(1).lower() not in HTML_TAGS:
                literal = {'t': 'Str', 'c': node['c'][1]}
                if node['t'] == 'RawInline':
                    node.clear(); node.update(literal)
                else:
                    node.clear(); node.update({'t': 'Para', 'c': [literal]})
        elif node['t'] == 'Header':
            # Keep MediaWiki's anchors, including _2, _3 for repeated headings, so old #links still land.
            anchor = anchor_id(stringify(node['c'][2]))
            n = seen_anchors[anchor.lower()] = seen_anchors.get(anchor.lower(), 0) + 1
            if n > 1:
                anchor = f'{anchor}_{n}'
            node['c'][2].insert(0, {'t': 'RawInline', 'c': ['html', f'<span id="{html.escape(anchor, quote=True)}"></span>']})
        elif node['t'] == 'Image':
            target = node['c'][2]
            if not node['c'][1]:
                # MediaWiki used the file name as alt text for uncaptioned images.
                node['c'][1] = [{'t': 'Str', 'c': os.path.basename(target[0]).split(':')[-1]}]
            target[0] = image_url(target[0], title)
            if target[1] == 'fig:':
                target[1] = ''

    walk(ast['blocks'], fix)
    # Links to pages that never existed (MediaWiki red links) become plain text.
    def unlink(blocks):
        if isinstance(blocks, list):
            out = []
            for b in blocks:
                if isinstance(b, dict) and b.get('t') == 'Link' and b['c'][2][0] is None:
                    out.extend(unlink(b['c'][1]))
                else:
                    out.append(unlink(b))
            return out
        if isinstance(blocks, dict):
            return {k: unlink(v) for k, v in blocks.items()}
        return blocks

    ast = unlink(ast)

    return pandoc(['-f', 'json', '-t', 'gfm', '--wrap=none'], json.dumps(ast))


def front_matter(**kw):
    lines = ['---']
    for k, v in kw.items():
        if isinstance(v, list):
            lines.append(f'{k}:')
            lines += [f'  - {json.dumps(x)}' for x in v]
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return '\n'.join(lines + ['---', ''])


def main():
    pages, images = load()

    redirects = {}
    for t, text in pages.items():
        m = re.match(r'\s*#redirect\s*\[\[([^\]|#]+)', text, re.I)
        if m:
            redirects[t] = canonical(m.group(1))
    for t in DROP_TO_MAIN:
        redirects[t] = MAIN_PAGE

    def final(t):
        seen = set()
        while t in redirects and t not in seen:
            seen.add(t)
            t = redirects[t]
        return t

    images_by_name = {canonical(i['name']): i for i in images}

    def image_path(i):
        return urlparse(i['url']).path

    def resolve(link, from_title):
        link = link.strip()
        name, _, frag = link.partition('#')
        if not name:
            return '#' + anchor_id(frag)
        t = canonical(name.lstrip(':'))
        if t.startswith('Wikipedia:'):
            # Interwiki prefix from MediaWiki's default map.
            return 'https://en.wikipedia.org/wiki/' + quote(t.split(':', 1)[1].replace(' ', '_'), safe=":()_-.,!'*~")
        if t.startswith('Special:'):
            notes.append(f'{from_title}: link to {t} dropped (no special pages on a static site)')
            return None
        if t.startswith(('File:', 'Image:', 'Media:')):
            fname = canonical(t.split(':', 1)[1])
            if fname in images_by_name:
                return (image_path(images_by_name[fname]) if t.startswith('Media:')
                        else file_page_url(fname))
        elif final(t) in pages and not final(t).startswith(SKIP_NAMESPACES):
            return page_url(final(t)) + ('#' + anchor_id(frag) if frag else '')
        notes.append(f'{from_title}: red link to {link!r}')
        return None

    def image_url(src, from_title):
        name = canonical(src.split(':', 1)[1] if ':' in src else src)
        if name in images_by_name:
            return image_path(images_by_name[name])
        problems.append(f'{from_title}: missing image {src!r}')
        return src

    for d in (OUT_PAGES, OUT_IMAGES):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

    inbound = {}
    for t in redirects:
        inbound.setdefault(final(t), []).append(page_url(t))
    inbound.setdefault(MAIN_PAGE, []).extend(['/', '/wiki/'])

    written = 0
    outputs = {}

    def output_path(t):
        # Different titles can share a sanitised file name; never let one overwrite another.
        name = source_name(t)
        if name.lower() in outputs:
            raise SystemExit(f'output file clash: {t!r} and {outputs[name.lower()]!r} both map to {name}')
        outputs[name.lower()] = t
        return os.path.join(OUT_PAGES, name)

    written_titles = set()
    for t, text in sorted(pages.items()):
        if t in redirects or t.startswith(SKIP_NAMESPACES):
            continue
        try:
            body = convert(t, text, resolve, image_url)
        except RuntimeError as e:
            problems.append(f'{t}: pandoc failed: {str(e).strip()}')
            continue
        fm = front_matter(title=t, permalink=page_url(t), redirect_from=sorted(inbound.get(t, [])))
        with open(output_path(t), 'w') as f:
            # Raw: stops Liquid interpreting any {{ or {% in page text.
            f.write(fm + '\n{% raw %}\n' + body + '{% endraw %}\n')
        written += 1
        written_titles.add(t)

    for name, i in sorted(images_by_name.items()):
        dest = os.path.join(ROOT, image_path(i).lstrip('/'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(EXPORT, 'files', i['name']), dest)
        t = 'File:' + name
        body = f'![{name}]({image_path(i)})\n\n[Full size]({image_path(i)}) · {i["size"]} bytes · uploaded {i["timestamp"][:10]}\n'
        with open(output_path(t), 'w') as f:
            f.write(front_matter(title=t, permalink=file_page_url(name)) + '\n' + body)
        written += 1

    for target, urls in sorted(inbound.items()):
        if target not in written_titles:
            problems.append(f'redirects {urls} point at {target!r}, which was not written')

    print(f'wrote {written} pages, {len(images_by_name)} images, {len(redirects)} redirects')
    for n in notes:
        print('NOTE', n)
    for p in problems:
        print('PROBLEM', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
