#utils.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def create_user(username, password, email, **kwargs):
    """
    Создает нового пользователя с заданными параметрами.
    """
    user = User.objects.create(
        username=username,
        email=email,
        **kwargs  # Позволяет передавать дополнительные параметры
    )
    user.set_password(password)
    user.save()
    return user


def create_superuser(username, password, email):
    """
    Создает суперпользователя.  Предполагается, что суперпользователь
    уже создан вручную, поэтому эта функция используется в основном
    для других целей.
    """
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password  # Суперпользователи создаются с открытым паролем, который потом хешируется
    )
    return user


def get_admin_user():
    """
    Возвращает существующего суперпользователя Niaz, если он существует,
    или создает его, если он не существует.
    """
    try:
        return User.objects.get(username="Niaz", is_superuser=True)
    except User.DoesNotExist:
        # Если суперпользователя нет, создаем его
        return create_superuser(
            username="Niaz",
            password="NIAZrezeda12",
            email="niaz.hakimov@mail.ru"
        )


def create_member_user(username, password, email):
    """
    Создает обычного пользователя.
    """
    return create_user(username=username, password=password, email=email)


def get_member_user():
    """
    Возвращает обычного пользователя.
    """
    user = User.objects.create(
        username="member_test",
        email="tester_member@test2.com",
    )
    user.set_password('qwerty')
    user.save()
    return user
