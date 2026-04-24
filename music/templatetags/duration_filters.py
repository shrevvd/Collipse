from django import template

register = template.Library()

@register.filter
def format_duration(seconds):
    if not seconds:
        return "--:--"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"