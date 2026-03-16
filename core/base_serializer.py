from rest_framework import serializers


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "code", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
