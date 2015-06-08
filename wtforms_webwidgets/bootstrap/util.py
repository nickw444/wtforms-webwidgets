from functools import wraps
from ..common import custom_widget_wrapper
from wtforms.widgets.core import HTMLString

__all__ = ['bootstrap_styled']

def render_field_errors(field):
    """
    Render field errors as html.
    """
    if field.errors:
        html = """<p class="help-block">Error: {errors}</p>""".format(
            errors='. '.join(field.errors)
        )
        return HTMLString(html)

    return None

def render_field_description(field):
    """
    Render a field description as HTML. 
    """
    if hasattr(field, 'description') and field.description != '':
        html = """<p class="help-block">{field.description}</p>"""
        html = html.format(
            field=field
        )
        return HTMLString(html)
    
    return ''


def form_group_wrapped(f):
    """
    Wrap a field within a bootstrap form-group. Additionally sets has-error

    This decorator sets has-error if the field has any errors.
    """
    @wraps(f)
    def wrapped(self, field, *args, **kwargs):
        classes = ['form-group']
        if field.errors:
            classes.append('has-error')

        html = """<div class="{classes}">{rendered_field}</div>""".format(
            classes=' '.join(classes),
            rendered_field=f(self, field, *args, **kwargs)
        )
        return HTMLString(html)

    return wrapped

def meta_wrapped(f):
    """
    Add a field label, errors, and a description (if it exists) to 
    a field. 
    """
    @wraps(f)
    def wrapped(self, field, *args, **kwargs):
        html = "{label}{errors}{original}<small>{description}</small>".format(
            label=field.label(class_='control-label'),
            original=f(self, field, *args, **kwargs),
            errors=render_field_errors(field) or '',
            description=render_field_description(field)
        )
        return HTMLString(html)
    return wrapped

def bootstrap_styled(cls=None, add_meta=True, form_group=True, 
    input_class='form-control'):
    """
    Wrap a widget to conform with Bootstrap's html control design.
    
    
    Args:
        input_class: Class to give to the rendered <input> control.
        add_meta: bool: 
    """

    def real_decorator(cls):
        class NewClass(cls): pass
        NewClass.__name__ = cls.__name__
        NewClass = custom_widget_wrapper(NewClass)

        _call = NewClass.__call__

        def call(*args, **kwargs):
            if input_class:
                kwargs.setdefault('class', input_class)

            return _call(*args, **kwargs)

        if add_meta: call = meta_wrapped(call)
        if form_group: call = form_group_wrapped(call)

        NewClass.__call__ = call
        return NewClass

    if cls:
        # Allow calling decorator(cls) instead of decorator()(cls)
        rv = real_decorator(cls)
        return rv

    return real_decorator


