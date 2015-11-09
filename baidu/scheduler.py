# -*- coding: utf-8 -*-

from exceptions import ParamError


class BaseScheduler(object):
    """
    use as scheduler base class.
    """
    def __init__(self, aks):
        super(BaseScheduler, self).__init__()
        self.aks = aks

    def next(self):
        raise NotImplementedError


class RoundRobinScheduler(BaseScheduler):
    """
    implement round-robin poll scheduler algorithm
    """
    def __init__(self, aks):
        super(RoundRobinScheduler, self).__init__(aks)
        self.cur_index = 0

    def next(self):
        if len(self.aks) < 1:
            raise ParamError(u'aks不能为空')
        ak = self.aks[self.cur_index]
        self.cur_index += 1
        if self.cur_index == len(self.aks):
            self.cur_index = 0
        return ak
