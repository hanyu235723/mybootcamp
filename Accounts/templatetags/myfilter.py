
from django import template
register = template.Library()

@register.filter(name='addattr')
def addattr(field,class_name):
    
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })
    