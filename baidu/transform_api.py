# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import requests
import logging
import json

baidu_ak = '9ea66EnDo1YLFuzu5QDDp4zU'
transform_url = 'http://api.map.baidu.com/geoconv/v1/'

def stringify_coords(coords):
    if isinstance(coords, dict):
        return '%s,%s' % (coords['lng'], coords['lat'])

    coords_str = ''
    for coord in coords:
        coords_str += '%s,%s;' % (coord['lng'], coord['lat'])
    coords_str = coords_str[:-1]
    return coords_str


def format_result(array):
    ret = []
    for item in array:
        ret.append({'lng': item['x'], 'lat': item['y']})
    return ret


def transform(coords, **kwargs):
    from_type = kwargs.get('from', 3)
    to_type = kwargs.get('to', 5)
    output = kwargs.get('output', 'json')
    params = {'from': from_type, 'to': to_type, 'ak': baidu_ak, 'output': output, 'coords': stringify_coords(coords)}
    try:
        r = requests.get(transform_url, params=params)
        r.raise_for_status()

        data = json.loads(r.text)
        if data['status'] == 0:
            return format_result(data['result'])
        logging.error(u'坐标转换接口调用失败, 错误码: %d' % data['status'])
        return None
    except:
        logging.exception(u'获取坐标转化失败: %s' % json.dumps(params))
    return None
