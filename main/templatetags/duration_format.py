from django import template

register = template.Library()

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())

    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60

    hours_str = f'{hours}h ' if hours else ''
    minutes_str = f'{minutes}min ' if minutes else ''

    return f'{hours_str}{minutes_str}'