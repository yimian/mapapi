# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import unittest
from baidu.location_api import LocationApi
from baidu.scheduler import RoundRobinScheduler


class TestLocationApi(unittest.TestCase):
    def setUp(self):
        self.scheduler = RoundRobinScheduler(['wwx6xhe8aQncZZUm7QsIPXKI', '9ea66EnDo1YLFuzu5QDDp4zU'])
        self.location_api = LocationApi(self.scheduler)

    def test_get_detail_location_by_address(self):
        detail = self.location_api.get_detail_location_by_address(u'百度大厦', u'北京')
        self.assertIsNotNone(detail)
        self.assertEqual(detail['precise'], 1)
        self.assertEqual(detail['confidence'], 80)
        self.assertEqual(detail['level'], u'商务大厦')
        self.assertEqual(detail['location']['lng'], 116.30783584945)
        self.assertEqual(detail['location']['lat'], 40.056876296398)

    def test_get_location_by_address(self):
        location = self.location_api.get_location_by_address(u'百度大厦', u'北京')
        self.assertIsNotNone(location)
        self.assertEqual(location['lat'], 40.056876296398)
        self.assertEqual(location['lng'], 116.30783584945)

    def test_get_detail_address_by_location(self):
        detail = self.location_api.get_detail_address_by_location({'lng': 116.322987, 'lat': 39.983424})
        self.assertIsNotNone(detail)
        self.assertEqual(detail['formatted_address'], u'北京市海淀区中关村大街27号1101-08室')
        self.assertEqual(detail['business'], u"中关村,人民大学,苏州街")
        self.assertEqual(detail['addressComponent']['province'], u'北京市')
        self.assertEqual(detail['addressComponent']['city'], u'北京市')

    def test_get_address_by_location(self):
        address = self.location_api.get_address_by_location({'lng': 116.322987, 'lat': 39.983424})
        self.assertIsNotNone(address)
        self.assertEqual(address['province'], u'北京')
        self.assertEqual(address['city'], u'北京')

    def test_get_province_by_location(self):
        province = self.location_api.get_province_by_location({'lng': 116.322987, 'lat': 39.983424})
        self.assertIsNotNone(province)
        self.assertEqual(province, u'北京')

    def test_get_formatted_province(self):
        province = self.location_api.get_formatted_province(u'北京市海淀区百度大厦')
        self.assertIsNotNone(province)
        self.assertEqual(province, u'北京')

    def test_get_formatted_address(self):
        address = self.location_api.get_formatted_address(u'北京市海淀区百度大厦')
        self.assertIsNotNone(address)
        self.assertEqual(address['province'], u'北京')
        self.assertEqual(address['city'], u'北京')

    def test_get_formatted_detail_address(self):
        detail = self.location_api.get_formatted_detail_address(u'北京市海淀区百度大厦')
        self.assertIsNotNone(detail)
        self.assertEqual(detail['addressComponent']['province'], u'北京市')
        self.assertEqual(detail['addressComponent']['city'], u'北京市')


if __name__ == '__main__':
    unittest.main()
