import json


class DailyNutrient:
    """An  entry  in  the  database  for  storing  the  user’s  nutrient  intake  for  aspecific day"""
    user_id: str
    cal_consumed: int
    pro_consumed: int
    fat_consumed: int
    CHO_consumed: int
    cal_suggested: int
    pro_suggested: int
    fat_suggested: int
    CHO_suggested: int
    intake_date: str
    meal_taken: int

    def __init__(self, user_id: str = '', cal_consumed: int = 0, pro_consumed: int = 0, fat_consumed: int = 0,
                 CHO_consumed: int = 0, cal_suggested: int = 0, pro_suggested: int = 0, fat_suggested: int = 0, 
                 CHO_suggested: int = 0, intake_date: str = '', meal_taken: int = 0):
        self.user_id = user_id
        self.cal_consumed = cal_consumed
        self.pro_consumed = pro_consumed
        self.fat_consumed = fat_consumed
        self.CHO_consumed = CHO_consumed
        self.cal_suggested = cal_suggested
        self.pro_suggested = pro_suggested
        self.fat_suggested = fat_suggested
        self.CHO_suggested = CHO_suggested
        self.intake_date = intake_date
        self.meal_taken = meal_taken

    def get_sort_key(self) -> str:
        return f'{self.user_id}#{self.intake_date}'

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def fromJSON(self, json_obj) -> None:
        json_obj = json.loads(json_obj)
        self.user_id = json_obj.get('user_id')
        self.cal_consumed = json_obj.get('cal_consumed')
        self.pro_consumed = json_obj.get('pro_consumed')
        self.fat_consumed = json_obj.get('fat_consumed')
        self.CHO_consumed = json_obj.get('CHO_consumed')
        self.cal_suggested = json_obj.get('cal_suggested')
        self.pro_suggested = json_obj.get('pro_suggested')
        self.fat_suggested = json_obj.get('fat_suggested')
        self.CHO_suggested = json_obj.get('CHO_suggested')
        self.intake_date = json_obj.get('intake_date')
        self.meal_taken = json_obj.get('meal_taken')
