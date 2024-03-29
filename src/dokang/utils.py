# Copyright (c) Polyconseil SAS. All rights reserved.
import json
import os
import os.path

from dokang import api


def get_harvester(fqn):
    module_fqn, function_fqn = fqn.rsplit('.', 1)
    module = __import__(module_fqn, fromlist=[function_fqn])
    return getattr(module, function_fqn)


def doc_set(settings, uploaded):

    harvester = get_harvester(settings['dokang.uploaded_docs.harvester'])
    upload_dir = settings.get('dokang.uploaded_docs.dir')
    uploaded_path = os.path.join(upload_dir, uploaded)

    title = None
    info_file = os.path.join(uploaded_path, '.dokang')
    if os.path.exists(info_file):
        with open(info_file, encoding="utf-8") as fp:
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
        try:
            os.makedirs(os.path.dirname(index_path))
        except OSError:  # It's ok if the parent dir exists already
            pass
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
