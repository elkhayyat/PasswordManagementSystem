from django.utils.translation import gettext_lazy as _

from authentication.models import User
from utils.services.base_filter import BaseModelFilter
from utils.services.base_get import BaseModelGet


class CreateUserService:
    def __init__(self, email, password: str, first_name: str | None = None,
                 last_name: str | None = None):
        self.user = None
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.execute()

    def prepare(self):
        self._check_email_is_unique()

    def execute(self):
        return self._create_user()

    def _create_user(self):
        self.user = User.objects.create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.user.set_password(self.password)
        self.user.save()
        return self.user

    def _check_email_is_unique(self):
        if User.objects.filter(email=self.email).exists():
            raise ValueError(_('Email is already taken'))


class GetOrCreateUserService:
    def __init__(self, email, password: str, first_name: str | None = None,
                 last_name: str | None = None):
        self.user = None
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.execute()

    def prepare(self):
        self._is_email_exists()

    def execute(self):
        return self._create_user()

    def _create_user(self):
        self.user = User.objects.get_or_create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.user.set_password(self.password)
        self.user.save()
        return self.user

    def _is_email_exists(self):
        if User.objects.filter(email=self.email).exists():
            return True
        return False


class ChangePasswordService:
    def __init__(self, user, new_password):
        self.user = user
        self.new_password = new_password
        self.execute()

    def execute(self):
        self.user.set_password(self.new_password)
        self.user.save()
        return self.user


class EditUserService:
    def __init__(self, user: 'User', password: str | None = None, first_name: str | None = None,
                 last_name: str | None = None):
        self.user = user
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.execute()

    def execute(self):
        return self._edit_user()

    def _edit_user(self):
        if self.password is not None:
            self.user.set_password(self.password)
        if self.first_name is not None:
            self.user.first_name = self.first_name
        if self.last_name is not None:
            self.user.last_name = self.last_name
        self.user.save()
        return self.user


class FilterUserService(BaseModelFilter):
    model = User


class GetUserService(BaseModelGet):
    model = User
