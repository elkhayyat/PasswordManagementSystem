from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.models import TextChoices, UIDModel


# Create your models here.
class Tenant(UIDModel):
    class Types(TextChoices):
        PERSONAL = 'personal', _('Personal')
        BUSINESS = 'business', _('Business')
        OWNER = 'owner', _('Owner')

    name = models.CharField(_('Name'), max_length=100)
    type = Types.model_field(verbose_name=_('Type'))
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Registration Date'))
    security_key = models.CharField(max_length=100, verbose_name=_('Security Key'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'tenants'

    @property
    def is_expired(self):
        if self.type == self.Types.PERSONAL:
            return False


class PersonalTenant(Tenant):
    type = Tenant.Types.model_field(default=Tenant.Types.PERSONAL)

    class Meta:
        default_related_name = 'personal_tenants'

    @property
    def is_expired(self):
        return False


class BusinessTenant(Tenant):
    type = Tenant.Types.model_field(default=Tenant.Types.BUSINESS)
    paid_till = models.DateTimeField(verbose_name=_('Paid Till'))

    class Meta:
        default_related_name = 'business_tenants'

    @property
    def is_expired(self):
        return self.paid_till is not None and self.paid_till < timezone.now()


class TenantModel(UIDModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class User(AbstractBaseUser, UIDModel):
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = _("Users")
        verbose_name = _("User")
        default_related_name = 'users'


class TenantUser(TenantModel, UIDModel):
    class Statuses(TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        LOCKED = 'locked', 'Locked'
        REJECTED = 'rejected', 'Rejected'

    class Roles(TextChoices):
        OWNER = 'Owner', 'Owner'
        ADMIN = 'Admin', 'Admin'
        USER = 'User', 'User'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = Roles.model_field(verbose_name='Role')
    status = Statuses.model_field(verbose_name=_('Status'), default=Statuses.ACTIVE)

    class Meta:
        default_related_name = 'tenant_users'
        verbose_name = _('Tenant User')
        verbose_name_plural = _('Tenant Users')


class TenantInvoice(TenantModel, UIDModel):
    class Statuses(TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        CANCELLED = 'cancelled', 'Cancelled'

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    status = Statuses.model_field(verbose_name=_('Status'), default=Statuses.PENDING)
    due_date = models.DateTimeField(verbose_name=_('Due Date'))
    reference = models.CharField(max_length=100, verbose_name=_('Reference'), null=True, blank=True)

    class Meta:
        default_related_name = 'tenant_invoices'
        verbose_name = _('Tenant Invoice')
        verbose_name_plural = _('Tenant Invoices')
