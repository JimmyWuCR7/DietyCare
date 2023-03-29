import db

from datetime import datetime, timedelta

from datatypes.DailyNutrient import DailyNutrient
from datatypes.DishTaken import DishTaken
from datatypes.User import User
from services import intake_customization_services
from services import user_services

DEFAULT_CAL_SUGGESTED = 500
DEFAULT_PRO_SUGGESTED = 500
DEFAULT_FAT_SUGGESTED = 500
DEFAULT_CHO_SUGGESTED = 500
BUILD_MUSCLE = 'Build Muscle'
LOSE_WEIGHT = 'Lose Weight'
# TODO update pydoc

def add_new_daily_nutrient(user_id: str, cal_suggested: int, pro_suggested: int, fat_suggested: int, CHO_suggested: int,
                           intake_date: str) -> DailyNutrient:
    """Exports the user's daily intake
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    DailyNutrient: The new dish intake record object.
    """
    daily_nutrient = DailyNutrient(user_id=user_id, cal_suggested=cal_suggested, pro_suggested=pro_suggested, fat_suggested=fat_suggested,
                                   CHO_suggested=CHO_suggested, intake_date=intake_date)
    db.put_daily_nutrient(daily_nutrient)
    return daily_nutrient


def add_new_dish_taken(user_id: str, food_name: str, food_intake_amount: int, intake_date: str,
                       meal_type: str, nth_dish_of_meal: int, cal_consumed: int, pro_consumed: int,
                       fat_consumed: int, CHO_consumed: int) -> DishTaken:
    """Exports the user's daily intake
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    DailyNutrient: The new dish intake record object.
    """
    new_dish_intake = DishTaken(user_id=user_id,
                                food_name=food_name,
                                food_intake_amount=food_intake_amount,
                                intake_date=intake_date,
                                meal_type=meal_type,
                                nth_dish_of_meal=nth_dish_of_meal,
                                cal_consumed=cal_consumed,
                                pro_consumed=pro_consumed,
                                fat_consumed=fat_consumed,
                                CHO_consumed=CHO_consumed)

    daily_nut_response = get_daily_nutrient(user_id=user_id, intake_date=intake_date)
    daily_nut_to_update = DailyNutrient()
    daily_nut_to_update.fromJSON(daily_nut_response)
    # Null Check, add daily_nutrient if DNE
    if not daily_nut_to_update.user_id:
        current_user = User()
        current_user.fromJSON(user_services.get_user(user_id=user_id))
        if current_user.diet_goal == BUILD_MUSCLE:
            customized_intake = intake_customization_services.suggest_for_muscle_goals(age=current_user.age, gender=current_user.gender, height=current_user.height, weight=current_user.weight, exercise_level=current_user.exercise_level, body_fat=current_user.body_fat, body_type=current_user.body_type.lower())
        else:
            customized_intake = intake_customization_services.suggest_for_weight_goals(age=current_user.age, gender=current_user.gender, height=current_user.height, weight=current_user.weight, target_weight=current_user.target_weight, body_fat=current_user.body_fat)
        add_new_daily_nutrient(user_id=user_id, cal_suggested=customized_intake.suggest_cal, pro_suggested=customized_intake.suggest_pro, fat_suggested=customized_intake.suggest_fat, CHO_suggested=customized_intake.suggest_ch, intake_date=intake_date)
    daily_nut_response = get_daily_nutrient(user_id=user_id, intake_date=intake_date)
    daily_nut_to_update = DailyNutrient()
    daily_nut_to_update.fromJSON(daily_nut_response)
    daily_nut_to_update.cal_consumed = daily_nut_to_update.cal_consumed + new_dish_intake.cal_consumed
    daily_nut_to_update.pro_consumed = daily_nut_to_update.pro_consumed + new_dish_intake.pro_consumed
    daily_nut_to_update.fat_consumed = daily_nut_to_update.fat_consumed + new_dish_intake.fat_consumed
    daily_nut_to_update.CHO_consumed = daily_nut_to_update.CHO_consumed + new_dish_intake.CHO_consumed
    daily_nut_to_update.meal_taken = daily_nut_to_update.meal_taken + 1

    db.put_daily_nutrient(daily_nut_to_update)
    db.put_dish_taken(new_dish_intake)

    return new_dish_intake


def get_daily_nutrient(user_id: str, intake_date: str) -> str:
    """Exports the user's daily intake
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    DailyNutrient: The new dish intake record object.
    """
    date_obj = datetime.strptime(intake_date, "%Y-%m-%d")
    intake_date = f'{date_obj.year}-{date_obj.month}-{date_obj.day}'
    daily_nutrient = DailyNutrient(user_id=user_id, intake_date=intake_date)
    get_response = db.get_daily_nutrient(daily_nutrient.get_sort_key())
    return get_response.get('Item').get('Body') if get_response.get('Item') else DailyNutrient().toJSON()


def get_dish_taken(user_id: str, intake_date: str, meal_type: str, food_name: str) -> str:
    """Puts a user into DB
    Parameters:
    user (str): The user id.
    Returns:
    User: The constructed User object
    """
    date_obj = datetime.strptime(intake_date, "%Y-%m-%d")
    intake_date = f'{date_obj.year}-{date_obj.month}-{date_obj.day}'
    dish_taken = DishTaken(user_id=user_id, intake_date=intake_date, meal_type=meal_type, food_name=food_name)
    get_response = db.get_dish_taken(dish_taken)
    return get_response.get('Item').get('Body') if get_response.get('Item') else DishTaken().toJSON()


def list_dish_taken_by_date(user_id: str, intake_date: str) -> list:
    """Puts a user into DB
    Parameters:
    user (str): The user id.
    Returns:
    User: The constructed User object
    """
    date_obj = datetime.strptime(intake_date, "%Y-%m-%d")
    intake_date = f'{date_obj.year}-{date_obj.month}-{date_obj.day}'
    dish_taken = DishTaken(user_id=user_id, intake_date=intake_date)
    get_response = db.list_dish_taken_by_date(dish_taken)
    return [d.get('Body') for d in get_response]


def delete_dish_taken(user_id: str, intake_date: str, meal_type: str, food_name: str) -> str:
    """Puts a user into DB
    Parameters:
    user (str): The user id.
    Returns:
    User: The constructed User object
    """
    dish_taken = DishTaken(user_id=user_id, intake_date=intake_date, meal_type=meal_type, food_name=food_name)
    return db.delete_dish_taken(dish_taken).get('ResponseMetadata').get('HTTPStatusCode') == 200


def get_daily_nutrient_within_dates(user_id: str, start_date: str, end_date: str) -> list:
    """Exports the user's daily intake
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    DailyNutrient: The new dish intake record object.
    """
    date_list = __generate_date_list(start_date, end_date)
    result = []
    for date in date_list:
        daily_nutrient = get_daily_nutrient(user_id=user_id, intake_date=date)
        result.append(daily_nutrient)
    return result



def __generate_date_list(start_date: str, end_date: str) -> list:
    date_list = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while start_date <= end_date:
        date = f'{start_date.year}-{start_date.month}-{start_date.day}'
        date_list.append(date)
        start_date += timedelta(days=1)
    return date_list
