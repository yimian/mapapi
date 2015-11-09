# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import requests
import logging
import json


class TransformApi(object):
    """
    transform other format coordinates to baidu coordinates.
    """
    transform_url = 'http://api.map.baidu.com/geoconv/v1/'

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def _stringify_coords(self, coords):
        if isinstance(coords, dict):
            return '%s,%s' % (coords['lng'], coords['lat'])

        coords_str = ''
        for coord in coords:
            coords_str += '%s,%s;' % (coord['lng'], coord['lat'])
        coords_str = coords_str[:-1]
        return coords_str

    def _format_result(self, result):
        ret = []
        for item in result:
            ret.append({'lng': item['x'], 'lat': item['y']})
        return ret

    def transform(self, coords, **kwargs):
        """
        完成坐标转换

        :param coords: {'lat':, 'lng':, }或者list of {'lat':, 'lng':,}
        :param kwargs: available parameters include 'from', 'to', 'output'
        :return: if success  return
            [
                { 'lat':, 'lng':, }
                ...
            ]
            else return None.
        """
        from_type = kwargs.get('from', 3)
        to_type = kwargs.get('to', 5)
        output = kwargs.get('output', 'json')
        params = {'from': from_type, 'to': to_type, 'ak': self.scheduler.next(),
                  'output': output, 'coords': self._stringify_coords(coords)}
        try:
            r = requests.get(self.transform_url, params=params)
            r.raise_for_status()

            data = json.loads(r.text)
            if data['status'] == 0:
                return self._format_result(data['result'])
            logging.debug(u'failed to transform: %s' % r.text)
            return None
        except:
            logging.exception(u'获取坐标转化失败: %s' % json.dumps(params))
        return None
