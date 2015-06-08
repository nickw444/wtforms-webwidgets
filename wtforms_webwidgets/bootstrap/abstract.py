"""
A set of abstract widgets which require a subclass to be useful.
"""

from wtforms.widgets.core import Input, HTMLString
from abc import ABCMeta
from ..common import CustomWidgetMixin

class BootstrapPlainCheckboxRadio(Input, CustomWidgetMixin):
    """
    Abstract widget for a Bootstrap Checkbox or Radio implementation.
    """
    __metaclass__ = ABCMeta
    def __call__(self, field, **kwargs):
        label = getattr(field, 'label', None)
        if label in kwargs:
            label = kwargs.pop('label').strip()

        html = """
        <div class="{input_type}">
            <label>{rendered_field}{label}</label>
        </div>
        """.format(
            label=label,
            input_type=self.input_type,
            rendered_field=super(BootstrapPlainCheckboxRadio, self).__call__(field, **kwargs)
        )
        return HTMLString(html)