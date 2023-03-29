import boto3

from boto3.dynamodb.conditions import Key

from datatypes.DailyNutrient import DailyNutrient
from datatypes.DishTaken import DishTaken
from datatypes.User import User

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id='AKIAUJFI4YIETNXUBS6R',
                          aws_secret_access_key='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')
intake_table = dynamodb.Table('DietyCare-DailyIntake')
user_table = dynamodb.Table('DietyCare-Users')

DAILY_NUTRIENT_PK = 'DailyNutrient'
DISH_TAKEN_PK = 'DishTaken'
USER_PK = 'User'


def put_daily_nutrient(daily_nutrient: DailyNutrient) -> None:
    intake_table.put_item(
        Item={
            'Type': DAILY_NUTRIENT_PK
            ,
            'Id': daily_nutrient.get_sort_key(),
            'Body': daily_nutrient.toJSON()
        }
    )


def get_daily_nutrient(sort_key: str) -> str:
    daily_nut_response = intake_table.get_item(
        Key={
            'Type': DAILY_NUTRIENT_PK,
            'Id': sort_key
        }
    )
    return daily_nut_response


def put_dish_taken(dish_taken: DishTaken) -> None:
    intake_table.put_item(
        Item={
            'Type': DISH_TAKEN_PK,
            'Id': dish_taken.get_sort_key(),
            'Body': dish_taken.toJSON()
        }
    )


def get_dish_taken(dish_taken: DishTaken) -> str:
    get_response = intake_table.get_item(
        Key={
            'Type': DISH_TAKEN_PK,
            'Id': dish_taken.get_sort_key()
        }
    )
    return get_response


def delete_dish_taken(dish_taken: DishTaken) -> None:
    delete_response = intake_table.delete_item(
        Key={
            'Type': DISH_TAKEN_PK,
            'Id': dish_taken.get_sort_key()
        }
    )
    return delete_response


def list_dish_taken_by_date(dish_taken: DishTaken) -> None:
    list_response = intake_table.query(
        KeyConditionExpression=Key('Type').eq(DISH_TAKEN_PK) & Key('Id').begins_with(dish_taken.get_sort_key_for_daily_nutrient())
    )
    return list_response['Items']


def put_user(user: User) -> None:
    user_table.put_item(
        Item={
            'Type': USER_PK,
            'Id': user.get_sort_key(),
            'Body': user.toJSON()
        }
    )


def get_user(user: User) -> str:
    user_response = user_table.get_item(
        Key={
            'Type': USER_PK,
            'Id': user.get_sort_key()
        }
    )
    return user_response


def delete_user(user: User) -> None:
    user_response = user_table.delete_item(
        Key={
            'Type': USER_PK,
            'Id': user.get_sort_key()
        }
    )
    return user_response
