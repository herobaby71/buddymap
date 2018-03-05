from django.conf.urls import url

from .views import CreateGroupAPIView, RemoveGroupAPIView, AddUserToGroupAPIView, RemoveUserFromGroupAPIView, GetGroupsFromUserAPIView, GetUsersInGroup

app_name="groups"
urlpatterns = [
    url(r'^create/$', CreateGroupAPIView.as_view(), name='create'),
    url(r'^remove/$', RemoveGroupAPIView.as_view(), name='remove'),
    url(r'^adduser/$', AddUserToGroupAPIView.as_view(), name='adduser'),
    url(r'^removeuser/$', RemoveUserFromGroupAPIView.as_view(), name='removeuser'),
    url(r'^getgroups/$', GetGroupsFromUserAPIView.as_view(), name='adduser'),
    url(r'^getusers/$', GetUsersInGroup.as_view(), name='removeuser'),

]
