Usage In Flask (And Others)
###########################

When declaring fields as part of a form using WTForms, if you wished to set 
a custom widget for a field, you would need to set `widget=MyWidget()`. 

I have found when overriding all widgets with some skinned widgets, it's 
very tedious and prone to errors to set this value every time. Instead, it is 
more intuitive to set a dictionary of defaults, and look up field types and get
their apropriate widget. 

To use this method we need:
 
 1. A way of identifying when a widget has been set from the Field kwargs.
 2. A way of overriding a default widget when it is not provided.

I have found that it is most aproriatly done within a ``render_field`` 
templating macro. 

Provided within the common submodule of this framework is the class 
``FieldRenderer``. This class provides an interface for setting a lookup table
for default renderers and a method to render a given field. 


.. autoclass:: wtforms_webwidgets.FieldRenderer
    :members:


Example
=======

An example from Flask/Jinja.

.. code:: python

    from wtforms_webwidgets import FieldRenderer
    from wtforms_webwidgets.bootstrap import default_widgets

    renderer = FieldRenderer(lookup_dict=default_widgets)

    # Alternatively, you can declare your own lookup dictionary:
    import wtforms_webwidgets.bootstrap as wt_bs
    renderer = FieldRenderer(lookup_dict={
        'TextField': wt_bs.TextInput(),
    })

    # Example for injecting into Jinja within Flask
    app.jinja_env.globals['render_field'] = renderer


Now, within your templates you can do the following:

.. code:: html

    {{ render_field(form.my_field) }}

If the widget was not declared with a custom widget, it will be renderered
accordingly to the FieldRender's lookup dictionary.