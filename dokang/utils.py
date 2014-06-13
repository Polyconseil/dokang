# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.

def load_doc_sets(settings):
    """Given a settings dictionnary with the path of the doc sets file,
    replace the path (in-place) with the doc sets themselves.
    """
    key = 'dokang.doc_sets'
    path = settings[key]
    contents = {}
    with open(path) as fp:
        exec(fp.read(), {}, contents)  # pylint: disable=exec-used
    sets = {}
    for info in contents['DOC_SETS']:
        sets[info['id']] = info
    settings[key] = sets
    return settings
