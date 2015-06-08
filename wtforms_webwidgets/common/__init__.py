"""
The common library is used to house common library functionality of 
wtforms-webwidgets. Additionally, it houses widgets in the form of abstract 
classes. 

When creating a new control, make a generic version of the control in 
the common library, and extend its functionality for the Web framework of your 
choice. This will allow faster future extension of other web frameworks.
"""

from wtforms.widgets.core import html_params, CheckboxInput, HTMLString
from functools import wraps
from abc import ABCMeta


__all__ = ['custom_widget_wrapper', 'CustomWidgetMixin','MultiField', 
'FieldRenderer']

class CustomWidgetMixin(object):
    """
    A mixin to apply to a widget to identify it as a non-wtforms builtin.
    """
    __metaclass__ = ABCMeta
    __webwidget__ = True


def custom_widget_wrapper(cls):
    """
    A decorator to wrap a widget to identify it as non-wtforms builtin.
    """
    cls.__webwidget__ = True
    return cls


class FieldRenderer(object):
    """
    Injectable renderer class for templating frameworks. 

    Args:
        lookup_dict (dict): The dictionary to look up field types to find their default
            render type.
    """

    def __init__(self, lookup_dict):
        self._lookup = lookup_dict

    def __call__(self, field, **kwargs):
        """
        Return a rendered field.
        Checks to see if the field has a custom widget set. If it does not have
        a custom widget, the field type is looked up in the lookup dictionary
        to get the default renderer for this field type. 

        If you wish to not perform any lookup, simply call field() without 
        invoking this method. This method simply overrides a field's widget
        value.

        Args:
            field (wtforms.Field): The Field to render.
        """
        if not hasattr(field.widget, '__webwidget__'):
            if field.type in self._lookup:
                field.widget = self._lookup[field.type]

        return field(**kwargs)


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
        if field.iter_choices():
            for value, label, checked in field.iter_choices():
                choice_id = u'%s-%s' % (field_id, value)
                options = dict(kwargs, label=label, value=value, id=choice_id)
                if checked:
                    options['checked'] = 'checked'

                field.checked = checked 
                field.label.text = label
                html.append(self.choice_renderer(field, **options))

        html.append(u'</div>')
        return HTMLString(u''.join(html))
