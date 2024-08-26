# Cria uma partida fake com o usuário p0 (id: 1) e p9 (id: 10),
# para testar a reconexão.

from schemas.players_schema import PlayersSchema
from schemas.rooms_schema import RoomSchema
from utils.ROOM.RoomManager import ROOMS


async def createFakeMatch():
    STANDARD_CARDS = [
    {"slug":'abraao'},
    {"slug":'adao'},
    {"slug":'daniel'},
    {"slug":'davi'},
    {"slug":'elias'},
    {"slug":'ester'},
    {"slug":'eva'},
    {"slug":'jaco'},
    {"slug":"jose-do-egito"},
    {"slug":"josue"},
    {"slug":"maria"},
    {"slug":"moises"},
    {"slug":"noe"},
    {"slug":"salomao"},
    {"slug":"sansao"},
]

    p0 = PlayersSchema(id=1, available_cards=STANDARD_CARDS)
    p9 = PlayersSchema(id=10, available_cards=STANDARD_CARDS)
    fake_room = RoomSchema(id="fake_match", name="sala fake", created_by=p0)

    ROOMS.createRoom(fake_room)
    await ROOMS.enterRoom(room_id=fake_room.id, player=p9, password="")
    p9.ready = True
    fake_room.setReady(p0.id)

    p9.ready = True
    await ROOMS.handleRoom({
        "data_type": "ready",
        "room_data": {
            "id": fake_room.id,
            },
        "user_data": {
            "id": p0.id,
        }
    })
