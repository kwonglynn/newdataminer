import os

word = 'man'

os.system("conda activate django2|scrapy crawl dict -o results.json -a word=%s" % word)
