# Configure settings for project
# Need to run this before calling models from application!
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','NDM.settings')

import django
# Import settings
django.setup()
# from django.db.models import Q   # Can be used for filtering.

from myserver.models import Dict
object_list = Dict.objects.all()

for object in object_list:
    word = object.word

    # added_by = object.added_by
    # pron = object.pron
    # morf = object.morf
    # forms = object.forms
    # trans = object.trans
    # created_date = object.created_date
    # last_date = object.last_date
    # name_label = object.name_label

    accordion_id = 'accordion' + '_' + word
    heading_id = 'heading' + '_' + word
    collapse_id = 'collapse' + '_' + word

    # print (word, accordion_id, heading_id, collapse_id)
    object.accordion_id = accordion_id
    object.heading_id = heading_id
    object.collapse_id = collapse_id
    object.save()

    # For new objects!
    # dict = Dict.objects.get_or_create(word=word, added_by=added_by, pron=pron, morf=morf,
    #                                   forms=forms, trans=trans,
    #                                   created_date=created_date, last_date=last_date, name_label=name_label,
    #                                   accordion_id=accordion_id,
    #                                   heading_id=heading_id,
    #                                   collapse_id=collapse_id,
    #                                  )[0]
    # dict.save()
    print (object.word, object.accordion_id, object.heading_id, object.collapse_id)
