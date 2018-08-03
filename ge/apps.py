# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class GeConfig(AppConfig):
    name = 'ge'
    verbose_name = 'Geografía Electoral'

    def ready(self):
        import ge.signals
