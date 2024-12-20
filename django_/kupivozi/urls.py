from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', admin.site.urls),
    path('/', main, name="main"),
]
