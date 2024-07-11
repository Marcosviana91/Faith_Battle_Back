from schemas.API_schemas import ClientRequestSchema
from schemas.players_schema import PlayersInMatchSchema
from schemas.matches_schema import MatchSchema
from utils.ConnectionManager import WS


class MatchManager:
    MATCHES: list[MatchSchema]

    def __init__(self) -> None:
        self.MATCHES = []

    def getStats(self):
        response = []
        for match in self.MATCHES:
            response.append(match.getMatchStats)
        return {"matches": response}

    def createMatch(self, match: MatchSchema):
        self.MATCHES.append(match)
        for match in self.MATCHES:
            print(match)


MATCHES = MatchManager()
