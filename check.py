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

@app.route('/')
def index():
    return render_template_string(
    """
    <h3>WTForms-Webwidgets</h3>
    <ul>
        <li><a href="{{ url_for('.bootstrap') }}">Bootstrap Sample Form</a></li>
    </ul>
    """
    )


# -----------------------------------
# Dynamic Instantiation of all wt_bs.
# -----------------------------------
import wtforms as wt
import wtforms_webwidgets.bootstrap as wt_bs

bs_fields = {
    'core': [
        (wt.BooleanField, wt_bs.PlainCheckbox(),{}),
        (wt.BooleanField, wt_bs.PlainRadio(),{}),
        (wt.TextField, wt_bs.TextInput(),{}),
        (wt.PasswordField, wt_bs.PasswordInput(),{}),
        (wt.HiddenField, wt_bs.HiddenInput(),{}),
        (wt.FileField, wt_bs.FileInput(),{}),
        (wt.SubmitField, wt_bs.SubmitInput(),{}),
        (wt.TextField, wt_bs.TextArea(),{}),
        (wt.SelectField, wt_bs.Select(),{'choices':[('choice1','Choice1'), ('choice2','Choice2')]}),
        (wt.SelectMultipleField, wt_bs.Select(multiple=True),{'choices':[('choice1','Choice1'), ('choice2','Choice2')]}),
    ],
    'extra': [
        (wt.FileField, wt_bs.JasnyFileInput(),{'name_override':'JasnyFileInput'}),
        (wt.BooleanField, wt_bs.LabelAboveCheckbox(),{}),
        (wt.SelectMultipleField, wt_bs.RadioGroup(), {'choices':[('choice1','Choice1'), ('choice2','Choice2')]}),
        (wt.SelectMultipleField, wt_bs.CheckboxGroup(), {'choices':[('choice1','Choice1'), ('choice2','Choice2')]}),
    ],
    'html5': [],
}

# Do HTML forms too.
for widget in wt_bs.html5.__all__:
    bs_fields['html5'].append(
        (wt.TextField, getattr(wt_bs.html5, widget)(), {'name_override': widget})
    )

bs_forms = dict()
i = 0
for group, data in bs_fields.items():
    class WidgetCls(Form): pass
    class NoWidgetCls(Form): pass

    for fieldtype, fieldwidget, kwargs in data:
        
        widget_name = fieldwidget.__class__.__name__
        if 'name_override' in kwargs:
            widget_name = kwargs.pop('name_override')

        widget_name = '{}(widget={})'.format(
            fieldtype.__name__, 
            widget_name
        )
        widget = fieldtype(widget_name, widget=fieldwidget, **kwargs)

        nowidget_name = '{}()'.format(
            fieldtype.__name__
        )
        nowidget = fieldtype(nowidget_name, **kwargs)

        setattr(WidgetCls, str(i), widget)
        setattr(NoWidgetCls, str(i), nowidget)

        i+=1

    bs_forms[group] = (WidgetCls, NoWidgetCls)

def inst_forms():
    forms = dict()
    i = 0
    for group, data in bs_forms.items():
        forms[group] = (data[0](prefix=str(i)), data[1](prefix=str(i+1)))
        i+=2

    return forms

# -------------
# Show All Fields for BS.
# -------------

from wtforms_webwidgets.bootstrap import default_widgets
@app.route('/bootstrap')
def bootstrap():
    renderer = FieldRenderer(default_widgets)
    forms = inst_forms()

    return render_template_string(
        """
        <head>
        <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" />
        <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script> 
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/css/jasny-bootstrap.min.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min.js"></script>
        </head>
        <body>
            <div class="container-fluid">
                <h2>Bootstrap</h2>
                
                {% for group, data in forms.items() %}
                    <h3>{{ group }}</h3>
                    <div class="row">
                    {% for name, form in [('With Widget Defined', data[0]), ('Without Widget Defined', data[1])] %}
                        <div class="col-xs-6">
                        <h4>{{ name }}</h4>
                        <div class="row">
                            <div class="col-xs-6"><strong>{{ '{{ field }}' }}</strong></div>
                            <div class="col-xs-6"><strong>{{ '{{ _render_field(field) }}' }}</strong></div>
                        </div>
                        {% for field in form %}
                            <div class="row">
                                <div class="col-xs-6">
                                    {{ field() }}
                                </div>
                                <div class="col-xs-6">
                                    {{ render_field(field) }}
                                </div>
                            </div>
                        {% endfor %}
                        </div>
                    {% endfor %}
                    </div>
                {% endfor %}


            </div>
        </body>
        """, 
        forms=forms,
        render_field=renderer,
        bs_forms=bs_forms
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)