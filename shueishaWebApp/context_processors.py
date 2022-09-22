from django.contrib.auth.models import User

# Método para añadir la variable 'me' al contexto de la solicitud
def project_context(request):
    context = {
        'me' : User.objects.first(), # Tomar el primer objeto de la consulta a la tabla User
    }
    return context