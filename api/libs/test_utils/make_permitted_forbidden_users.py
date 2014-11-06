from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission, User


def make_permitted_forbidden_users(permissions_codenames):
    return (
        make_permitted_user(permissions_codenames),
        make_forbidden_user())


def make_permitted_user(permissions_codenames):
    """
    Make an ordinary, non-staff, non-admin user with Django permissions as
    defined in `permissions_codenames`. Attach a rest-framework auth token.
    """
    permitted = User.objects.create_user('permitted', '', 'password')
    Token.objects.create(user=permitted)

    for codename in permissions_codenames:
        permitted.user_permissions.add(
            Permission.objects.get(codename=codename))
    return permitted


def make_forbidden_user():
    """
    Make an ordinary, non-staff, non-admin user with no Django permissions with
    a rest-framework auth token.
    """
    forbidden = User.objects.create_user('forbidden', '', 'password')
    Token.objects.create(user=forbidden)
    return forbidden


def delete_users():
    User.objects.get(username='permitted').delete()
    User.objects.get(username='forbidden').delete()
