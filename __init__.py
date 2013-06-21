#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

'''
Gauge
=====

The :class:`Gauge` widget is a widget for displaying gauge. 

.. note::

Source svg file provided for customing.

'''

__all__ = ('Gauge')

__title__ = 'garden.gauge'
__version__ = '0.1'
__author__ = 'julien@hautefeuille.eu'

import kivy
kivy.require('1.7.1')
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label

class Gauge(Widget):
    '''
    Gauge class

    '''

    unit = NumericProperty(1.8)
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
    file_gauge = StringProperty("cadran.png")
    file_needle = StringProperty("needle.png")
    size_gauge = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        
        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotate=False, 
            do_scale=False,
            do_translation=False
            )

        _img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, 
            self.size_gauge))

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotate=False,
            do_scale=False,
            do_translation=False
            )

        _img_needle = Image(source=self.file_needle, size=(self.size_gauge, 
            self.size_gauge))

        self._gauge.add_widget(_img_gauge)
        self._needle.add_widget(_img_needle)
        
        self.add_widget(self._gauge)
        self.add_widget(self._needle)
        self.add_widget(Label(text='Made with Kivy'))

        self.bind(pos=self._update)
        self.bind(size=self._update)

        Clock.schedule_interval(self._turn, 0)
        
    def _update(self, *args):
        '''
        Update gauge and needle positions after sizing or positioning.

        '''
        self._gauge.pos = (self.x, self.y)
        self._needle.pos = (self.x, self.y)

    def _turn(self, *args):
        '''
        Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.

        '''
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = (50 * self.unit) - (self.value * self.unit)

class GaugeApp(App):
        def build(self):
            import psutil
            def refresh(*args):
                gauge.value = psutil.cpu_percent(interval=1)
            box = BoxLayout(orientation='horizontal', spacing=0, padding=0)
            gauge = Gauge(value=50, size_gauge=256)
            box.add_widget(gauge)
            Clock.schedule_interval(refresh, 0)
            return box
            
if __name__ in ('__main__'):
    GaugeApp().run()