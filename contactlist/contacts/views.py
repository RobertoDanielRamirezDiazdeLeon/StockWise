
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import QuerySet
from contacts.models import Contact
from typing import Any
from django.contrib.auth.views import LoginView
from .models import Contact  # tu modelo de productos
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware.csrf import get_token
from django.conf import settings
from django.http import HttpResponse
# Create your views here.7
"""
class ContactListView(generic.ListView):
    model = Contact
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        q = self.request.GET.get('q')
        if q:
            return Contact.objects.filter(name__icontains=q)
        return super().get_queryset()

class ContactCreateView(generic.CreateView):
    model = Contact
    fields = ('avatar', 'name','email','birth','phone')
    success_url = reverse_lazy('contact_list')

class ContactUpdateView(generic.UpdateView):
    model = Contact
    fields = ('avatar', 'name','email','birth','phone')
    success_url = reverse_lazy('contact_list')

class ContactDeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('contact_list')

class ContactLoginView(LoginView):
    template_name = 'contacts/contact_login.html'
    success_url = reverse_lazy('contact_list')
    def get_success_url(self):
        return self.success_url
    


"""
def home_view(request):
    return render(request, "contacts/contact_home.html")

class ContactSalesListView(generic.TemplateView):
    template_name = "contacts/contact_sales.html"

# LISTADO con búsqueda
class ContactListView(generic.ListView):
    model = Contact
    paginate_by = 5
    template_name = "contacts/contact_list.html"
    login_url = 'login'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return (
                Contact.objects.filter(product__icontains=q) 
                | Contact.objects.filter(code__icontains=q)
            ).order_by("stock")   # 👈 ordena por stock de menor a mayor
        return super().get_queryset().order_by("stock")  # 👈 aquí también



# CREAR producto
class ContactCreateView(generic.CreateView):
    model = Contact
    fields = (
        'avatar',
        'code',
        'product',
        'category',
        'price',
        'stock',
        'supplier',
        'description',
    )
    success_url = reverse_lazy('contact_list')
    template_name = "contacts/contact_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # 👈 guarda el creador
        form.instance.updated_by = self.request.user  # 👈 también como último editor inicial
        return super().form_valid(form)

# EDITAR producto
class ContactUpdateView(generic.UpdateView):
    model = Contact
    fields = (
        'avatar',
        'code',
        'product',
        'category',
        'price',
        'stock',
        'supplier',
        'description',
    )
    success_url = reverse_lazy('contact_list')
    template_name = "contacts/contact_form.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user  # 👈 actualiza último editor
        return super().form_valid(form)


# ELIMINAR producto
class ContactDeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('contact_list')
    template_name = "contacts/contact_confirm_delete.html"


# LOGIN de usuarios (si lo usas)
class ContactLoginView(LoginView):
    template_name = 'contacts/contact_login.html'
    success_url = reverse_lazy('contact_list')

    def get_success_url(self):
        return self.success_url


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
        else:
            return render(request, 'contacts/contact_login.html', {
                'error': 'Credenciales incorrectas',
                'csrf_token': get_token(request)  # <-- asegúrate que haya token
            })
    return render(request, 'contacts/contact_login.html', {
        'csrf_token': get_token(request)
    })

def logout_view(request):
    logout(request)
    return redirect('login')

