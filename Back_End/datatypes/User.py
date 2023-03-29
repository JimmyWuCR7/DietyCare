import json


class User:
    """An  entry  in  the  database  for  storing  the  user"""
    user_id: str
    gender: str
    age: int
    height: float
    weight: float
    target_weight: float
    body_fat: float
    body_type: str
    exercise_level: int
    allergens: list
    diet_goal: str
    is_vegetarian: bool
    b_day: int
    b_month: int
    b_year: int
    registration_date: str

    def __init__(self, user_id: str = '', gender: str = '', age: int = 0, height: float = 0,
                 weight: float = 0, target_weight: float = 0, body_fat: float = 0, body_type: str = '',
                 exercise_level: int = 0, allergens: list = [], diet_goal: str = '', is_vegetarian: bool = False,
                 b_day: int = 0, b_month: int = 0, b_year: int = 0, registration_date: str = ''):
        self.user_id = user_id
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.target_weight = target_weight
        self.body_fat = body_fat
        self.body_type = body_type
        self.exercise_level = exercise_level
        self.allergens = allergens
        self.diet_goal = diet_goal
        self.is_vegetarian = is_vegetarian
        self.b_day = b_day
        self.b_month = b_month
        self.b_year = b_year
        self.registration_date = registration_date

    def get_sort_key(self) -> str:
        return f'{self.user_id}'

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def fromJSON(self, json_obj) -> None:
        json_obj = json.loads(json_obj)
        self.user_id = json_obj.get('user_id')
        self.gender = json_obj.get('gender')
        self.age = int(json_obj.get('age'))
        self.height = float(json_obj.get('height'))
        self.weight = float(json_obj.get('weight'))
        self.target_weight = float(json_obj.get('target_weight'))
        self.body_fat = float(json_obj.get('body_fat'))
        self.body_type = json_obj.get('body_type')
        self.exercise_level = int(json_obj.get('exercise_level'))
        self.allergens = json_obj.get('allergens')
        self.diet_goal = json_obj.get('diet_goal')
        self.is_vegetarian = json_obj.get('is_vegetarian')
        self.b_day = int(json_obj.get('b_day'))
        self.b_month = int(json_obj.get('b_month'))
        self.b_year = int(json_obj.get('b_year'))
        self.registration_date = json_obj.get('registration_date')
