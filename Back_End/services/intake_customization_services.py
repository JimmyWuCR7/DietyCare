import math

from datatypes.CustomizedIntake import CustomizedIntake


def suggest_for_weight_goals(age: int, gender: str, height: float, weight: float, target_weight: float,
                             body_fat: float) -> CustomizedIntake:
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
    customized_intake = CustomizedIntake()
    BMR = 0
    if gender[0].upper() == 'M':
        BMR_Mifflin_StJeor = 10 * weight + 6.25 * height - 5 * age + 5
        BMR_RevisedHarris_Benedict = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
        BMR_Katch_McArdle = 370 + 21.6 * (1 - body_fat) * weight
        BMR = 1 / 3 * (BMR_Mifflin_StJeor + BMR_RevisedHarris_Benedict + BMR_Katch_McArdle)
    elif gender[0].upper() == 'F':
        BMR_Mifflin_StJeor = 10 * weight + 6.25 * height - 5 * age - 161
        BMR_RevisedHarris_Benedict = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593
        BMR_Katch_McArdle = 370 + 21.6 * (1 - body_fat) * weight
        BMR = 1 / 3 * (BMR_Mifflin_StJeor + BMR_RevisedHarris_Benedict + BMR_Katch_McArdle)
    cal = BMR * 1.2
    if target_weight == weight:
        customized_intake.suggest_cal = math.ceil(cal)
    elif target_weight < weight:
        customized_intake.suggest_cal = math.ceil(cal * 0.8)
    elif target_weight > weight:
        customized_intake.suggest_cal = math.ceil(cal * 1.2)
    customized_intake.suggest_pro = customized_intake.suggest_cal * 0.2 / 4
    customized_intake.suggest_ch = customized_intake.suggest_cal * 0.5 / 4
    customized_intake.suggest_fat = customized_intake.suggest_cal * 0.3 / 9
    return customized_intake


def suggest_for_muscle_goals(age: int, gender: str, height: float, weight: float, exercise_level: int, body_fat: float,
                             body_type: str) -> CustomizedIntake:
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
    customized_intake = CustomizedIntake()
    BMR = 0
    if gender[0].upper() == 'M':
        BMR_Mifflin_StJeor = 10 * weight + 6.25 * height - 5 * age + 5
        BMR_RevisedHarris_Benedict = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
        BMR_Katch_McArdle = 370 + 21.6 * (1 - body_fat) * weight
        BMR = 1 / 3 * (BMR_Mifflin_StJeor + BMR_RevisedHarris_Benedict + BMR_Katch_McArdle)
    elif gender[0].upper() == 'F':
        BMR_Mifflin_StJeor = 10 * weight + 6.25 * height - 5 * age - 161
        BMR_RevisedHarris_Benedict = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593
        BMR_Katch_McArdle = 370 + 21.6 * (1 - body_fat) * weight
        BMR = 1 / 3 * (BMR_Mifflin_StJeor + BMR_RevisedHarris_Benedict + BMR_Katch_McArdle)

    def TDEEGet(exercise_level, BMR):
        return {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}[exercise_level] * BMR

    TDEE = TDEEGet(exercise_level, BMR)
    customized_intake.suggest_cal = math.ceil(TDEE * 1.15)

    def ratioGet(body_type):
        return {'endomorph': [0.25, 0.4, 0.35], 'ectomorph': [0.4, 0.3, 0.4], 'mesomorph': [0.4, 0.35, 0.25]}[body_type]

    listRatio = ratioGet(body_type)
    customized_intake.suggest_ch = listRatio[0] * customized_intake.suggest_cal / 4
    customized_intake.suggest_pro = listRatio[1] * customized_intake.suggest_cal / 4
    customized_intake.suggest_fat = listRatio[2] * customized_intake.suggest_cal / 9
    return customized_intake