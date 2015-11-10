# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import unittest
from baidu.scheduler import RoundRobinScheduler
from baidu.place_api import PlaceApi
import logging


class TestPlaceApi(unittest.TestCase):
    def setUp(self):
        self.scheduler = RoundRobinScheduler(['wwx6xhe8aQncZZUm7QsIPXKI', '9ea66EnDo1YLFuzu5QDDp4zU'])
        self.place_api = PlaceApi(self.scheduler)

    def test_get_place_by_page(self):
        ret = self.place_api.get_place_by_page(u'银行', u'济南')
        self.assertIsNotNone(ret)
        self.assertEqual(len(ret['results']), 20)

    def test_get_place_all(self):
        ret = self.place_api.get_place_by_page(u'银行', u'济南')
        self.assertIsNotNone(ret)
        total = ret['total']
        logging.debug('total: %d' % total)  # 不起作用
        ret = self.place_api.get_place_all(u'银行', u'济南')
        self.assertIsNotNone(ret)
        self.assertEqual(len(ret), total)

    def test_get_place_by_uids_with_string(self):
        place = self.place_api.get_place_by_uids('c14fc238f7fadd4ea5da390f')
        self.assertIsNotNone(place)
        self.assertEqual(place['name'], u'觉品壹号')
        places = self.place_api.get_place_by_uids(['c14fc238f7fadd4ea5da390f', '5a8fb739999a70a54207c130'])
        self.assertIsNotNone(places)
        self.assertEqual(len(places), 2)
        self.assertEqual(places[1]['name'], u'百度大厦员工食堂')


if __name__ == '__main__':
    unittest.main()
