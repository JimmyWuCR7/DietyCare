import db

from datetime import date

from datatypes.User import User


def put_user(user: str) -> User:
    """Puts a user into DB
    Parameters:
    user (str): The user id.
    Returns:
    User: The constructed User object
    """
    user_obj = User()
    user_obj.fromJSON(user)
    today = date.today()
    user_obj.registration_date = f'{today.year}-{today.month}-{today.day}'
    db.put_user(user_obj)
    return user_obj


def get_user(user_id: str) -> str:
    """Puts a user into DB
    Parameters:
    user (str): The user id.
    Returns:
    User: The constructed User object
    """
    user = User(user_id=user_id)
    get_response = db.get_user(user)
    return get_response.get('Item').get('Body') if get_response.get('Item') else 'Get User failed'


def delete_user(user_id: str) -> bool:
    """Puts a user into DB
    Parameters:
    user (str): The user id.
    Returns:
    bool: Whether the user is deleted successfully
    """
    user = User(user_id=user_id)
    return db.delete_user(user).get('ResponseMetadata').get('HTTPStatusCode') == 200
