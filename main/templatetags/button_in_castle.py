from django import template
from main.models import Castle

register = template.Library()


@register.inclusion_tag("main/tag_button.html")
def tags():
    pass
