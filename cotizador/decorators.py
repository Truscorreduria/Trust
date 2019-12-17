from django.urls import reverse
from functools import wraps
from django.http import HttpResponseRedirect


def profile_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous:
            profile = request.user.profile()
            if profile.perfil_completo() and not profile.cambiar_pass:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('cotizador:perfil'))
        else:
            return HttpResponseRedirect(reverse('cotizador:login'))

  return wrap