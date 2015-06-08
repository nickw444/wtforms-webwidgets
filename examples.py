"""
A Flask app to render all fields using different methods.
"""

from flask import Flask, render_template_string
from flask_wtf import Form
from wtforms_webwidgets import FieldRenderer


app = Flask(__name__)
app.config.update({
    'WTF_CSRF_ENABLED': False
})
@app.after_request
def after(response):
    return response

@app.route('/')
def index():
    return render_template_string("""
    <head>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" />
    <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script> 
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/css/jasny-bootstrap.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min.js"></script>
    </head>
    <body>
    <div class="container">
    <h3>WTForms-Webwidgets</h3>
    <ul>
        <li><a href="{{ url_for('.basic') }}">Basic Usage</a></li>
        <li><a href="{{ url_for('.fieldrenderer') }}">Using a Field Renderer</a></li>
        <li><a href="{{ url_for('.defaults') }}">Setting Defaults</a></li>
    </ul>
    </div>
    </body>
    """)


import wtforms as wt
import wtforms_webwidgets.bootstrap as wt_bs

"""
Basic Form
**********
This is the standard usage that WTForms suggests to use.
This method involves setting widget=MyWidget() on every field that you wish to
customise/set.

See docs for available widgets for Bootstrap.
"""
class BasicForm(Form):
    textfield = wt.TextField('My Text Field', widget=wt_bs.TextInput())
    textfield_no = wt.TextField('My Text Field Without Widget')
    filefield = wt.FileField('My File Upload', widget=wt_bs.FileInput())
    filefield_no = wt.FileField('My File Upload Without Widget')
    imagefield = wt.FileField('My Image Upload', widget=wt_bs.JasnyImageInput())

@app.route('/basic')
def basic():
    form = BasicForm()

    return render_template_string("""
    <head>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" />
    <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script> 
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/css/jasny-bootstrap.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min.js"></script>
    </head>
    <body>
    <div class="container">
        <h3>Basic Form</h3>
        {{ form.textfield }}
        {{ form.textfield_no }}
        {{ form.filefield }}
        {{ form.filefield_no }}
        {{ form.imagefield }}
    </div>
    </body>
    """, form=form)


"""
Field Renderer
**************
Using a field renderer allows a function to decide which widget to use 
automatically, given an input dictionary with your default options.

use a FieldRenderer() as a render_field macro in your template. A FieldRenderer
will automatically decide which widget to render a field with by looking it 
up in its dictionary. 

    * If a field does not exist in the dictionary, it's default widget will be used
    * If a field already has a widget from this package specified, the field
      will be rendered using that widget. (See Example 1)
    * If a field has a widget from a different package, that widget will be
      overridden. You can stop this behaviour by not using the render_field
      (or similar) macro for this field. (See Example 2)

"""
from wtforms_webwidgets import FieldRenderer

class FieldRendererForm(Form):
    textfield = wt.TextField('My Text Field', widget=wt_bs.TextInput())
    textfield_no = wt.TextField('My Text Field Without Widget')

    # Declare a textField to use a PasswordInput (Example 1)
    passwordfield = wt.TextField('My Pass Field', widget=wt_bs.PasswordInput())
    passwordfield_no = wt.TextField('My Pass Field Without Widget')

    filefield = wt.FileField('My File Upload', widget=wt_bs.FileInput())
    filefield_no = wt.FileField('My File Upload Without Widget')

renderer_defaults = {
    'TextField': wt_bs.TextInput()    
}
@app.route('/fieldrenderer')
def fieldrenderer():
    renderer = FieldRenderer(renderer_defaults)
    form = FieldRendererForm()

    return render_template_string("""
    <head>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" />
    <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script> 
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/css/jasny-bootstrap.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min.js"></script>
    </head>
    <body>
    <div class="container">
        <h3>Field Renderer Form</h3>
        {{ render_field(form.textfield) }}
        {{ render_field(form.textfield_no) }}
        {{ render_field(form.filefield) }}
        {{ render_field(form.filefield_no) }}

        <hr />
        {# Example 1 #}
        <p>
            Rendering the passwordfield which has a widget= set will render
            using the given original widget (first field). 
        </p>
        <p>
            Since no widget was given to the second, it used the default
            for the type 'TextField'
        </p>
        {{ render_field(form.passwordfield) }}
        {{ render_field(form.passwordfield_no) }}

        <hr />
        {# Example 2 #}
        <p>You may find you wish to render the default field style.</p>
        <p>To do this, just don't specify render_field on a field without a widget</p>
        {{ form.textfield_no }}

    </div>
    </body>
    """, form=form, render_field=renderer)


"""
Setting Defaults
****************
Since using a field renderer brings easier widget rendering without specifying,
it's often useful to override an entire library.

Take the bootstrap submodule from this package. It exposes a ``default_widgets``
dictionary.

Using a FieldRenderer, we can use this dictionary to have our fields rendered
without providing widget= for each field. 

Since ``default_widgets`` is a dictionary, you can override specific keys to 
change the default widgets for specific field types. (Example 2)
"""
from wtforms_webwidgets import FieldRenderer

class SettingDefaultsForm(Form):
    textfield = wt.TextField('My Text Field')
    passwordfield = wt.PasswordField('My Pass Field')
    passwordfield_expl = wt.PasswordField('My Pass Field With Explicit Widget', widget=wt_bs.PasswordInput())
    filefield = wt.FileField('My File Upload')

renderer_defaults_custom = wt_bs.default_widgets

# Make PasswordField's render with TextInput by default. (Example 2)
renderer_defaults_custom['PasswordField'] = wt_bs.TextInput()

@app.route('/defaults')
def defaults():
    renderer = FieldRenderer(renderer_defaults_custom)
    form = SettingDefaultsForm()

    return render_template_string("""
    <head>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" />
    <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script> 
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/css/jasny-bootstrap.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min.js"></script>
    </head>
    <body>
    <div class="container">
        <h3>Field Renderer Form</h3>
        {{ render_field(form.textfield) }}
        {{ render_field(form.filefield) }}
        {{ render_field(form.passwordfield) }}
        <hr />
        <p>The following field we explicitly set widget=wt_bs.PasswordInput. </p>
        <p>
           Although the field type of this control is PasswordField, the defaults
           say all PasswordField's should be rendered using TextInput. Since we explicitly
           defined the widget for this field, it will be rendered using wt_bs.PasswordInput
        </p>
        {{ render_field(form.passwordfield_expl) }}

    </div>
    </body>
    """, form=form, render_field=renderer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
