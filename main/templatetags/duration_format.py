from django import template

register = template.Library()

#Método de formato de fechas a texto para las plantilass

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())

    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600 #Separar en horas y minutos para mostrar un mensaje más amigable
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60

    hours_str = f'{hours}h ' if hours else ''
    minutes_str = f'{minutes}min ' if minutes else ''

    return f'{hours_str}{minutes_str}'