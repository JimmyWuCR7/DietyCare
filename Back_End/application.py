import json

from flask import Flask, request, jsonify, Response

from services import intake_tracking_services, meal_recommendation_services, intake_customization_services, user_services

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/dailyNutrient', methods=['PUT'])
def daily_nut_init() -> str:
    """Inits a new DailyNutrient entry in DB
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    dict: The dict of the new dish intake record.
    """
    new_daily_nutrient = intake_tracking_services.add_new_daily_nutrient(user_id=request.args.get('user_id'),
                                                         cal_suggested=float(request.args.get('target_cal')),
                                                         pro_suggested=float(request.args.get('target_pro')),
                                                         fat_suggested=float(request.args.get('target_fat')),
                                                         CHO_suggested=float(request.args.get('target_CHO')),
                                                         intake_date=request.args.get('intake_date'))

    return new_daily_nutrient.toJSON()


@application.route('/dishIntake', methods=['PUT'])
def put_dish_taken() -> str:
    """Record a dish taken
    Parameters:
    user_id (str): The user id.
    food_name (str): The food's name.
    food_intake_amount (int): The amount of food.
    intake_date (str): The intake date.
    meal_type (str): The meal type. Breakfast? Lunch?.
    cal_consumed (int): The calories consumed.
    pro_consumed (int): The proteins consumed.
    fat_consumed (int): The fat consumed.
    CHO_consumed (int): The CHO consumed.
    Returns:
    dict: The dict of the new dish intake record.
    """
    new_dish_intake = intake_tracking_services.add_new_dish_taken(user_id=request.args.get('user_id'),
                                                  food_name=request.args.get('food_name'),
                                                  food_intake_amount=float(request.args.get('food_intake_amount')),
                                                  intake_date=request.args.get('intake_date'),
                                                  meal_type=request.args.get('meal_type'),
                                                  nth_dish_of_meal=int(request.args.get('nth_dish_of_meal')),
                                                  cal_consumed=float(request.args.get('cal_consumed')),
                                                  pro_consumed=float(request.args.get('pro_consumed')),
                                                  fat_consumed=float(request.args.get('fat_consumed')),
                                                  CHO_consumed=float(request.args.get('CHO_consumed')))
    return new_dish_intake.toJSON()


@application.route('/dishIntake', methods=['DELETE'])
def delete_dish_taken() -> str:
    """Exports the user's dish intake
    Parameters:
    user_id (str): The user id.
    intake_date (str): The date for the user.
    meal_type (int): The meal type.
    Returns:
    dict: The dict of daily intake of the current day.
    """
    return jsonify(intake_tracking_services.delete_dish_taken(user_id=request.args.get('user_id'),
                                                    intake_date=request.args.get('intake_date'), 
                                                    meal_type=request.args.get('meal_type'),
                                                    food_name=request.args.get('food_name')))


@application.route('/dailyNutrient', methods=['GET'])
def get_daily_nutrient() -> str:
    """Gets the user's daily intake
    Parameters:
    user_id (str): The user id.
    intake_date (str): The date for the user.
    Returns:
    dict: The dict of daily intake of the current day.
    """
    return intake_tracking_services.get_daily_nutrient(user_id=request.args.get('user_id'),
                                                        intake_date=request.args.get('intake_date'))


@application.route('/dishIntake', methods=['GET'])
def get_dish_taken() -> str:
    """Gets the user's dish intake
    Parameters:
    user_id (str): The user id.
    intake_date (str): The date for the user.
    meal_type (int): The meal type.
    Returns:
    dict: The dict of daily intake of the current day.
    """
    return intake_tracking_services.get_dish_taken(user_id=request.args.get('user_id'),
                                                    intake_date=request.args.get('intake_date'), 
                                                    meal_type=request.args.get('meal_type'),
                                                    food_name=request.args.get('food_name'))


