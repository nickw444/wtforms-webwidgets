"""
Widgets for various HTML5 input types from wtforms.widgets.html5
"""

from .util import bootstrap_styled
import wtforms.widgets.html5 as wt_html5
import wtforms.widgets.core as wt_core

import sys
thismodule = sys.modules[__name__]
__all__ = []

#Build the widget classes using our factory in util.py
for widget_name in wt_html5.__all__:
    if issubclass(getattr(wt_html5, widget_name), wt_core.Input):
        new_widget = bootstrap_styled(getattr(wt_html5, widget_name))
        setattr(thismodule, widget_name, new_widget)
        __all__.append(widget_name)
