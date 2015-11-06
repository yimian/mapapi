# -*- coding: utf-8 -*-
import codecs
from baidu.geo_api import get_address_location
import json

with codecs.open('data/clinic.txt', 'r', encoding='utf-8') as f:
    matched = []
    unmatched = []
    for line in f:
        clinic_name = line.strip()
        loc = get_address_location(u'深圳 %s' % clinic_name)
        if loc:
            matched.append({'name': clinic_name, 'loc': loc})
        else:
            unmatched.append(clinic_name)

    print 'nmatched: %d, unmatched: %d' % (len(matched), len(unmatched))

    with codecs.open('data/matched_clinic.txt', 'w', encoding='utf-8') as f:
        json.dump(matched, f)
