from django.db import models


class ActiveTenantUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
