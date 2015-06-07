from .core import *
from .html5 import *
from .extra import *


# A dictionary of default_widgets to use for different field kinds
# Allows for use of a macro like render_template to override the 
# wtforms default widgets, and means you don't need to supply kwarg
# widget=MyWidget() for every field. 

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
