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

def dict_create(word_q):
    word_q = word_q.strip().lower()

    word_q = ';' + word_q + ';'  # Add ';' to help filtering.

    dicts = Dict.objects.filter(Q(word_forms__icontains=word_q))
    # Eg. tycka --> tycka, if tycka has already been added.
    if dicts.exists():
        return
    else:
        word_in = word_q.split(';')[1].split()[0] # With scrapy, only one single word can be searched.

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

        os.system("conda activate django2 | scrapy crawl dict -o %s -a word=%s" % (result_file_name, word_in))

        while True:
            if os.path.isfile(result_file_name):
                if os.path.getsize(result_file_name) > 0:
                    with open(result_file_name, 'r') as fi:
                        lines = fi.readlines()
                        result_json = lines[1].strip()
                        result_dict = json.loads(result_json)
                        word = result_dict['word']

                        print(word_q, word_in, word)
                        try:
                            if word.endswith('*'):
                                word = word[:-1]

                            # To see if the word has been added. Eg. tyckte --> tycka, only add the form now.
                            dict = Dict.objects.filter(word=word)[0]
                            if dict:
                                # dict.com can only search single words, a pharse will be treated as single single.
                                if ' ' in word_q:
                                    word_q = word_q.split()[0] + ';'

                                if word_q not in dict.word_forms:
                                    dict.add_form(word_q)
                                return
                        except AttributeError:
                            # No word was found.
                            return
                        except IndexError:
                            # For the first search!
                            pass

                        word_form = ';' + word + ';'  # The root word, add ';' to help filtering.
                        pron = result_dict['pron']
                        morf = result_dict['morf']
                        forms = result_dict['form']
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

                        id = re.sub(r'\s+', '_', word)
                        accordion_id = "accordion" + "_" + id
                        heading_id = "heading" + "_" + id
                        collapse_id = "collaspse" + "_" + id

                        break
                else:
                    time.sleep(1)
                    return
            else:
                time.sleep(1)

        dict = Dict(word=word, word_forms=word_form, pron=pron, morf=morf,
                    forms=forms, trans=trans, trans_all=trans_all,
                    accordion_id=accordion_id,
                    heading_id=heading_id,
                    collapse_id=collapse_id,
                    )
        dict.save()
        os.chdir(cwd)

with open('swedish_list.txt', 'r') as fi:
    word_list = fi.readlines()

for word_q in word_list:
    print(word_q)
    dict_create(word_q)
