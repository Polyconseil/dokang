# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.
from __future__ import unicode_literals

import os
import os.path

from dokang import api


def get_harvester(fqn):
    module_fqn, function_fqn = fqn.rsplit(b'.', 1)
    module = __import__(module_fqn, fromlist=[function_fqn])
    return getattr(module, function_fqn)


def doc_set(settings, uploaded):

    harvester = get_harvester(settings['dokang.uploaded_docs.harvester'])
    upload_dir = settings.get('dokang.uploaded_docs.dir')

    uploaded = uploaded.decode('utf-8')
    uploaded_path = os.path.join(upload_dir, uploaded)
    return {
        'id': uploaded,
        'title': uploaded,
        'path': uploaded_path,
        'harvester': harvester(),
    }


def load_doc_sets(settings):
    """
    Given a settings dictionary with the path of the doc sets file,
    replace the path (in-place) with the doc sets themselves.
    """
    index_path = settings['dokang.index_path']
    if not os.path.exists(index_path):
        api.initialize_index(index_path)

    upload_dir = settings['dokang.uploaded_docs.dir']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    sets = settings['dokang.doc_sets'] = {}
    for uploaded in os.listdir(upload_dir):
        sets[uploaded] = doc_set(settings, uploaded)

    return settings
