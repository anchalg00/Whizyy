"""whizyy URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from blogs.views import home_view,logout_view,blog_view,userpage_view,follow_view,unfollow_view,write_blog
from blogs.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view,name='home'),
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name='logout'),
    path('blogs/<int:category_id>',blog_view,name='blogs'),
    path('writeblogs/',write_blog,name='writeblogs'),
    path('blogs/<slug:blogslug>',single_blog_view,name='single_blog'),
    path('<slug:username>/userpage/',userpage_view,name='userpage'),
    path('follow/<slug:username>',follow_view,name='follow'),
    path('unfollow/<slug:username>',unfollow_view,name='unfollow'),
    path('like/<slug:blogslug>',like_blog,name='like'),
    path('unlike/<slug:blogslug>',unlike_blog,name='unlike'),
    path('ckeditor/',include('ckeditor_uploader.urls')),

    # path('blogs/create_comment/',create_comment_view,name='create_comment'),
    # url(r'^tinymce/', include('tinymce.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

