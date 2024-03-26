class VaultPermission:
    def __init__(self, user, vault_item):
        self.user = user
        self.vault_item = vault_item

    def user_has_access_to_folder(self):
        if self.vault_item.folder is None:
            return True
        return self.vault_item.folder.tenant == self.user.tenant

    def user_has_access_to_vault_item(self):
        return self.vault_item.tenant == self.user.tenant
