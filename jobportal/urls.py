from django.contrib import admin
from django.urls import path
from campus.views import (
    home,
    companies,
    institutes,
    opportunities,
    recruitment_detail,
    applications,
    analytics
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('companies/', companies, name='companies'),

    path('institutes/', institutes, name='institutes'),

    path('opportunities/', opportunities, name='opportunities'),

    path(
        'opportunities/<int:recruitment_role_id>/',
        recruitment_detail,
        name='recruitment_detail'
    ),

    path('applications/', applications, name='applications'),
    path('analytics/', analytics, name='analytics'),
]