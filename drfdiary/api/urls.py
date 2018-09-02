from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
import rest_auth

from .views import CreateView, DetailsView, UserDetailsView, UserView


urlpatterns = {
    url(r'^accounts/', include('rest_auth.urls')),
    url(r'^accounts/registration/', include('rest_auth.registration.urls')),
    url(r'^entries/$', CreateView.as_view(), name="create"),
    url(r'^entries/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
    url(r'^get-token/$', obtain_auth_token),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^users/(?P<pk>[0-9]+)/$',
        UserDetailsView.as_view(), name="user_details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
