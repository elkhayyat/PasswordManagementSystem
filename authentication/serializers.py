from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from authentication.models import Tenant, TenantUser
from authentication.repositories.register import RegisterRepository
from utils.serializers import UIDSerializer


class UserSerializer(UIDSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'tenants']
        read_only_fields = ['id', 'is_active', 'date_joined', 'tenants']


class TenantUserSerializer(UIDSerializer):
    class Meta:
        model = TenantUser
        fields = ['id', 'tenant', 'user', 'role', 'status']
        read_only_fields = ['id', 'tenant', 'user']


class TenantSerializer(UIDSerializer):
    tenant_users = TenantUserSerializer(many=True)

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'type', 'registration_date', 'tenant_users']
        read_only_fields = ['id', 'registration_date', 'tenant_users']


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField()
    tenant_type = serializers.ChoiceField(choices=Tenant.Types.values)
    tenant_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        RegisterRepository(**validated_data).execute()

    @staticmethod
    def validate_email(email):
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(_('Email already exists'))
        return email

    def validate_tenant_name(self, tenant_name):
        if self.fields.get('tenant_type') == Tenant.Types.BUSINESS and not tenant_name:
            raise serializers.ValidationError(_('Tenant name is required for business account'))
        return tenant_name

    def validate_first_name(self, first_name):
        if not first_name and self.fields.get('tenant_type') == Tenant.Types.PERSONAL:
            raise serializers.ValidationError(_('First name is required for personal account'))
        return first_name

    def validate_last_name(self, last_name):
        if not last_name and self.fields.get('tenant_type') == Tenant.Types.PERSONAL:
            raise serializers.ValidationError(_('Last name is required for personal account'))
        return last_name


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
