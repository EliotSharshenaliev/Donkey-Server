from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError

from accounts.models import UserToRegister, RegisterBox

User = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    """
            {'id': 1, 'password': '',
            'last_login': '2023-07-21T09:06:47Z',
            'is_superuser': True,
            'username': 'admin',
            'first_name': 'wafmarat',
            'last_name': 'awfwafwfaaw',
            'email': '', 'is_staff': True,
            'is_active': True,
            'date_joined': '2023-07-20T05:05:17Z',
            'isOnline': False,
            'passport_number': 'AC1241252',
            'groups': [],
            'user_permissions': []}

    """

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "isOnline", "passport_number", "is_superuser"]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post_detail", queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "posts"]


class UserToRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=32)

    class Meta:
        model = UserToRegister
        fields = ["email", "username", "password"]


class RegisterBoxSerializer(serializers.ListSerializer):
    child = UserToRegisterSerializer()

    def create(self, validated_data):
        box = RegisterBox.objects.create()
        user_instances = []
        for user_data in validated_data:
            user_instance = UserToRegister.objects.create(box=box, **user_data)
            user_instances.append(user_instance)
        return user_instances

    # def create(self, validated_data):
    #     tracks_data = validated_data.pop('usertoregister')
    #     box = RegisterBox.objects.create()
    #     for track_data in tracks_data:
    #         UserToRegister.objects.create(box=box, **track_data)
    #     return box
