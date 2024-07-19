from pydantic import BaseModel, ConfigDict

class CardSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # nome único: jose-do-egito
    slug: str | None
    wisdom_cost: int | None = None
    attack_point: int | None = None
    defense_points: int | None = None
    # player id - card slug - secret
    in_game_id: str | None = None
    status: str | None = "ready" #"ready" | "used" | "not-enough" 
    
    # card_type: int
    
    # used: bool
    # has_passive_skill: bool
    # has_active_skill: bool
    # attachable: bool
    
    @property
    def getCardStats(self):
        return {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "wisdom_cost": self.wisdom_cost,
            "attack_point": self.attack_point,
            "defense_points": self.defense_points,
            "status": self.status,
        }
    
    
    def passiveSkill(self):
        ...

    def activeSkill(self):
        ...

    def onAttach(self):
        ...

    def onDettach(self):
        ...

    def onInvoke(self):
        ...

    def onDestroy(self):
        ...

    def onAttack(self):
        ...

    def onDefense(self):
        ...

