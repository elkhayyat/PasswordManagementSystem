from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from authentication.models import User, Tenant


class AddTenantUserService:
    def __init__(self, user: 'User', tenant: 'Tenant', role: str):
        self.user = user
        self.tenant = tenant
        self.role = role
        self.execute()

    def execute(self):
        return self._create_user_tenant()

    def _create_user_tenant(self):
        return self.user.tenantuser_set.create(tenant=self.tenant, role=self.role)


class LockTenantUser:
    def __init__(self, target_user, done_by):
        self.user = target_user
        self.done_by = done_by
        self.prepare()
        self.execute()

    def prepare(self):
        self._check_user_can_be_locked()

    def execute(self):
        self.user.is_active = False
        self.user.save()
        return self.user

    def _check_user_can_be_locked(self):
        if self.user.is_active is False:
            raise ValueError(_('User is already locked'))


class UnlockTenantUser:
    def __init__(self, target_user, done_by):
        self.user = target_user
        self.done_by = done_by
        self.prepare()
        self.execute()

    def prepare(self):
        self._check_user_can_be_unlocked()

    def execute(self):
        self.user.is_active = True
        self.user.save()
        return self.user

    def _check_user_can_be_unlocked(self):
        if self.user.is_active is True:
            raise ValueError(_('User is already unlocked'))


