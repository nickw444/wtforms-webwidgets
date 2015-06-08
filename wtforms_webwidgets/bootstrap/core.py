"""
Widgets to override the default widgets provided with wtforms.
"""


import wtforms.widgets.core as wt_core
from .util import bootstrap_styled
from .abstract import BootstrapPlainCheckboxRadio
from ..common import CustomWidgetMixin

__all__ = [
    'PlainCheckbox', 'PlainRadio', 'TextInput', 'PasswordInput', 'HiddenInput',
    'CheckboxInput', 'RadioInput', 'FileInput', 'SubmitInput', 'TextArea',
    'Select'
]

class PlainCheckbox(BootstrapPlainCheckboxRadio):
    """Render a checkbox without any bootstrap container classes."""
    def __init__(self):
        self.input_type = 'checkbox'

class PlainRadio(BootstrapPlainCheckboxRadio):
    """Render a radio without any bootstrap container classes."""
    def __init__(self):
        self.input_type = 'radio'


TextInput = bootstrap_styled(wt_core.TextInput)
PasswordInput = bootstrap_styled(wt_core.PasswordInput)
HiddenInput = wt_core.HiddenInput # We don't need to style this.

CheckboxInput = PlainCheckbox
RadioInput = PlainRadio

FileInput = bootstrap_styled(wt_core.FileInput, input_class=None)

class SubmitInput(wt_core.SubmitInput, CustomWidgetMixin):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class', 'btn btn-default')
        return super(SubmitInput, self).__call__(field, **kwargs)


TextArea = bootstrap_styled(wt_core.TextArea)
Select = bootstrap_styled(wt_core.Select)