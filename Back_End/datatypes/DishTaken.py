import json


class DishTaken:
    """An  entry  in  the  database  for storing the user’s taken dish"""
    user_id: str
    food_name: str
    food_intake_amount: int
    intake_date: str
    meal_type: str
    nth_dish_of_meal: int
    cal_consumed: int
    pro_consumed: int
    fat_consumed: int
    CHO_consumed: int

    def __init__(self, user_id: str = '', food_name: str = '', food_intake_amount: int = 0, intake_date: str = '',
                 meal_type: str = 0, nth_dish_of_meal: int = 0, cal_consumed: int = 0, pro_consumed: int = 0,
                 fat_consumed: int = 0, CHO_consumed: int = 0, ):
        self.user_id = user_id
        self.food_name = food_name
        self.food_intake_amount = food_intake_amount
        self.intake_date = intake_date
        self.meal_type = meal_type
        self.nth_dish_of_meal = nth_dish_of_meal
        self.cal_consumed = cal_consumed
        self.pro_consumed = pro_consumed
        self.fat_consumed = fat_consumed
        self.CHO_consumed = CHO_consumed

    def get_sort_key(self) -> str:
        return f'{self.user_id}#{self.intake_date}#{self.meal_type}#{self.food_name}'

    def get_sort_key_for_daily_nutrient(self) -> str:
        return f'{self.user_id}#{self.intake_date}'

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def fromJSON(self, json_obj) -> None:
        json_obj = json.loads(json_obj)
        self.user_id = json_obj.get('user_id')
        self.food_name = json_obj.get('user_id')
        self.food_intake_amount = json_obj.get('user_id')
        self.intake_date = json_obj.get('user_id')
        self.meal_type = json_obj.get('meal_type')
        self.nth_dish_of_meal = json_obj.get('nth_dish_of_meal')
        self.cal_consumed = json_obj.get('cal_consumed')
        self.pro_consumed = json_obj.get('pro_consumed')
        self.fat_consumed = json_obj.get('fat_consumed')
        self.CHO_consumed = json_obj.get('CHO_consumed')
