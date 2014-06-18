# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.

import imp


def load_doc_sets(settings):
    """Given a settings dictionnary with the path of the doc sets file,
    replace the path (in-place) with the doc sets themselves.
    """
    key = 'dokang.doc_sets'
    path = settings[key]
    module = imp.load_source('dokang__doc_sets', path)
    sets = {}
    for info in module.DOC_SETS:
        sets[info['id']] = info
    settings[key] = sets
    return settings
