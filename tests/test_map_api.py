# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import unittest
from baidu import MapApi


class TestMapApi(unittest.TestCase):
    def setUp(self):
        self.map_api = MapApi(['wwx6xhe8aQncZZUm7QsIPXKI', '9ea66EnDo1YLFuzu5QDDp4zU'])

    def test_location_api(self):
        detail = self.map_api.location_api.get_detail_location_by_address(u'百度大厦', u'北京')
        self.assertIsNotNone(detail)
        self.assertEqual(detail['precise'], 1)
        self.assertEqual(detail['confidence'], 80)
        self.assertEqual(detail['level'], u'商务大厦')
        self.assertEqual(detail['location']['lng'], 116.30783584945)
        self.assertEqual(detail['location']['lat'], 40.056876296398)

    def test_place_api(self):
        ret = self.map_api.place_api.get_place_by_page(u'银行', u'济南')
        self.assertIsNotNone(ret)
        self.assertEqual(len(ret['results']), 20)

    def test_transform_api(self):
        coords = self.map_api.transform_api.transform({'lat': 29.5754297789, 'lng': 114.218927345})
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 1)
        self.assertEqual(coords[0]['lat'], 29.58158536743)
        self.assertEqual(coords[0]['lng'], 114.22539195408)

if __name__ == '__main__':
    unittest.main()
