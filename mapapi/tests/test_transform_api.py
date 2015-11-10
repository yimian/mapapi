# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import unittest
from baidu.scheduler import RoundRobinScheduler
from baidu.transform_api import TransformApi


class TestTransformApi(unittest.TestCase):
    def setUp(self):
        self.scheduler = RoundRobinScheduler(['wwx6xhe8aQncZZUm7QsIPXKI', '9ea66EnDo1YLFuzu5QDDp4zU'])
        self.transform_api = TransformApi(self.scheduler)

    def test_transform_with_single_param(self):
        # python 浮点数精度有限
        coords = self.transform_api.transform({'lat': 29.5754297789, 'lng': 114.218927345})
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 1)
        self.assertEqual(coords[0]['lat'], 29.58158536743)
        self.assertEqual(coords[0]['lng'], 114.22539195408)

    def test_transform_with_list(self):
        coords = self.transform_api.transform([{'lat': 29.5754297789, 'lng': 114.218927345},
                                               {'lat': 29.5754297789, 'lng': 114.218927345}])
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 2)
        self.assertEqual(coords[1]['lat'], 29.58158536743)
        self.assertEqual(coords[1]['lng'], 114.22539195408)


if __name__ == '__main__':
    unittest.main()
