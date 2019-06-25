import os
import sys
phrase_q = sys.argv[1].strip().lower()

print ('Before')

os.system("conda activate django2|scrapy crawl phrase -o results.json -a phrase=%s" % phrase_q)

print ('After')
