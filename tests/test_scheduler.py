# -*- coding: utf-8 -*-
__author__ = 'zhangjinjie'

import unittest
from baidu.scheduler import RoundRobinScheduler
from baidu.exceptions import ParamError


class TestRoundRobinScheduler(unittest.TestCase):
    def test_next_with_correct_aks(self):
        scheduler = RoundRobinScheduler(['wwx6xhe8aQncZZUm7QsIPXKI', '9ea66EnDo1YLFuzu5QDDp4zU'])
        self.assertEqual(scheduler.next(), 'wwx6xhe8aQncZZUm7QsIPXKI')
        self.assertEqual(scheduler.next(), '9ea66EnDo1YLFuzu5QDDp4zU')
        self.assertEqual(scheduler.next(), 'wwx6xhe8aQncZZUm7QsIPXKI')

    def test_next_with_empty_aks(self):
        scheduler = RoundRobinScheduler([])
        with self.assertRaises(ParamError):
            scheduler.next()


if __name__ == '__main__':
    unittest.main()
