# -*- coding: utf-8 -*-
""" use as main map interface. """

from scheduler import RoundRobinScheduler
from location_api import LocationApi
from place_api import PlaceApi
from transform_api import TransformApi


class MapApi(object):
    def __init__(self, aks=None, scheduler=None, **kwargs):
        super(MapApi, self).__init__()
        self.aks = aks
        self.scheduler = scheduler
        self._place_api_inst = None
        self._location_api_inst = None
        self._transform_api_inst = None

    def set_aks(self, aks):
        """
        set application keys.

        :param aks: list of application keys
        """
        self.aks = aks

    def set_scheduler(self, scheduler):
        """
        set scheduler.

        :param scheduler:
        """
        self.scheduler = scheduler

    @property
    def place_api(self):
        """
        get place api interface.

        :return: PlaceApi instance.
        """
        if self._place_api_inst:
            return self._place_api_inst
        if not self.scheduler:
            self.scheduler = RoundRobinScheduler(self.aks)
        self._place_api_inst = PlaceApi(self.scheduler)
        return self._place_api_inst

    @property
    def location_api(self):
        """
        get location api interface.

        :return: LocationApi instance.
        """
        if self._location_api_inst:
            return self._location_api_inst
        if not self.scheduler:
            self.scheduler = RoundRobinScheduler(self.aks)
        self._location_api_inst = LocationApi(self.scheduler)
        return self._location_api_inst

    @property
    def transform_api(self):
        """
        get transform api interface.

        :return: TransformApi instance.
        """
        if self._transform_api_inst:
            return self._transform_api_inst
        if not self.scheduler:
            self.scheduler = RoundRobinScheduler(self.aks)
        self._transform_api_inst = TransformApi(self.scheduler)
        return self._transform_api_inst
