from schemas import ClientRequestSchema, MatchSchema, PlayersInMatchSchema
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
