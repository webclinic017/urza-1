from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from news import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, pwd):
        validate_password(pwd)
        return pwd

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)
