# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import requests
import json
import logging


class PlaceApi(object):
    u"""
    search poi data by keyword.
    """
    search_url = 'http://api.map.baidu.com/place/v2/search'
    detail_url = 'http://api.map.baidu.com/place/v2/detail'
    eventsearch_url = 'http://api.map.baidu.com/place/v2/eventsearch'
    eventdetail_url = 'http://api.map.baidu.com/place/v2/eventdetail'

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def get_place_by_page(self, query, region, **kwargs):
        u"""
        城市内检索

        百度在没有查找到对应查询请求时, 会返回在其它城市查找到的结果, 返回格式为[{'num': , 'name': ''} ...]这样的数组
        获取一页query相关地理信息
        :param query: 查询关键词
        :param region: 地区
        :param kwargs:
        :return:  if success return
            {
                status: 本次API访问状态, 成功返回0, 其他返回其他数字,
                message: 对本次API访问状态值的英文说明, 如果成功返回'ok', 失败返回错误说明,
                total: 检索总数, 用户请求中设置了page_num字段时才会出现, 当检索总数超过760时, 多次刷新同一请求得到的total值, 可能稍有不同
                results: [
                    {
                        name:  POI名称,
                        location: {
                            lat: 纬度,
                            lng: 经度
                        },
                        address: POI地址信息,
                        telephone: POI电话信息,
                        uid: POI的唯一标识,
                        detail_info: {  # POI扩展信息, 仅当scope=2时, 显示该字段, 不同POI类型, 显示的detail_info字段不同
                            distance: 距离中心点距离,
                            type: POI类型,
                            tag: 标签,
                            detail_url: POI的详情页,
                            price: POI商户的价格,
                            shop_hours: 营业时间,
                            overall_rating: 总体评分,
                            taste_rating: 口味评分,
                            service_rating: 服务评分,
                            environment_rating: 环境评分,
                            facility_rating: 星级评分,
                            hygiene_rating: 卫生评分,
                            technology_rating: 技术评分,
                            image_num: 图片数,
                            groupon_num: 团购数,
                            discount_num: 优惠数,
                            comment_num: 评论数,
                            favorite_num: 收藏数,
                            checkin_num: 签到数
                        }
                    }
                    ...
                ]
            }
            else return None.
        """
        tag = kwargs.get('tag', '')
        scope = kwargs.get('scope', 1)  # 检索结果详细成都, 1 基本信息, 2 POI详细信息
        # filter字段设置, scope为2时有效
        industry_type = kwargs.get('industry_type', 'cater')  # 行业类型. 取值范围为: hotel 宾馆, cater 餐饮, life 生活娱乐
        # 排序字段. industry_type为hotel时, 取指范围为: default 默认, price 价格, total_score 好评, level: 星级,
        # health_score: 卫生, distance: 距离; 为cater时, default: 默认, taste_rating: 口味, price: 价格,
        # overall_rating: 好评, service_rating: 服务, distance: 距离; 为life时, default: 默认, price: 价格,
        # overall_rating: 好评, comment_num: 服务, distance: 距离
        sort_name = kwargs.get('sort_name', 'default')
        sort_rule = kwargs.get('sort_rule', 0)  # 排序规则, 0 从高到低, 1 从低到高
        groupon = kwargs.get('groupon', 1)  # 是否有团购, 1 有团购, 0 无团购
        discount = kwargs.get('discount', 1)  # 是否有打折, 1 有打折, 0 无打折
        page_size = kwargs.get('page_size', 20)  # 每页数据记录数. 最大返回20条
        page_num = kwargs.get('page_num', 0)  # 页序号
        params = {'query': query, 'output': 'json', 'scope': scope, 'page_size': page_size, 'page_num': page_num,
                  'ak': self.scheduler.next()}
        if scope == 2:
            filter = 'industry_type:{industry_type}|sort_name:{sort_name}|sort_rule:{sort_rule}|groupon:{groupon}|' \
                     'discount:{discount}'.format(industry_type=industry_type, sort_name=sort_name,
                                                  sort_rule=sort_rule, groupon=groupon, discount=discount)
            params['filter'] = filter

        if tag:
            params['tag'] = tag

        params['region'] = region
        r = requests.get(self.search_url, params=params)
        try:
            r.raise_for_status()
            data = json.loads(r.text)
            # print json.dumps(data, ensure_ascii=False)
            if data['status'] == 0:
                # 在状态为0时, 也有可能没有找到搜索结果, 而是返回在其它城市查找到的结果, 返回格式为[{'num': , 'name': ''} ...]这样的数组
                if len(data['results']) > 0:
                    if 'location' in data['results'][0]:
                        return data
                    logging.debug(data['results'])
                    return None
                return data
            else:
                logging.error('failed to get place, return result is %s' % r.text)
                return None
        except Exception as e:
            logging.exception(e)
            return None

    def get_place_all(self, query, region, **kwargs):
        u"""
        根据关键词query查找所有地址信息

        *注意* 百度最多返回400条记录
        :param query: 查询关键词
        :param region: 地区
        :param kwargs:
        :return: if success return
            [
                {
                    name:  POI名称,
                    location: {
                        lat: 纬度,
                        lng: 经度
                    },
                    address: POI地址信息,
                    telephone: POI电话信息,
                    uid: POI的唯一标识,
                    detail_info: {  # POI扩展信息, 仅当scope=2时, 显示该字段, 不同POI类型, 显示的detail_info字段不同
                        distance: 距离中心点距离,
                        type: POI类型,
                        tag: 标签,
                        detail_url: POI的详情页,
                        price: POI商户的价格,
                        shop_hours: 营业时间,
                        overall_rating: 总体评分,
                        taste_rating: 口味评分,
                        service_rating: 服务评分,
                        environment_rating: 环境评分,
                        facility_rating: 星级评分,
                        hygiene_rating: 卫生评分,
                        technology_rating: 技术评分,
                        image_num: 图片数,
                        groupon_num: 团购数,
                        discount_num: 优惠数,
                        comment_num: 评论数,
                        favorite_num: 收藏数,
                        checkin_num: 签到数
                    }
                }
                ...
            ]
            else return []
        """
        data = []
        kwargs.update({'page_num': 0})
        r = self.get_place_by_page(query, region, **kwargs)
        if r is None:
            return data
        data.extend(r['results'])
        total = r['total']
        page_size = kwargs.get('page_size', 20)
        # print "total: %d, page_size: %d" % (total, page_size)
        for i in range(1, total / page_size + 1):
            kwargs.update({'page_num': i})
            r = self.get_place_by_page(query, region, **kwargs)
            if r is None:
                break
            if r['total'] == 0:
                break
            data.extend(r['results'])
        return data

    def get_place_by_uids(self, uids, **kwargs):
        u"""
        Place详情检索服务

        uids最多支持10个
        :param uids: string or list
        :param kwargs: available keys include 'output', 'scope'
        :return: same with get_place_all.
        """
        params = {}
        if isinstance(uids, list):
            params['uids'] = ','.join(uids)
        else:
            params['uid'] = uids
        params['output'] = kwargs.get('output', 'json')  # json or xml 请求返回格式
        params['scope'] = kwargs.get('scope', 1)  # 1 返回基本信息, 2 返回POI详细信息
        params['ak'] = self.scheduler.next()
        try:
            r = requests.get(self.detail_url, params=params)
            r.raise_for_status()

            data = json.loads(r.text)
            if data['status'] == 0:
                return data['result']

            logging.error('failed to get place, return result is %s' % r.text)
            return []
        except Exception as e:
            logging.exception(e)
        return []
