from rest_framework import serializers

from vault.models import VaultItem


class VaultItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultItem
        fields = '__all__'
        read_only_fields = ('id', 'uid', 'created_at', 'updated_at')
