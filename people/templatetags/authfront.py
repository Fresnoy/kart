from django import template

register = template.Library()

@register.simple_tag
def authfront_reset_password_url(token):
    return "canard"
