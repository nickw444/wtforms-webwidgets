"""
WTForms Extended Widgets.

This package aims to one day eventually contain advanced widgets for all the
common web UI frameworks.

Currently this module contains widgets for:
 
 - Boostrap

A Widget can be identieid as being from this package by being a subclass of
CustomWidgetMixin. This class can be applied by using the custom_widget_wrapper
decorator. 
"""

from .abstract import *
