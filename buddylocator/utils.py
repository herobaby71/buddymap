from channels.db import database_sync_to_async
from .exceptions import ClientError
from groups.models import Group, Membership
from maplocators.models import Locator

# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_group_or_error(group_id, user):
    """
        Tries to fetch a group for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the group they requested (by ID)
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        raise ClientError("group_INVALID")
    # Check permissions (whether the user belongs to the group or not)
    # try:
    #     member_valid= Membership.objects.filter(group=group, user=user)
    # except Membership.DoesNotExist:
    #     raise ClientError("group_ACCESS_DENIED")
    members = list(Membership.objects.filter(group=group))
    members = [item.user for item in members]
    if user not in members:
        raise ClientError("group_ACCESS_DENIED")
    return group

@database_sync_to_async
def save_locator_to_db(longitude, latitude, user):
    """
        Save user message to corresponding group
    """
    loc_obj = Locator.objects.create_locator(user, longitude, latitude)
    loc_obj.save()
    return message

@database_sync_to_async
def get_locator_history(group):
    """
        Get Message history for the specify group
    """
    try:
        messages = BuddyMessage.objects.filter(group=group).order_by('created')
    except BuddyMessage.DoesNotExist:
        messages = [""]
    return messages




#
