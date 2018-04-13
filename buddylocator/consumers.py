from django.conf import settings

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .exceptions import ClientError
from .utils import get_group_or_error, get_locator_history #utility to the database
from urllib import parse
import json

# from buddymap.mixins import RestTokenConsumerMixin

class LocatorConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        if self.scope.get('user').is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
            print("Successfully Authenticate User: ",self.scope["user"])
        # Store which groups the user has joined on this connection

        self.groups = set()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        try:
            print(command)
            if command == "join":
                # Make them join the group
                print("join")
                await self.join_group(content["group"])
            elif command == "leave":
                # Leave the group
                print("leave")
                await self.leave_group(content["group"])
            elif command == "send":
                print("send")
                await self.send_group(content["group"], content["longitude"], content["latitude"])
            elif command == "history":
                print("get history")
                await self.get_history(content["group"])
        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the groups we are still in
        for group_id in list(self.groups):
            try:
                await self.leave_group(group_id)
            except ClientError:
                pass

    ##### Command helper methods called by receive_json

    async def join_group(self, group_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        group = await get_group_or_error(group_id, self.scope["user"])

        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_GROUPS:
            await self.channel_layer.group_send(
                group.group_name,
                {
                    "type": "locator.join",
                    "group_id": group_id,
                    "buddycode": self.scope["user"].buddycode,
                }
            )

        # Store that we're in the group
        self.groups.add(group_id)
        # Add them to the group so they get group messages
        await self.channel_layer.group_add(
            group.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the group
        await self.send_json({
            "join": str(group.id),
            "group": group.name,
        })

        #Save Message to database
        # await save_message_to_db(group, settings.LOC_TYPE_ENTER, "", self.scope["user"])


    async def leave_group(self, group_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        group = await get_group_or_error(group_id, self.scope["user"])

        #Save Message to database
        # await save_message_to_db(group, settings.LOC_TYPE_LEAVE, "", self.scope["user"])

        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_GROUPS:
            await self.channel_layer.group_send(
                group.group_name,
                {
                    "type": "locator.leave",
                    "group_id": group_id,
                    "buddycode": self.scope["user"].buddycode,
                }
            )
        # Remove that we're in the group
        self.groups.discard(group_id)
        # Remove them from the group so they no longer get group messages
        await self.channel_layer.group_discard(
            group.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the group
        await self.send_json({
            "leave": str(group.id),
        })

    async def send_group(self, group_id, longitude, latitude):
        """
        Called by receive_json when someone sends a message to a group.
        """
        # Check they are in this group
        if group_id not in self.groups:
            raise ClientError("group_ACCESS_DENIED")
        # Get the group and send to the group about it
        group = await get_group_or_error(group_id, self.scope["user"])

        await self.channel_layer.group_send(
            group.group_name,
            {
                "type": "locator.message",
                "group_id": group_id,
                "buddycode": self.scope["user"].buddycode,
                "longitude": longitude,
                "latitude": latitude
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so locator.join becomes locator_join
    async def locator_join(self, event):
        """
        Called when someone has joined our locator.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "LOC_type": settings.LOC_TYPE_ENTER,
                "group": event["group_id"],
                "buddycode": event["buddycode"],
            },
        )

    async def locator_leave(self, event):
        """
        Called when someone has left our locator.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "LOC_type": settings.LOC_TYPE_LEAVE,
                "group": event["group_id"],
                "buddycode": event["buddycode"],
            },
        )

    async def locator_message(self, event):
        """
        Called when someone has messaged our locator.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "LOC_type": settings.LOC_TYPE_MESSAGE,
                "group": event["group_id"],
                "buddycode": event["buddycode"],
                "longitude": event["longitude"],
                "latitude": event["latitude"],
            },
        )

    # async def global_notification(self, event):
    #     """
    #     Called when someone has messaged our locator.
    #     """
    #     # Send a message down to the client
    #     await self.send_json(
    #         {
    #             "LOC_type": settings.LOC_TYPE_GLOBAL,
    #             "group": event["group_id"],
    #             "buddycode": event["buddycode"],
    #             "message": event["message"],
    #         },
    #     )
