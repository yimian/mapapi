# -*- coding: utf-8 -*-
import codecs
from mapapi import baidu
import json

with codecs.open('data/clinic.txt', 'r', encoding='utf-8') as f:
    map_api = baidu.MapApi()
    matched = []
    unmatched = []
    for line in f:
        clinic_name = line.strip()
        loc = map_api.location_api.get_location_by_address(u'深圳 %s' % clinic_name)
        if loc:
            matched.append({'name': clinic_name, 'loc': loc})
        else:
            unmatched.append(clinic_name)

    print('nmatched: %d, unmatched: %d' % (len(matched), len(unmatched)))

    with codecs.open('data/matched_clinic.txt', 'w', encoding='utf-8') as f:
        json.dump(matched, f)
