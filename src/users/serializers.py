# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        name = validated_data.pop("name")
        validated_data.pop("confirm_password")

        first_name, *last_name = name.split(" ", 1)
        user = User(
            email=validated_data["email"],
            username=validated_data["email"],  # username is required
            first_name=first_name,
            last_name=last_name[0] if last_name else "",
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
