from flask_login import current_user
from ..models import UserFriend


def get_all_friends() -> list:
    """ Возвращает список всех друзей пользователя """
    list_friends = list()

    q1 = UserFriend.query.filter(UserFriend.friend_one == current_user.id).all()
    q2 = UserFriend.query.filter(UserFriend.friend_two == current_user.id).all()

    list_friends.extend([q.friend_two for q in q1])
    list_friends.extend([q.friend_one for q in q2])

    return list_friends