@application.route('/dishIntakeList', methods=['GET'])
def list_dish_taken() -> str:
    """Gets the user's dish intake
    Parameters:
    user_id (str): The user id.
    intake_date (str): The date for the user.
    meal_type (int): The meal type.
    Returns:
    dict: The dict of daily intake of the current day.
    """
    list_result = intake_tracking_services.list_dish_taken_by_date(user_id=request.args.get('user_id'),
                                                    intake_date=request.args.get('intake_date'))
    return jsonify([json.loads(r) for r in list_result])


@application.route('/logGeneration', methods=['GET'])
def log_generation() -> Response:
    """Generates necessary information for plotting.
    Parameters:
    start_date (str): The start date. It should be the format: 'yyyy-mm-dd'.
    end_date (str): The end date. It should be the format: 'yyyy-mm-dd'.
    user_id (str): The user id.
    Returns:
    list[dict]: The necessary information for plotting.
    """
    result = intake_tracking_services.get_daily_nutrient_within_dates(user_id=request.args.get('user_id'),
                                                      start_date=request.args.get('start_date'),
                                                      end_date=request.args.get('end_date'))

    return jsonify(result)


@application.route('/weightIntakeCustomization', methods=['GET'])
def weight_intake_customization() -> str:
    """Suggests intake combinations for weight goals
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    dict: The dict of the new dish intake record.
    """
    # TODO update pydoc
    customized_intake = intake_customization_services.suggest_for_weight_goals(age=int(request.args.get('age')),
                                                          gender=request.args.get('gender'),
                                                          height=float(request.args.get('height')),
                                                          weight=float(request.args.get('weight')),
                                                          target_weight=float(request.args.get('target_weight')),
                                                          body_fat=float(request.args.get('body_fat')))

    return customized_intake.toJSON()


@application.route('/muscleIntakeCustomization', methods=['GET'])
def muscle_intake_customization() -> str:
    """Suggests intake combinations for weight goals
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    dict: The dict of the new dish intake record.
    """
    # TODO update pydoc
    customized_intake = intake_customization_services.suggest_for_muscle_goals(age=int(request.args.get('age')),
                                                          gender=request.args.get('gender'),
                                                          height=float(request.args.get('height')),
                                                          weight=float(request.args.get('weight')),
                                                          exercise_level=int(request.args.get('exercise_level')),
                                                          body_fat=float(request.args.get('body_fat')),
                                                          body_type=request.args.get('body_type'))

    return customized_intake.toJSON()


@application.route('/mealRecommendation', methods=['GET'])
def meal_recommendation() -> Response:
    """Suggests intake combinations for weight goals
    Parameters:
    user_id (str): The user id.
    target_cal (int): The target calories for the day
    target_fat (int): The target fat for the day
    target_pro (int): The target protein for the day
    target_CHO (int): The target CHO for the day
    intake_date (str): The intake date.
    Returns:
    dict: The dict of the new dish intake record.
    """
    # TODO update pydoc
    recommended_meal = meal_recommendation_services.make_recommendation(calories=int(request.args.get('calories')))

    return jsonify(recommended_meal)


@application.route('/user', methods=['PUT'])
def put_user() -> str:
    """Puts a user into DB
    Parameters:
    user (dict): A serialized user in request body.
    Returns:
    dict: The dict of the new user record.
    """
    new_user = user_services.put_user(user=json.dumps(request.json))

    return new_user.toJSON()


@application.route('/user', methods=['GET'])
def get_user() -> str:
    """Gets a user from DB
    Parameters:
    user_id (str): Id of the user to get.
    Returns:
    dict: The dict of the user record.
    """
    return user_services.get_user(user_id=request.args.get('user_id'))


@application.route('/user', methods=['DELETE'])
def delete_user() -> str:
    """Deletes a user in DB
    Parameters:
    user_id (str): Id of the user to delete.
    Returns:
    dict: The dict of the new user record.
    """
    deletion_response = user_services.delete_user(user_id=request.args.get('user_id'))
    return jsonify(deletion_response)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True

    # public host
    #application.run(ssl_context='adhoc', host='0.0.0.0')

    # localhost
    application.run()
