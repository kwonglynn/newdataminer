import os

word = 'mig'

os.system("conda activate django2|scrapy crawl dict -o results.json -a word=%s" % word)
