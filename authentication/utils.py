from encryption.encryption import KeyGenerator


class TenantSecurityKey:
    def __init__(self, tenant):
        self.tenant = tenant

    @staticmethod
    def generate_key():
        return KeyGenerator.generate_key()

    def set_random_security_key(self):
        self.tenant.security_key = self.generate_key()
        self.tenant.save()
