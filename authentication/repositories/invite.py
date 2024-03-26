from authentication.services.user import GetUserService


class InviteUserToTenantRepository:
    def __init__(self, tenant, email):
        self.user = None
        self.tenant = tenant
        self.email = email

    def _get_user(self):
        return GetUserService(email=self.email).execute()
