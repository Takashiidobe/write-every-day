#!/usr/bin/env python3

import glob
from pathlib import Path
from subprocess import run

print('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="./sitemap.xsl"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for f in glob.glob("./src/*.md"):
    f = f[5:]
    file_stem = Path(f).stem
    print(f"<url><loc>./{file_stem}.html</loc>")
    last_mod_res = run(['git', 'log', '-1', '--pretty="%cd"', '--date=iso-local', f], capture_output=True)
    last_modified = last_mod_res.stdout.strip().decode('utf-8')
    print(f"<lastmod>{last_modified}</lastmod>")
    pub_res = run(['git', 'log', '-1', '--pretty="%cd"', '--date=iso-local', f], capture_output=True)
    published = pub_res.stdout.strip().decode('utf-8')
    print(f"<pubdate>\"{published}\"</pubdate>")
    print("</url>")
print("</urlset>")
