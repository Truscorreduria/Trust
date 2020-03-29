from django.urls import reverse
from functools import wraps
from django.http import HttpResponseRedirect
from backend.models import get_profile


def profile_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous:
            profile = get_profile(request.user)
            if profile.perfil_completo() and not profile.cambiar_pass:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('cotizador:perfil'))
        else:
            return HttpResponseRedirect(reverse('cotizador:login'))

    return wrap
