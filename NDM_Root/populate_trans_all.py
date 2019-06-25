# Configure settings for project
# Need to run this before calling models from application!
import re
import json
import time

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','NDM.settings')

import django
from django.db.models import Q
# Import settings
django.setup()
# from django.db.models import Q   # Can be used for filtering.

from myserver.models import Dict

dict_list = Dict.objects.all()
for dict in dict_list:
    word = dict.word.split()[0]
    print(word)
    
    if dict.trans_all:
        continue

    cwd = os.getcwd()
    ## Work in the dict directory.
    # Local
    dict_dir = r'C:\Google\Work\MyWebsite\newdataminer\NDM_Root\myserver\dict'
    # PythonAnyWhere
    # dict_dir = r'/home/guanglin/newdataminer/NDM_Root/myserver/dict'
    os.chdir(dict_dir)
    username = 'system'
    result_file_name = username + '.json'
    # Delete the result json file it already exists.
    if os.path.isfile(result_file_name):
        os.remove(result_file_name)

    os.system("conda activate django2 | scrapy crawl dict -o %s -a word=%s" % (result_file_name, word))

    while True:
        if os.path.isfile(result_file_name):
            if os.path.getsize(result_file_name) > 0:
                with open(result_file_name, 'r') as fi:
                    lines = fi.readlines()
                    result_json = lines[1].strip()
                    result_dict = json.loads(result_json)

                    trans_list = json.loads(result_dict['trans'])

                    # For display in table view:
                    trans_list0 = trans_list[0] # Only take the first translation for now.
                    trans = ''
                    for item in trans_list0[:2]:
                        if not re.search('[0-9]', item):
                            trans += item + ' '
                    # For display in card view and detail view:
                    trans_all = ''
                    for term in trans_list:
                        trans_all += ' '.join(term) + '<br>'


                    break
            else:
                time.sleep(1)
        else:
            time.sleep(1)

    dict.word_forms = ';' + word + ';'  # Add ';' to help filtering.
    dict.trans_all = trans_all

    dict.save()
    os.chdir(cwd)
