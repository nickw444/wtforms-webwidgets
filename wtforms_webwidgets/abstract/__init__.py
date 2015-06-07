"""
Declare additional inputs in an unthemed manor.
This allows additional skinning without re-implementation.
"""

from wtforms.widgets.core import html_params, CheckboxInput, HTMLString
from functools import wraps
from abc import ABCMeta


__all__ = ['custom_widget_wrapper', 'CustomWidgetMixin','MultiField']

class CustomWidgetMixin(object):
    pass


def custom_widget_wrapper(cls):
    """
    Declare a decorator to wrap a widget to identify it as non-wtforms builtin.

    Flask-Boilerplate-Utils uses this to determine the apropriate widget to use
    """
    class Wrapped(cls, CustomWidgetMixin): pass
    Wrapped.__name__ = cls.__name__
    return Wrapped


class MultiField(CustomWidgetMixin):
    """
    Render a compatible field's iter_choices using a given choice renderer.
    """
    __metaclass__ = ABCMeta

    def __init__(self, choice_renderer):
        self.choice_renderer = choice_renderer

    def __call__(self, field, container_class='', **kwargs):
        field_id = kwargs.pop('id', field.id)

        html = [u'<div {0}>'.format(html_params(id=field_id, class_=container_class))]
        for value, label, checked in field.iter_choices():
            choice_id = u'%s-%s' % (field_id, value)
            options = dict(kwargs, label=label, value=value, id=choice_id)
            if checked:
                options['checked'] = 'checked'

            field.checked = checked 
            html.append(self.choice_renderer(field, **options))

        html.append(u'</div>')
        return HTMLString(u''.join(html))
