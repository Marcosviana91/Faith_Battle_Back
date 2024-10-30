class Notification():
    def __init__(
        self,
        message: str,
        title: str | None = None,
        player_trigger_id: int | None = None,
        card_trigger_id: str | None = None,
        move_type: str | None = None,
        player_target_id: int | None = None,
        card_target_id: str | None = None,
        stillUntilDismiss: bool = False,
    ):
        self.message = message
        self.title = title
        self.player_trigger_id = player_trigger_id
        self.card_trigger_id = card_trigger_id
        self.move_type = move_type
        self.player_target_id = player_target_id
        self.card_target_id = card_target_id
        self.stillUntilDismiss = stillUntilDismiss

    def getData(self):
        _data = {
            'message': self.message,
        }
        if self.title:
            _data.update({'title': self.title})
        if self.player_trigger_id:
            _data.update({'player_trigger_id': self.player_trigger_id})
        if self.card_trigger_id:
            _data.update({'card_trigger_id': self.card_trigger_id})
        if self.move_type:
            _data.update({'move_type': self.move_type})
        if self.player_target_id:
            _data.update({'player_target_id': self.player_target_id})
        if self.card_target_id:
            _data.update({'card_target_id': self.card_target_id})
        if self.stillUntilDismiss:
            _data.update({'stillUntilDismiss': self.stillUntilDismiss})
        return {
            'data_type': 'notification',
            'notification': _data,
        }
