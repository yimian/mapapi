# -*- coding: utf-8 -*-
u""" 处理城市坐标 """
__author__ = 'zhangjinjie'

import requests
import logging
import json
from mapapi.baidu.exceptions import ParamError

# 返回码
baidu_ret_code = {
    0: u'正常',
    1: u'服务器内部错误',
    2: u'请求参数非法',
    3: u'权限校验失败',
    4: u'配额校验失败',
    5: u'ak不存在或者非法',
    101: u'服务禁用',
    102: u'不通过白名单或者安全码不对',
}


class LocationApi(object):
    """
    translate address to geographical coordinates(refer to location) or location to address....
    """
    # 通过地址获取地理坐标url地址
    baidu_json_location_url = u'http://api.map.baidu.com/geocoder/v2/'

    # 通过地理坐标返回地址信息url地址
    baidu_json_region_url = u'http://api.map.baidu.com/geocoder/v2/'

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def _format_province(self, province):
        u"""
        标准化省份信息, 比如将'内蒙古自治区'统一转换成'内蒙古'.

        :param province: origin province
        :return: formatted province
        """
        length = len(province)
        if province.endswith(u'省') or province.endswith(u'市'):
            return province[0:length - 1]
        elif province.endswith(u'自治区'):
            if u'内蒙古' in province:
                return u'内蒙古'
            if u'宁夏' in province:
                return u'宁夏'
            if u'广西' in province:
                return u'广西'
            if u'新疆' in province:
                return u'新疆'
            if u'西藏' in province:
                return u'西藏'
        return province

    def _format_city(self, city):
        """
        标准化城市信息, 去掉城市尾部所带的'市'.

        :param city: origin city
        :return: formatted city
        """
        if u'市' in city:
            length = len(city)
            return city[0:length - 1]
        return city

    def get_detail_location_by_address(self, address, city=None):
        """
        根据地址信息获取地理坐标

        :param address: address must include province and city information.
        :param city: city just functions as a filter for return data.
        :return: if success, return
            { 'location':  # 经纬度坐标
                { 'lat': , 'lng': },
              'precise': , # 位置的附加信息, 是否精确查找, 1为精确查找, 0为不精确
              'confidence': , # 可信度
              'level': , # 地址类型
            }
            else return None.
        """
        if address is None:
            raise ParamError(u'address不能为空')
        params = {'address': address, 'ak': self.scheduler.next(), 'output': 'json'}
        if city:
            params['city'] = city
        try:
            r = requests.get(self.baidu_json_location_url, params=params)
            r.raise_for_status()

            data = json.loads(r.text)
            if data['status'] == 0:
                return data['result']
            else:
                logging.debug(r.text)
        except Exception as e:
            logging.exception(e)

        logging.error(u'failed to get address location for %s' % address)
        return None

    def get_location_by_address(self, address, city=None):
        """
        Same with get_detail_location_by_address, except for just return {'lat': , 'lng'} location info.

        :param address:
        :param city:
        :return: if success return {'lat': , 'lng': } else return None.
        """
        detail = self.get_detail_location_by_address(address, city)
        if detail:
            return detail['location']
        return None

    def get_detail_address_by_location(self, location, **kwargs):
        """
        根据地理坐标获取地址信息

        :param location: {'lat': , 'lng': } 地理坐标
        :param kwargs:
        :return: if success return
            { 'location': {'lat':, 'lng'},
              'origin_location': {'lat':, 'lng'}, # 这是请求的location, 并非百度原始返回的
              'formatted_address":, # 结构化地址信息
              'business':, # 商圈
              'addressComponent': # 地址信息
                { 'country":, # 国家
                  'province':, # 省名
                  'city':, # 城市名
                  'district':, # 区县名
                  'street':, # 街道名
                  'street_number':, # 街道门牌号
                  'country_code':, # 国家code
                  'direction':, # 和当前坐标点的方向
                  'distance': # 和当前坐标点的距离
                }
              'pois': # 周边poi数组
                { 'addr':, # 地址信息
                  'cp':, # 数据来源
                  'direction':, # 和当前坐标点方向
                  'distance':, # 离坐标点距离
                  'name':, # poi名称
                  'poiType':, # poi类型, 如'办公大楼, 商务大厦'
                  'point':, # poi坐标
                  'tel':, # 电话
                  'uid':, # poi唯一标识
                  'zip':, # 邮编
                }
              'sematic_description':, # 当前位置结合POI的语义化结果描述
            } or return None.
        :raise ParamError: if location is None.
        """
        if location is None:
            raise ParamError(u'location不能为空')
        params = {'ak': self.scheduler.next(), 'output': 'json', 'location': '{lat},{lng}'.format(lat=location['lat'],
                                                                                                  lng=location['lng']),
                  'coordtype': kwargs.get('coordtype', 'bd09ll'), 'pois': kwargs.get('pois', 0)}
        try:
            r = requests.get(self.baidu_json_region_url, params=params)
            r.raise_for_status()

            data = json.loads(r.text)
            if data['status'] == 0:
                data['result']['origin_location'] = {'lat': location['lat'], 'lng': location['lng']}
                return data['result']
            else:
                logging.debug(r.text)
        except Exception as e:
            logging.exception(e)

        logging.error(u'failed to get province for %s' % str(location))
        return None

    def get_province_by_location(self, location, **kwargs):
        """
        Same with get_detail_address_by_location, except for just returning formatted province info.

        :param location: {'lat':, 'lng':,}
        :param kwargs:
        :return: if success, return formatted province, else return None.
        """
        detail = self.get_detail_address_by_location(location, **kwargs)
        if detail:
            return self._format_province(detail['addressComponent']['province'])
        return None

    def get_address_by_location(self, location, **kwargs):
        """
        Same with get_detail_address_by_location, except for just returning addressComponent info whose provine and city
        are formatted.

        :param location: {'lat':, 'lng':}
        :param kwargs:
        :return: if success return
                { 'country":, # 国家
                  'province':, # 省名
                  'city':, # 城市名
                  'district':, # 区县名
                  'street':, # 街道名
                  'street_number':, # 街道门牌号
                  'country_code':, # 国家code
                  'direction':, # 和当前坐标点的方向
                  'distance': # 和当前坐标点的距离
                }
                else return None.
        """
        detail = self.get_detail_address_by_location(location, **kwargs)
        if detail:
            address = detail['addressComponent']
            address['province'] = self._format_province(address['province'])
            address['city'] = self._format_province(address['city'])
            return address
        return None

    def get_formatted_province(self, address):
        """
        返回地址所对应的标准化省份名称

        :param address: 详细地址信息
        :return: if success return province info else return None.
        """
        location = self.get_location_by_address(address)
        if location:
            return self.get_province_by_location(location)
        return None

    def get_formatted_address(self, address):
        """
        返回地址所对应的标准化地址信息

        :param address: 详细地址信息
        :return: if success return
                { 'country":, # 国家
                  'province':, # 省名
                  'city':, # 城市名
                  'district':, # 区县名
                  'street':, # 街道名
                  'street_number':, # 街道门牌号
                  'country_code':, # 国家code
                  'direction':, # 和当前坐标点的方向
                  'distance': # 和当前坐标点的距离
                }
                else return None.
        """
        location = self.get_location_by_address(address)
        if location:
            return self.get_address_by_location(location)
        return None

    def get_formatted_detail_address(self, address):
        """
        返回地址所对应的标准化的详细地址

        :param address: 详细地址信息
        :return: if success return
            { 'location': {'lat':, 'lng'},
              'origin_location': {'lat':, 'lng'}, # 这是请求的location, 并非百度原始返回的
              'formatted_address":, # 结构化地址信息
              'business':, # 商圈
              'addressComponent': # 地址信息
                { 'country":, # 国家
                  'province':, # 省名
                  'city':, # 城市名
                  'district':, # 区县名
                  'street':, # 街道名
                  'street_number':, # 街道门牌号
                  'country_code':, # 国家code
                  'direction':, # 和当前坐标点的方向
                  'distance': # 和当前坐标点的距离
                }
              'pois': # 周边poi数组
                { 'addr':, # 地址信息
                  'cp':, # 数据来源
                  'direction':, # 和当前坐标点方向
                  'distance':, # 离坐标点距离
                  'name':, # poi名称
                  'poiType':, # poi类型, 如'办公大楼, 商务大厦'
                  'point':, # poi坐标
                  'tel':, # 电话
                  'uid':, # poi唯一标识
                  'zip':, # 邮编
                }
              'sematic_description':, # 当前位置结合POI的语义化结果描述
            } or return None.
        """
        location = self.get_location_by_address(address)
        if location:
            return self.get_detail_address_by_location(location)
        return None

