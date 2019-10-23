"""vpn_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vpn_project.apps.vpn_app import views

from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^api/', include('vpn_project.apps.vpn_app.urls')),

    path('',views.index),
    path('admin/', admin.site.urls),
    path('companies/', TemplateView.as_view(template_name='companies.html')),
    path('users/', TemplateView.as_view(template_name='users.html')),
    path('abusers/', views.show_abusers, name='show_abusers'),
    path('show_report/<int:month>', views.show_report, name='show_report'),



# -------------------------------------------------------------------------------------------
# ------------------------------------- Old options -----------------------------------------
# -------------------------------------------------------------------------------------------

    path('companies2/', views.companies_list, name="companies_list"),
    path('companies/edit/<int:pk>', views.edit_company, name="edit_company", ),
    path('companies/new_company/', views.add_company),
    path('companies/delete/<int:pk>/', views.delete_company),

    path('users2/', views.users_list, name="users_list"),
    path('users/edit/<int:pk>', views.edit_user, name="edit_user", ),
    path('users/new_user/', views.add_user),
    path('users/delete/<int:pk>/', views.delete_user),

    path('abusers2/', views.abusers, name='abusers'),
    path('gen_data/', views.generate_data, name='gen_data'),
    path('report/', views.create_report, name='create_report'),

]
