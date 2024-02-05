#!/usr/bin/env sh

pandoc-rss $(find . -type f -name "*.html")> site/rss.xml

PREFIX=$(cat <<-END
  <?xml version="1.0" encoding="UTF-8" ?>
  <?xml-stylesheet href="./rss.xsl" type="text/xsl"?>
  <rss version="2.0">
  <channel>
    <title>Write every day</title>
    <link>https://write.takashiidobe.com</link>
  <description>Writing every day for practice</description>
END
)

# prefix
echo $PREFIX | cat - site/rss.xml | sponge site/rss.xml

# suffix
echo "</channel></rss>" >> site/rss.xml
