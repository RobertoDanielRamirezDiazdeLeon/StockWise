from django.urls import path
from contacts import views
from contacts.views import login_view
from .views import home_view
from .views import (
    ContactListView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
    ContactLoginView,  # Importa la nueva vista
    logout_view
)
urlpatterns = [
    path('', login_view, name='login'),  # Login en la raíz
    path('main/', views.ContactListView.as_view(), name='contact_list'),
    path('new/', views.ContactCreateView.as_view(), name='contact_new'),
    path('<int:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_edit'),
    path('<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    path('logout/', views.logout_view, name='logout'),
    path("sales/", views.ContactSalesListView.as_view(), name="sales"),
    path("home/", home_view, name="home"),
]