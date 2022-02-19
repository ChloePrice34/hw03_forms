from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace='about')),
    path('author/', include('about.urls', namespace='about_author')),
    path('tech/', include('about.urls', namespace='about_tech')),
]
