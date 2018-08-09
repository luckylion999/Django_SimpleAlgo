from django.conf.urls import url
from main import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^plot/', views.plot, name='plot'),
    url(r'^ajax/save_data/$', views.save_data, name='save_data'),
]