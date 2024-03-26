import uuid

from django.db import models

from encryption.encryption import Encryption


# Create your models here.
class UIDModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class SecuredCharField(models.BinaryField):
    @classmethod
    def decrypt(cls, key) -> str | None:
        if not cls.value:
            return None

        cipher_suite = Encryption(key)
        decrypted_value = cipher_suite.decrypt(cls.value)
        return decrypted_value


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.save()


class TextChoices(models.TextChoices):

    @classmethod
    def max_length(cls) -> int:
        return max(len(value) for value in cls.values)

    @classmethod
    def model_field(cls, verbose_name: str = None, default: 'TextChoices' = None) -> models.CharField:
        return models.CharField(verbose_name=verbose_name, max_length=cls.max_length(),
                                choices=cls.choices, default=default, null=True, blank=True)

    @classmethod
    def serialize_choices(cls):
        return [{'value': value, 'label': label} for value, label in cls.choices]
