"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('postcreate', views.postCreate, name='post'),
    path('postedit/<int:id>', views.postEdit, name='postEdit'),
    path('post/<int:id>/<slug:slug>', views.postView, name='postView'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('postdelete/<int:id>', views.postDelete, name='postDelete'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>', views.categoryFilter, name='categoryFilter'),
    path('tags/<slug:slug>', views.tagFilter, name='tagFilter'),
    path('comment/', include('comment.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', views.userLogin, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('contact/', views.contactView, name='contact'),
    path('success/', views.successView, name='success'),
    path('about/', views.aboutMe, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
