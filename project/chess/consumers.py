import json
from asyncio import events
from re import L

from channels.generic.websocket import (AsyncJsonWebsocketConsumer,
                                        AsyncWebsocketConsumer)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class ChessConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "game_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        to = text_data_json["to"]
        ffrom = text_data_json["from"]
        fen = text_data_json["fen"]
        pgn = text_data_json["pgn"]
        username = text_data_json["username"]
        pk = text_data_json["pk"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message,
                                   "to": to, "from": ffrom, "fen": fen, "pgn": pgn, "username": username, "pk": pk}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        to = event["to"]
        ffrom = event["from"]
        fen = event["fen"]
        pgn = event["pgn"]
        username = event["username"]
        pk = event["pk"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "to": to, "from": ffrom, "fen": fen, "pgn": pgn, "username": username, "pk": pk}))


# dopisz tutaj pk, jak masz pk to wtedy niech wysyla username i pk, w skrypcie zapisz se pk i username zeby sprawdzac czy sie nie zmienily,
# jak sie zakonczy gra to wpisuj pk do skryptu
