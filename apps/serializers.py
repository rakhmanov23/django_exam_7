from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.models import Vacancy, User


class VacancySerializer(ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmailSerializer(ModelSerializer):
    class Meta:
        fields = 'email',
        model = User


class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        if not email:
            raise serializers.ValidationError("Email is required")

        if not code:
            raise serializers.ValidationError("Verification code is required")

        return data