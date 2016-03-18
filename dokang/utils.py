# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.
from __future__ import unicode_literals

import json
import os
import os.path

from dokang import api
from . import compat


def get_harvester(fqn):
    module_fqn, function_fqn = fqn.rsplit('.', 1)

    # Hack around https://bugs.python.org/issue21720
    if compat.PY2 and not isinstance(module_fqn, bytes):
        module_fqn = module_fqn.encode()
        function_fqn = function_fqn.encode()

    module = __import__(module_fqn, fromlist=[function_fqn])
    return getattr(module, function_fqn)


def doc_set(settings, uploaded):

    harvester = get_harvester(settings['dokang.uploaded_docs.harvester'])
    upload_dir = settings.get('dokang.uploaded_docs.dir')
    uploaded_path = os.path.join(upload_dir, uploaded)

    title = None
    info_file = os.path.join(uploaded_path, '.dokang')
    if os.path.exists(info_file):
        with open(info_file) as fp:
            info = json.load(fp)
            title = info.get('title') if isinstance(info, dict) else None

    return {
        'id': uploaded,
        'title': title or uploaded,
        'path': uploaded_path,
        'harvester': harvester(),
    }


def get_doc_sets(settings):
    """
    Get doc sets using path of doc sets file defined in settings.
    """
    index_path = settings['dokang.index_path']
    if not os.path.exists(index_path):
        os.makedirs(os.path.dirname(index_path))
        api.initialize_index(index_path)

    upload_dir = settings['dokang.uploaded_docs.dir']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    return {
        uploaded: doc_set(settings, uploaded)
        for uploaded in (
            x.decode('utf-8') if isinstance(x, bytes) else x
            for x in os.listdir(upload_dir)
        )
    }
