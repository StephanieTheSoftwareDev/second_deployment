from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg/$', views.reg),
    url(r'^login/$', views.login),
    url(r'^trips/$', views.success),
    url(r'^add_trip/$', views.add_trip),
    url(r'^logout/$', views.logout),
    url(r'^add/$', views.add_to_trips_list),
    url(r'^view_trip_details/(?P<trip_id>\d+)/$', views.view_trip),
    url(r'^delete_trip/(?P<trip_id>\d+)/$', views.delete_trip),
    url(r'^add_this_trip/(?P<other_trips_id>\d+)/$', views.add_this_trip),
    
    # url(r'^success/(?P<id>\d+)/$', views.success),
]
   