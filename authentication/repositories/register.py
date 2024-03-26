from authentication.models import Tenant
from authentication.services.tenant import CreatePersonalTenantService, CreateBusinessTenantService
from authentication.services.user import CreateUserService
from utils.repositories import BaseRepository


class RegisterRepository(BaseRepository):
    def __init__(self, email: str, password: str, first_name: str, last_name: str, tenant_type: 'Tenant.Types',
                 tenant_name: str = None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.tenant_type = tenant_type
        self.tenant_name = tenant_name
        super().__init__()

    def execute(self):
        user = self._create_user()
        self._create_personal_tenant()
        if self.tenant_type == Tenant.Types.BUSINESS:
            self._create_business_tenant()
        return user

    def _create_user(self):
        return CreateUserService(self.email, self.password, self.first_name, self.last_name).execute()

    def _create_personal_tenant(self):
        tenant_name = f"{self.first_name} {self.last_name}"
        return CreatePersonalTenantService(tenant_name)

    def _create_business_tenant(self):
        return CreateBusinessTenantService(self.tenant_name)
