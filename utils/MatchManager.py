from schemas.API_schemas import ClientRequestSchema
from schemas.players_schema import PlayersInMatchSchema
from schemas.matches_schema import MatchSchema
from utils.ConnectionManager import WS


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

    def endMatch(self, match_id: str):
        match = self._getMatchById(match_id)
        self.MATCHES.remove(match)
        del match


MATCHES = MatchManager()
