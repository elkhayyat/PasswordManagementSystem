from vault.models import VaultFolderPermission


class FolderRepository:
    def __init__(self, folder, user, permission, share_sub_folders=False):
        self.folder = folder
        self.user = user
        self.permission = permission
        self.share_sub_folders = share_sub_folders

    def is_user_has_access_to_folder(self, folder):
        return VaultFolderPermission.objects.filter(folder=folder, user=self.user, permission=self.permission).exists()

    def share_folder(self):
        pass
