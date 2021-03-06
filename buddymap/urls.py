"""buddymap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^account/password/', include('accounts.passwords.urls', namespace='password')),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^api/account/', include('accounts.apis.urls', namespace='account')),
    url(r'^api/activity/', include('activities.apis.urls', namespace='activity')),
    url(r'^api/friend/', include('friends.apis.urls', namespace='api-friend')),
    url(r'^api/group/', include('groups.apis.urls', namespace='api-group')),
    url(r'^api/locator/', include('maplocators.apis.urls', namespace='api-locator')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
