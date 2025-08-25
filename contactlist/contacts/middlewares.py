from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware que obliga a estar logueado para ver cualquier página
    excepto login, logout y admin.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs exactas exentas
        exempt_urls = [
            reverse('login'),     # '/'
            reverse('logout'),    # '/logout/'
            '/admin/',            # admin
        ]

        # Permitir estáticos y media
        if request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
            return self.get_response(request)

        # Si no está autenticado y no es una URL exenta
        if not request.user.is_authenticated:
            # comprobar igualdad exacta o admin subpaths
            if request.path not in exempt_urls and not request.path.startswith('/admin/'):
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)
