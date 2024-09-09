from schemas.API_schemas import ClientRequestSchema
from utils.DataBaseManager import DB
from utils.MATCHES.MatchClass import C_Match


class MatchManager:

    def __init__(self) -> None:
        self.MATCHES: list[C_Match] = []
        self.SPECTABLE_MATCHES: list[C_Match] = []

    def _getMatchById(self, match_id: str) -> C_Match:
        for match in self.MATCHES:
            if match.id == match_id:
                return match

    def getStats(self):
        response = []
        for match in self.MATCHES:
            response.append(match.getStats())
        return {"matches": response}

    async def createMatch(self, match: C_Match):
        self.MATCHES.append(match)
        for _team in match.players_in_match:
            for player in _team:
                await DB.setPlayerRoomOrMatch(player_id=player.id, match_id=match.id)
        await match.newRoundHandle()
        await match.updatePlayers()

    async def handleMove(self, data_raw: dict):
        data = ClientRequestSchema(**data_raw)
        if data.data_type == "match_move":
            match_room = self._getMatchById(data.match_move.get("match_id"))
            if (match_room):
                await match_room.incoming(data.match_move)
            if (match_room.checkWinner()):
                await self.endMatch(match_room)
                return
            await match_room.updatePlayers()

    async def endMatch(self, match: C_Match):
        await match.finishMatch()
        await match.updatePlayers()
        for _team in match.players_in_match:
            for player in _team:
                await DB.setPlayerRoomOrMatch(player_id=player.id, clear=True)
        self.MATCHES.remove(match)
        del match


MM = MatchManager()
