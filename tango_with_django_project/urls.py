"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include
from rango import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('rango/', include('rango.urls')),
    # 3 - The above maps any URLs starting with rango/ to be handled by rango.
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),

    path('like_page/', views.LikePageView.as_view(), name='like_page'),
    path('dislike_page/', views.DislikePageView.as_view(), name='dislike_page'),

    path('comment_like_page/', views.LikeCommentView.as_view(), name='like_page'),
    path('comment_dislike_page/', views.DislikeCommentView.as_view(), name='dislike_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
