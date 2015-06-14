"""
Additional Widgets Provided for use with Bootstrap
"""
from .util import bootstrap_styled
from ..common import MultiField as _MultiField
from ..common import CustomWidgetMixin
from .core import PlainCheckbox, PlainRadio
import wtforms.widgets.core as wt_core

__all__ = ['JasnyImageInput', 'JasnyFileInput', 'MultiField', 'CheckboxGroup',
           'RadioGroup', 'LabelAboveCheckbox']

from wtforms.widgets import FileInput

@bootstrap_styled(input_class=None)
class JasnyImageInput(CustomWidgetMixin):
    """
    A Jasny-Bootstrap renderer widget. (Requires Jasny-bootstrap js and css)
    """

    def __init__(self):
        
        self._field_renderer = FileInput()

    def __call__(self, field, **kwargs):
        html = """
        <div class="fileinput fileinput-new input-group" data-provides="fileinput">
          <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: 200px; height: 150px;"></div>
          <div>
            <span class="btn btn-default btn-file">
                <span class="fileinput-new">Select image</span>
                <span class="fileinput-exists">Change</span>
                <input type="file" name="...">
                {rendered_field}
            </span>
            <a href="#" class="btn btn-default fileinput-exists" data-dismiss="fileinput">Remove</a>
          </div>
        </div>
        """.format(
            rendered_field=self._field_renderer(field, **kwargs)
        )
        return html


@bootstrap_styled(input_class=None)
class JasnyFileInput(CustomWidgetMixin):
    """
    A Jasny-Bootstrap renderer widget. (Requires Jasny-bootstrap js and css)
    """

    def __init__(self):

        self._field_renderer = FileInput()

    def __call__(self, field, **kwargs):
        html = """
        <div class="fileinput fileinput-new input-group" data-provides="fileinput" style="width:100%;">
            <div class="form-control" data-trigger="fileinput">
                <span class="fileinput-filename"></span>
            </div>
            <span class="input-group-addon btn btn-default btn-file">
            <span class="fileinput-new">Select file</span>
            <span class="fileinput-exists">Change</span>
                {rendered_field}
            </span>
            <a href="#" class="input-group-addon btn btn-default fileinput-exists" data-dismiss="fileinput">Remove</a>
        </div>
        """.format(
            rendered_field=self._field_renderer(field, **kwargs)
        )
        return html


@bootstrap_styled(input_class=None)
class MultiField(_MultiField, CustomWidgetMixin):
    """
    Render a compatible field's choices using the given choice renderer.

    Args: 
        choice_renderer (Widget): The widget to call to render any subfields 
            for this field.
    """

    def __init__(self, choice_renderer):
        self.choice_renderer = choice_renderer


class RadioGroup(MultiField):
    """
    Render a compatible field's possible choices using radio boxes

    An alias of ``MultiField(choice_renderer=PlainRadio())``
    """
    def __init__(self):
        self.choice_renderer = PlainRadio()

class CheckboxGroup(MultiField):
    """
    Render a compatible field's possible choices using check boxes.

    An alias of ``MultiField(choice_renderer=PlainCheckbox())``
    """
    def __init__(self):
        self.choice_renderer = PlainCheckbox()

@bootstrap_styled(input_class='')
class LabelAboveCheckbox(wt_core.CheckboxInput):
    """
    Render a checkbox with it's label above rather than next to it.
    """
    def __call__(self, field, **kwargs):
        field = wt_core.CheckboxInput.__call__(self, field, **kwargs)
        return "<div>{0}</div>".format(field)

