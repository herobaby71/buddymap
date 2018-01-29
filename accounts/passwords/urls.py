from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns  = [
        url(r'^change/$',
                auth_views.PasswordChangeView.as_view(),
                name='password_change'),
        url(r'^change/done/$',
                auth_views.PasswordChangeDoneView.as_view(),
                name='password_change_done'),
        url(r'^reset/$',
                auth_views.PasswordResetView.as_view(),
                name='password_reset'),
        url(r'^reset/done/$',
                auth_views.PasswordResetDoneView.as_view(),
                name='password_reset_done'),
        url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                auth_views.PasswordResetConfirmView.as_view(),
                name='password_reset_confirm'),
        url(r'^reset/complete/$',
                auth_views.PasswordResetCompleteView.as_view(),
                name='password_reset_complete'),
]
