import os
import sys
word = sys.argv[1].strip().lower().split()[0]

print ('Before')

os.system("conda activate django2|scrapy crawl dict -o results.json -a word=%s" % word)

print ('After')
