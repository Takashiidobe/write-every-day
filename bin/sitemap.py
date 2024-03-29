#!/usr/bin/env python3

import re
import math
import glob
from pathlib import Path
from subprocess import run

file_pattern = re.compile(r'.*?(\d+).*?')
def get_order(file):
    match = file_pattern.match(Path(file).name)
    if not match:
        return math.inf
    return int(match.groups()[0])

print('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="./sitemap.xsl"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for f in sorted(glob.glob("./src/*.md"), key=get_order):
    last_mod_res = run(['git', 'log', '-1', '--follow', '--format=%aI', '--date=iso-local', f], capture_output=True)
    pub_res = run(['git', 'log', '-1', '--diff-filter=A', '--follow', '--format=%aI', '--date=iso-local', f], capture_output=True)
    f = f[5:]
    file_stem = Path(f).stem
    print(f"<url><loc>./{file_stem}.html</loc>")
    last_modified = last_mod_res.stdout.strip().decode('utf-8')
    print(f"<lastmod>{last_modified}</lastmod>")
    published = pub_res.stdout.strip().decode('utf-8')
    print(f"<pubdate>{published}</pubdate>")
    print("</url>")
print("</urlset>")
