# -*- coding: utf-8 -*-
""" use as main map interface. """

from scheduler import RoundRobinScheduler


class MapApi(object):
    def __init__(self, aks=None, **kwargs):
        super(MapApi, self).__init__()
        self.aks = aks

    def set_aks(self, aks):
        """
        set application keys.

        :param aks: list of application keys
        """
        self.aks = aks

    def place_api(self):
        """
        get place api interface.
        """
        pass

    def geo_api(self):
        pass

    def transform_api(self):
        pass
