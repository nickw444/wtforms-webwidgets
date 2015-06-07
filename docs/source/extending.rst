Extending
=========

Making Widgets For Your Favourite Framework
*******************************************

Create a submodule within this module named the title of the web framework
you wish to bring functionality to. 

When creating widgets from scratch, be sure to apply the 
``wtforms_webwidgets.common.CustomWidgetMixin`` mixin to your class. 

If you are extending an existing wtforms.widgets class, decorate it with 
``wtforms_webwidgets.common.custom_widget_wrapper``. This allows our 
``FieldRenderer`` know this is a custom widget, and not to check the lookup
dictionary to render a field which has this widget.



Contibuting
***********

To contribute your improvements to this library, please fork the repository, 
add functionality and submit a pull request.
