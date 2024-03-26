from rest_framework import serializers


class UIDSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=255, source='uid')
