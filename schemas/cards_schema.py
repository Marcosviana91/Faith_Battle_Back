

class CardSchema:
    def __init__(self, in_game_id: str):
        self.in_game_id = in_game_id
        # nome único: jose-do-egito
        self.card_slug: str
        # player id - card slug - secret
        self.in_game_id: str
        # hero, artifacts, miracles, sins, legendary, wisdom
        self.card_wisdom_cost: int
        self.card_attack_points: int
        self.card_defense_points: int
        self.card_has_passive_skill: bool
        self.card_has_active_skill: bool
        self.card_attachable: bool

        self.ready: bool

    def __str__(self):
        return f'\n########\n{self.card_slug}: {self.in_game_id}\n{self.card_wisdom_cost}, {self.card_attack_points}, {self.card_defense_points}\n########\n'

    def passiveSkill(self):
        ...

    def activeSkill(self):
        ...

    def onAttach(self):
        ...

    def onDettach(self):
        ...

    def onDestroy(self):
        ...

    def onInvoke(self):
        ...

    def onAttack(self):
        ...

    def onDefense(self):
        ...

