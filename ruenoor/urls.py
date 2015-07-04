"""ruenoor URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api
from robots.api import *
from robots.views import simple_view, root_view, signal_data

#admin.autodiscover()

# tasty-pie definitions
v1_api = Api(api_name='v1')

# equipment resources
v1_api.register(SystemResource())
v1_api.register(ProgramResource())
v1_api.register(LocalComputerResource())
v1_api.register(CommandResource())
v1_api.register(SignalResource())
v1_api.register(SettingResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^ruenoor/', simple_view, name='SimpleURL'),
    url(r'^data_api/', include([
        url(r'^signal/(?P<signal_id>\d+)/', signal_data, name='signal_data'),
    ])),
    url(r'^$', root_view, name='RootView')
]
