from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        list_fields_primary = ["id", "name", "last_name"]
        list_fields_secondary = ["birthday", "email", "curp", "rfc"]

        fields = list_fields_primary + list_fields_secondary
