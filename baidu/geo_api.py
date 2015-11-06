# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'
__doc__ = """ 处理城市坐标 """

import requests
import logging
import json
import urllib

# 百度应用密钥, 需要在百度地图上申请
# baidu_ak = 'wwx6xhe8aQncZZUm7QsIPXKI'
baidu_ak = '9ea66EnDo1YLFuzu5QDDp4zU'

# 通过地址获取地理坐标url地址
baidu_json_location_url = u'http://api.map.baidu.com/geocoder/v2/'

# 通过地理坐标返回地址信息url地址
baidu_json_region_url = u'http://api.map.baidu.com/geocoder/v2/?ak={ak}&location={lat},{lng}&output=json'

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


def get_address_location(address, city=None):
    """
    根据地址信息获取地理坐标

    注意: city只是起到过滤作用, 所输入的address信息应该带省市区信息
    """
    if address is None:
        return None
    params = {'address': address, 'ak': baidu_ak, 'output': 'json'}
    if city:
        params['city'] = city
    try:
        r = requests.get(baidu_json_location_url, params=params)
        r.raise_for_status()

        data = json.loads(r.text)
        # print data
        if data['status'] == 0:
            return data['result']['location']['lat'], data['result']['location']['lng']
        else:
            print json.dumps(data, ensure_ascii=False)  # 输出中文, 而非unicode字符
    except Exception as e:
        logging.exception(e)

    logging.error(u'failed to get address location for %s' % address)
    return None


def strip_province(province):
    """
    标准化省份信息, 比如将'内蒙古自治区'统一转换成'内蒙古'
    :param province:
    :return:
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


def strip_city(city):
    """
    标准化城市信息, 去掉城市尾部所带的'市'
    :param city:
    :return:
    """
    if u'市' in city:
        length = len(city)
        return city[0:length - 1]
    return city


def get_geo_province(location):
    """
    根据地理坐标信息, 返回能在echarts地图控件使用的省份
    :param location:
    :return:
    """
    url = baidu_json_region_url.format(ak=baidu_ak, lat=location[0], lng=location[1])
    try:
        r = requests.get(url)
        r.raise_for_status()

        data = json.loads(r.text)
        # print data
        if data['status'] == 0:
            province = data['result']['addressComponent']['province']
            return strip_province(province)
    except Exception as e:
        logging.exception(e)

    logging.error(u'failed to get province for %s' % str(location))
    return None


def get_geo_address(location):
    """
    根据地理坐标信息返回省市区街道等信息

    返回地址
    {
        'country': ,  # 国家
        'province': ,
        'city': ,
        'district': ,
        'street': ,
        'street_number': ,  # 街道门牌号
        'country_code': ,  # 国家code
        'direction': ,  # 和当前坐标点的方向, 当有门牌号的时候返回数据
        'distance': ,  # 和当前坐标点的距离, 当有门牌号的时候返回数据
    }
    :param location:
    :return:
    """
    url = baidu_json_region_url.format(ak=baidu_ak, lat=location[0], lng=location[1])
    try:
        r = requests.get(url)
        r.raise_for_status()

        data = json.loads(r.text)
        # print data
        if data['status'] == 0:
            address = data['result']['addressComponent']
            address['province'] = strip_province(address['province'])
            address['city'] = strip_city(address['city'])
            return address
    except Exception as e:
        logging.exception(e)

    logging.error(u'failed to get province for %s' % str(location))
    return None


def get_baidu_address(location):
    """
    根据地理坐标, 返回百度原始地址信息, 其中包含商圈等信息
    :param location:
    :return:
    """
    url = baidu_json_region_url.format(ak=baidu_ak, lat=location[0], lng=location[1])
    try:
        r = requests.get(url)
        r.raise_for_status()

        data = json.loads(r.text)
        # print data
        if data['status'] == 0:
            data['result']['origin_location'] = {'lat': location[0], 'lng': location[1]}
            return data['result']
    except Exception as e:
        logging.exception(e)

    logging.error(u'failed to get province for %s' % str(location))
    return None


def get_address_province(address):
    """
    根据地址信息, 返回地址所在省份
    :param address:
    :return:
    """
    location = get_address_location(address)
    if location:
        return get_geo_province(location)
    else:
        return None


def get_address_all(address):
    """
    根据地址信息, 返回省市区街道等信息
    :param address:
    :return:
    """
    location = get_address_location(address)
    if location:
        return get_geo_address(location)
    else:
        return None


def get_address_origin(address):
    """
    根据地址信息, 返回百度原始结果, 包含商圈等信息
    :param address:
    :return:
    """
    if address is None:
        return None
    location = get_address_location(address)
    if location:
        return get_baidu_address(location)
    else:
        return None
