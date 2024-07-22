from schemas.API_schemas import ClientRequestSchema
from schemas.matches_schema import MatchSchema


class MatchManager:
    MATCHES: list[MatchSchema]

    def __init__(self) -> None:
        self.MATCHES = []

    def _getMatchById(self, match_id: str) -> MatchSchema:
        for match in self.MATCHES:
            if match.id == match_id:
                return match
        return None

    @property
    def getStats(self):
        response = []
        for match in self.MATCHES:
            response.append(match.getMatchStats)
        return {"matches": response}

    def createMatch(self, match: MatchSchema):
        self.MATCHES.append(match)
        
    async def handleMove(self, data_raw: dict):
        data = ClientRequestSchema(**data_raw)
        # print('>>>>> RECV: ', data)
        if data.data_type == "match_move":
            match_room = self._getMatchById(data.match_move.get("match_id"))
            if (match_room):
                await match_room.incoming(data.match_move)


    def endMatch(self, match_id: str):
        match = self._getMatchById(match_id)
        self.MATCHES.remove(match)
        del match


MATCHES = MatchManager()
