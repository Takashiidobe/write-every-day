SOURCE_DOCS := $(shell find src -type f -name "*.md")
HTML_FILES=$(SOURCE_DOCS:src/%.md=site/%.html)
OUT_DIR=site/

all: html fix_links $(OUT_DIR)/robots.txt $(OUT_DIR)/sitemap.xml $(OUT_DIR)/rss.xml
	firefox site/index.html

html: mkdirs $(HTML_FILES)

fix_links: $(HTML_FILES)
	./bin/convert-html.sh

deploy: all
	ntl deploy --prod

site/%.html: src/%.md templates/pandoc-github-template.html.template
	pandoc -f markdown+fenced_divs -s $< -o $@ --table-of-contents --mathjax --section-divs --template templates/pandoc-github-template.html.template

clean:
	rm -r site/*.html

$(OUT_DIR)/robots.txt:
	@echo "User-agent: *" > $@
	@echo "Allow: *" >> $@
	@echo "Sitemap: $(BASE_URL)/sitemap.xml" >> $@

$(OUT_DIR)/sitemap.xml: $(HTML_FILES)
	./bin/sitemap.py > site/sitemap.xml

$(OUT_DIR)/rss.xml: $(HTML_FILES)
	./bin/rss.sh

.PHONY: mkdirs
mkdirs:
	cp -r assets/* site

$(OUT_DIR)/gen/%.html: posts/%.md templates/post.html
	/bin/pandoc -f markdown+fenced_divs -s $< -o $@ --table-of-contents --mathjax --filter pandoc-sidenote --section-divs --template templates/post.html
