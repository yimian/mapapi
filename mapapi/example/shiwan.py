# -*- coding: utf-8 -*-
"""
抓取广东省主要城市大中型超市, 便利店, 粤菜分布
"""

from xpinyin import Pinyin
from mapapi import baidu
import json
import logging
import re

malls = [u'家乐福', u'沃尔玛', u'好又多']
cities = [u'广州', u'深圳', u'佛山', u'东莞', u'惠州', u'中山', u'湛江', u'茂名', u'江门']

piny = Pinyin()
map_api = baidu.MapApi()


def get_file_name_by_city(city):
    return 'data/%s.json' % (piny.get_pinyin(city, ''))


def get_malls_by_city(malls, city, filter=None):
    """

    :param malls:
    :param city:
    :param filter: 过滤函数func(item, mall, city), 返回值为False的item将会被过滤掉
    """
    file_name = get_file_name_by_city(city)
    with open(file_name, 'w') as f:
        locations = []
        for m in malls:
            data = map_api.place_api.get_place_all(m, city, scope=2, industry_type='life', groupon=0, discount=0)
            nfilter = 0
            for item in data:
                try:
                    if filter and not filter(item, m, city):
                        nfilter += 1
                        continue
                    locations.append({'lat': item['location']['lat'], 'lng': item['location']['lng'], 'name': item['name'], 'keyword': m})
                except:
                    logging.exception(u'item格式错误: %s' % json.dumps(item))
                    print(item)
            if filter:
                print(city, m, len(data) - nfilter, 'filtered: %d' % nfilter)
            else:
                print(city, m, len(data))
        json.dump(locations, f)


def get_malls_all(filter=None):
    for city in cities:
        get_malls_by_city(malls, city, filter)


def filter_by_name(item, mall, city):
    pattern = u'\(%s.*店\)' % mall
    match = re.search(pattern, item['name'])
    if match:
        return False
    pattern = u'%s.*' % mall
    match = re.match(pattern, item['name'])
    if match:
        return True
    return False


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
