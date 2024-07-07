from pydantic import BaseModel

class CardSchema(BaseModel):
    # nome único: jose-do-egito
    slug: str
    # player id - card slug - secret
    in_game_id: str
    wisdom_cost: int
    attack_point: int
    defense_points: int
    
    used: bool
    has_passive_skill: bool
    has_active_skill: bool
    attachable: bool
    
    
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

