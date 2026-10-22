# wiki.openhome.org

Static copy of the OpenHome MediaWiki (OpenHome service specifications and
developer docs), served by GitHub Pages at https://wiki.openhome.org.

It is a point-in-time conversion taken on 2026-10-22: current page text only,
no edit history. The wiki itself (MediaWiki 1.16) is being retired.

## Layout

- `wiki/` — one Markdown page per wiki page. `permalink` keeps the old
  `/wiki/<Title>` URL; `redirect_from` covers the wiki's redirect pages.
- `mediawiki/images/` — uploaded files, at their original paths.
- `export/` — the raw MediaWiki export the site was generated from.
- `tools/convert.py` — the converter.

## Editing

Edit the Markdown in `wiki/` and open a pull request. Do not re-run the
converter once pages have been edited here: it regenerates `wiki/` from
`export/` and would overwrite those edits.

## Local preview

```
docker run --rm -v "$PWD:/srv" -w /srv -e BUNDLE_PATH=/srv/vendor/bundle -p 4000:4000 ruby:3.3 sh -c "bundle install && bundle exec jekyll serve --host 0.0.0.0"
```

## Re-running the conversion

```
docker run --rm -v "$PWD:/src" -w /src --entrypoint sh pandoc/core:3.5 -c "apk add --no-cache python3 && python3 tools/convert.py"
```

It prints a NOTE for each link to a page that never existed on the wiki;
those are kept as plain text, as the wiki showed them. It prints PROBLEM
and exits non-zero if any page, image or redirect could not be converted.
