from django.conf.urls import url

from .views import UserLoginAPIView, UserCreateAPIView, verifyCredentialsAPIView, getUserInfoAPIView, ChangeUserStatusAPIView

urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^verify/$', verifyCredentialsAPIView.as_view(), name='verify'),
    url(r'^info/$', getUserInfoAPIView.as_view(), name='info'),
    url(r'^change-status/$', ChangeUserStatusAPIView.as_view(), name='status'),

]
