
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Project Acceptance Predictor Admin"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Admin Panel"

urlpatterns = [
    path('', include('logistic.urls')),
    path('admin/', admin.site.urls),
]
