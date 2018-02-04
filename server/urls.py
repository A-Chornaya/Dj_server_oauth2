from . import views
from django.conf.urls import url

app_name = 'server'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^app/add/$', views.register_app, name='app_add'),
    url(r'^app/$', views.info_app, name='app_info'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^oauth/authorize/$', views.authorize, name='authorize'),
    url(r'^oauth/token/$', views.token, name='token'),
    url(r'^error/$', views.error, name='error'),
    ]

