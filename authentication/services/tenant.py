from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from authentication.models import TenantUser, Tenant


class CreateTenantService:
    def __init__(self, name: str, tenant_type: str | None):
        self.tenant = None
        self.name = name
        self.tenant_type = tenant_type
        self.execute()

    def execute(self):
        self.validate_tenant_type()
        self.create_tenant()
        return self.tenant

    def validate_tenant_type(self):
        if self.tenant_type not in Tenant.Types.values:
            raise ValueError(_('Invalid tenant type'))

    def create_tenant(self):
        self.tenant = Tenant.objects.create(name=self.name, type=self.tenant_type)


class CreatePersonalTenantService(CreateTenantService):
    def __init__(self, name: str):
        super().__init__(name, Tenant.Types.PERSONAL)


class CreateBusinessTenantService(CreateTenantService):
    def __init__(self, name: str):
        super().__init__(name, Tenant.Types.BUSINESS)


class TenantQuerySet(QuerySet):
    def personal(self):
        return self.filter(type=Tenant.Types.PERSONAL)

    def business(self):
        return self.filter(type=Tenant.Types.BUSINESS)

    def expired_business(self):
        return self.filter(type=Tenant.Types.BUSINESS, paid_till__lt=timezone.now())

    def active_business(self):
        return self.filter(type=Tenant.Types.BUSINESS, paid_till__gte=timezone.now())


class TenantPermissionService:
    @staticmethod
    def tenant_owner_type_exists():
        return Tenant.objects.filter(type=Tenant.Types.OWNER).exists()

    @staticmethod
    def has_only_one_owner(tenant):
        return tenant.tenantuser_set.filter(role=TenantUser.Roles.OWNER).count() == 1

    @staticmethod
    def is_owner(user, tenant):
        return tenant.tenantuser_set.filter(user=user, role=TenantUser.Roles.OWNER).exists()

    @staticmethod
    def is_admin(user, tenant):
        return tenant.tenantuser_set.filter(user=user, role=TenantUser.Roles.ADMIN).exists()

    @staticmethod
    def is_user(user, tenant):
        return tenant.tenantuser_set.filter(user=user, role=TenantUser.Roles.USER).exists()

    def has_access(self, user, tenant):
        return self.is_owner(user, tenant) or self.is_admin(user, tenant) or self.is_user(user, tenant)
