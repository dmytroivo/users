"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^user', views.user_html,name='user'),
        url(r'^plan', views.plan_html,name='plan'),
        url(r'^editplan', views.editplan_html,name='editplan'),
        url(r'^delete_by_id', views.delete_by_id),
        url(r'^edituser', views.edituser_html,name='edituser'),
        url(r'^delete_user_by_id', views.delete_user_by_id),
        url('', views.index_html,name='index')
]

#    url(r'^err/', TemplateView.as_view(template_name='err.html'))