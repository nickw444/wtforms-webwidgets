"""
Provides numerous WTForms widgets skinned for use with bootstrap.
"""

from .core import *
from .html5 import *
from .extra import *

default_widgets = {
    # Multi Types
    'SelectMultipleField': Select(multiple=True),
    'SelectField': Select(),
    'QuerySelectMultipleField': Select(multiple=True),
    'QuerySelectField': Select(),
    'RadioField': RadioGroup(),

    # Input Types
    'DateField': DateInput(),
    'TextField': TextInput(),
    'StringField': TextInput(),
    'PasswordField': PasswordInput(),
    
    'BooleanField': CheckboxInput(),
    'FileField': FileInput(),
    'SubmitField': SubmitInput(),
}
