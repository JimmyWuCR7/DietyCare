import json


class CustomizedIntake:
    """Dataclass for intake customization"""
    suggest_cal: str
    suggest_pro: int
    suggest_ch: int
    suggest_fat: int

    def __init__(self):
        self.suggest_cal = 0
        self.suggest_pro = 0
        self.suggest_ch = 0
        self.suggest_fat = 0

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
