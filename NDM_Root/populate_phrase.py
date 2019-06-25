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

def dict_create(phrase):
    phrase = phrase.strip().lower()

    phrases = Dict.objects.filter(word=phrase)
    # Eg. tycka --> tycka, if tycka has already been added.
    if phrases.exists():
        return
    else:
        cwd = os.getcwd()
        ## Work in the dict directory.
        # Local
        phrase_dir = r'C:\Google\Work\MyWebsite\newdataminer\NDM_Root\myserver\phrase'
        # PythonAnyWhere
        # dict_dir = r'/home/guanglin/newdataminer/NDM_Root/myserver/phrase'
        os.chdir(phrase_dir)
        username = 'system'
        result_file_name = username + '.json'
        # Delete the result json file it already exists.
        if os.path.isfile(result_file_name):
            os.remove(result_file_name)

        phrase_q = '-'.join(phrase.split())
        print (phrase_q)
        os.system("conda activate django2 | scrapy crawl phrase -o %s -a phrase=%s" % (result_file_name, phrase_q))

        while True:
            if os.path.isfile(result_file_name):
                if os.path.getsize(result_file_name) > 0:
                    with open(result_file_name, 'r') as fi:
                        lines = fi.readlines()
                        result_json = lines[1].strip()
                        result_dict = json.loads(result_json)
                        phrase = result_dict['phrase']

                        trans_list = result_dict['trans']

                        # For display in table view:
                        trans = trans_list[0] # Only take the first translation for now.

                        # For display in card view and detail view:
                        trans_all = ''
                        for i, term in enumerate(trans_list):
                            trans_all += str(i+1) + '. ' + term + '<br> '

                        id = re.sub(r'\s+', '_', phrase)
                        accordion_id = "accordion" + "_" + id
                        heading_id = "heading" + "_" + id
                        collapse_id = "collaspse" + "_" + id

                        break
                else:
                    time.sleep(1)
                    return
            else:
                time.sleep(1)

        phrase_form = ';' + phrase + ';'
        dict = Dict(word=phrase, word_forms=phrase_form, morf='phrase', trans=trans, trans_all=trans_all,
                    accordion_id=accordion_id,
                    heading_id=heading_id,
                    collapse_id=collapse_id,
                    )
        dict.save()
        os.chdir(cwd)

with open('phrase_list.txt', 'r') as fi:
    phrase_list = fi.readlines()

for phrase in phrase_list:
    print(phrase)
    dict_create(phrase)
