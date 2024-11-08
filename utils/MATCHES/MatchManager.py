from schemas.API_schemas import ClientRequestSchema
from utils.DataBaseManager import DB
from utils.MATCHES.MatchClass import C_Match
from utils.LoggerManager import Logger


class MatchManager:

    def __init__(self) -> None:
        self.MATCHES: list[C_Match] = []
        self.SPECTABLE_MATCHES: list[C_Match] = []

    def _getMatchById(self, match_id: str) -> C_Match:
        if match_id is not None:
            for match in self.MATCHES:
                if match.id == match_id:
                    return match
        return None

    def getStats(self):
        response = []
        for match in self.MATCHES:
            response.append(match.getStats())
        return {"matches": response}

    async def createMatch(self, match: C_Match):
        self.MATCHES.append(match)
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
        self.MATCHES.remove(match)
        Logger.info(msg=f'Partida encerrada: {match.id}', tag='MatchManager')
        Logger.status(msg=f'Partida encerrada: {match.getStats()}', tag='MatchManager')
        del match


MM = MatchManager()
