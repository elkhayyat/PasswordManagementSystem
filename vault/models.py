from abc import abstractmethod

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import TenantModel
from encryption.encryption import Encryption
from utils.models import UIDModel, SoftDeleteModel, SecuredCharField, TextChoices


# Create your models here.
class Folder(TenantModel, SoftDeleteModel, UIDModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Folders")
        default_permissions = []
        permissions = [
            ('create_folder', _('Create Folder')),
            ('edit_folder', _('Edit Folder')),
            ('delete_folder', _('Delete Folder')),
        ]


class VaultItem(TenantModel, SoftDeleteModel, UIDModel):
    class Types(TextChoices):
        PASSWORD = 'password', _('Password')
        BANK_CARD = 'bank_card', _('Bank Card')
        SECURED_NOTE = 'secured_note', _('Secured Note')

    type = Types.model_field(verbose_name=_('Type'))
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_cipher_suite(self) -> Encryption:
        return Encryption(self.tenant.security_key)

    def get_tenant_decoded_key(self):
        return self.tenant.security_key.decrypt(self.tenant.security_key)

    @abstractmethod
    def set_data(self, *args, **kwargs):
        pass

    class Meta:
        verbose_name_plural = _("Secured Items")
        default_related_name = "secured_items"
        default_permissions = []
        permissions = [
            ('create_vault_item', _('Create Vault Item')),
            ('edit_vault_item', _('Edit Vault Item')),
            ('soft_delete_vault_item', _('Soft Delete Vault Item')),
            ('hard_delete_vault_item', _('Hard Delete Vault Item'))
        ]


class LoginItem(VaultItem):
    username = SecuredCharField()
    password = SecuredCharField()
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    def set_data(self, username, password):
        self.username = self.get_cipher_suite().encrypt(username)
        self.password = self.get_cipher_suite().encrypt(password)

    class Meta:
        verbose_name_plural = _("Login Items")


class BankCard(VaultItem):
    class CardType(TextChoices):
        MASTER_CARD = "master_card", _("Master Card")
        VISA = "visa", _("VISA")
        MADA = "mada", _("Mada")

    card_number = SecuredCharField()
    holder_name = SecuredCharField()
    expiration_date = SecuredCharField()
    cvv = SecuredCharField()
    card_type = CardType.model_field()

    def set_data(self, card_number, holder_name, expiration_date, cvv):
        self.card_number = self.get_cipher_suite().encrypt(card_number)
        self.holder_name = self.get_cipher_suite().encrypt(holder_name)
        self.expiration_date = self.get_cipher_suite().encrypt(expiration_date)
        self.cvv = self.get_cipher_suite().encrypt(cvv)

    class Meta:
        verbose_name_plural = _("Bank Cards")


class SecuredNote(VaultItem):
    note = SecuredCharField()

    def set_data(self, note):
        self.note = self.get_cipher_suite().encrypt(note)

    class Meta:
        verbose_name_plural = _("Secured Notes")


class VaultAccessLog(UIDModel):
    class Actions(TextChoices):
        ACCESS = "access", _("Access")
        COPY_PASSWORD = "copy_password", _("Copy Password")

    timestamp = models.DateTimeField(auto_now_add=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    action = Actions.model_field()
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    item = models.ForeignKey(VaultItem, on_delete=models.PROTECT)


class VaultFolderPermission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class VaultItemPermission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(VaultItem, on_delete=models.CASCADE)
