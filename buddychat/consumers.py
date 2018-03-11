from django.conf import settings

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .exceptions import ClientError
from .utils import get_group_or_error, save_message_to_db, get_message_history #utility to the database
from urllib import parse
import json

# from buddymap.mixins import RestTokenConsumerMixin

class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        params = { key.decode(): val[0].decode() for key, val in parse.parse_qs(self.scope['query_string']).items() }
        print(params['token'])
        print(self.scope['user'])
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print("Message from client:",event.get('text'))
        self.send({
            "type": "websocket.send",
            "text": event.get("text"),
        })

class ChatConsumer(AsyncJsonWebsocketConsumer):
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
                await self.send_group(content["group"], content["message"])
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
                    "type": "chat.join",
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
        # await save_message_to_db(group, settings.MSG_TYPE_ENTER, "", self.scope["user"])



    async def leave_group(self, group_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        group = await get_group_or_error(group_id, self.scope["user"])

        #Save Message to database
        # await save_message_to_db(group, settings.MSG_TYPE_LEAVE, "", self.scope["user"])

        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_GROUPS:
            await self.channel_layer.group_send(
                group.group_name,
                {
                    "type": "chat.leave",
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

    async def send_group(self, group_id, message):
        """
        Called by receive_json when someone sends a message to a group.
        """
        # Check they are in this group
        if group_id not in self.groups:
            raise ClientError("group_ACCESS_DENIED")
        # Get the group and send to the group about it
        group = await get_group_or_error(group_id, self.scope["user"])
        #Save Message to database
        await save_message_to_db(group, settings.MSG_TYPE_MESSAGE, message, self.scope["user"])

        await self.channel_layer.group_send(
            group.group_name,
            {
                "type": "chat.message",
                "group_id": group_id,
                "user_id": self.scope["user"].id,
                "buddycode": self.scope["user"].buddycode,
                "first_name":self.scope["user"].firstName,
                "last_name":self.scope["user"].lastName,
                "message": message,
            }
        )

    async def get_history(self, group_id):
        group = await get_group_or_error(group_id, self.scope["user"])

        #send message history to client
        message_history = await get_message_history(group)
        for msg_hist in message_history:
            payload ={
                "msg_type": msg_hist.message_type,
                "group": group_id,
                "user_id": msg_hist.user.id,
                "buddycode": msg_hist.user.buddycode,
                "first_name":self.scope["user"].firstName,
                "last_name":self.scope["user"].lastName,
            }
            if(msg_hist.message_type==settings.MSG_TYPE_JOIN):
                payload["message"] = ''.join((msg_hist.user.buddycode,' joined the group'))
            elif(msg_hist.message_type==settings.MSG_TYPE_MESSAGE):
                payload["message"] = msg_hist.message
            await self.send_json(payload)

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "group": event["group_id"],
                "buddycode": event["buddycode"],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "group": event["group_id"],
                "buddycode": event["buddycode"],
            },
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "group": event["group_id"],
                "buddycode": event["buddycode"],
                "message": event["message"],
                "first_name":self.scope["user"].firstName,
                "last_name":self.scope["user"].lastName,
            },
        )

    # async def global_notification(self, event):
    #     """
    #     Called when someone has messaged our chat.
    #     """
    #     # Send a message down to the client
    #     await self.send_json(
    #         {
    #             "msg_type": settings.MSG_TYPE_GLOBAL,
    #             "group": event["group_id"],
    #             "buddycode": event["buddycode"],
    #             "message": event["message"],
    #         },
    #     )
