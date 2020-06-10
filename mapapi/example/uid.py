# -*- coding: utf-8 -*-

import json
import logging
from mapapi import baidu
import codecs


map_api = baidu.MapApi()


def get_locs(data):
    for item in data:
        loc = map_api.transform_api.get_place_by_uids(item['uid'])
        if loc:
            item['lat'] = loc['location']['lat']
            item['lng'] = loc['location']['lng']
            item['name'] = loc['name']
            item['address'] = loc['address']
        else:
            logging.error(u'获取地理坐标失败: %s' % item)


def get_locs_from_file(infile):
    import os
    dir_name, ext_name = os.path.splitext(infile)
    outfile = '%s_loc%s' % (dir_name, ext_name)
    with codecs.open(infile, 'r', encoding='utf-8') as f:
        data = json.load(f)
        get_locs(data)
        with codecs.open(outfile, 'w', encoding='utf-8') as f:
            json.dump(data, f)


def run_func(func_name, env, *args):
    if func_name in env:
        func = env.get(func_name)
        if hasattr(func, '__call__'):
            func(*args)
        else:
            print('%s is not a function name' % func_name)
    else:
        print('%s not found' % func_name)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("error, not less than one parameter")
        exit(-1)
    run_func(sys.argv[1], globals(), *sys.argv[2:])
