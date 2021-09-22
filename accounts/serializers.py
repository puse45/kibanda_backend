from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.choices import ROLES_TYPE
from accounts.models import Customer

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    expiry_time = serializers.DateTimeField(read_only=True)
    lifetime = serializers.DurationField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "sur_name",
            "first_name",
            "last_name",
            "email",
            "gender",
            "date_of_birth",
            "phone_number",
            "role",
        )


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    user = UserDetailSerializer(many=False, read_only=True)
    message = serializers.CharField(read_only=True)
    token = TokenSerializer(read_only=True, required=False)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        phone_number = data.get("phone_number", None)
        if not any([email, phone_number]):
            raise serializers.ValidationError(
                "Unable to login with provided credentials"
            )
        try:
            user_filter = {}
            if email:
                user_filter.update({"email": str(email)})
            else:
                user_filter.update({"phone_number": str(phone_number)})
            user = User.objects.get(**user_filter)
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            raise serializers.ValidationError(
                _("Unable to login with provided credentials")
            ) from e
        if not user.check_password(password):
            raise serializers.ValidationError(_("Invalid login credentials"))
        # authenticate(email=email, password=password)
        try:
            is_enabled = user.is_active and user.is_verified
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)
            validation = {
                "user": user,
                "message": ""
                if is_enabled
                else "Verify your account to retrieve token.",
            }
            if is_enabled:
                validation["token"] = {
                    "access": access_token,
                    "refresh": refresh_token,
                    "lifetime": refresh.lifetime,
                    "expiry_time": user.last_login + refresh.lifetime,
                }
            return validation
        except User.DoesNotExist as e:
            raise serializers.ValidationError(_("Invalid login credentials")) from e


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    sur_name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    user_type = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "sur_name",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "email",
            "password1",
            "password2",
            "role",
            "user_type",
        )
        extra_kwargs = {
            "role": {"write_only": True},
        }

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        phone = validated_data.pop("phone_number", validated_data.get("username", None))
        pwd = validated_data.pop("password1")
        user_type = validated_data.pop("user_type", None)
        validated_data.pop("password2")
        user = User.objects.create_user(
            email=email, phone_number=phone, password=pwd, **validated_data
        )
        if user_type:
            Customer.objects.create(customer_id=user.id, sales_agent_id=user_type.id)
        # return validated_data
        return user

    def validate(self, attrs):
        email = attrs.get("email", None)
        sur_name = attrs.get("sur_name", None)
        user_type = attrs.get("user_type", None)
        first_name = attrs.get("first_name", None)
        last_name = attrs.get("last_name", None)
        phone = attrs.get("phone_number", attrs.get("username", None))
        pwd1 = attrs.get("password1", None)
        pwd2 = attrs.get("password2", None)
        # if User.objects.filter(email=email).exists():
        #     raise serializers.ValidationError(_("User with this email already exists."))
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError(
                _("User with this phone number already exists.")
            )
        if email is None:
            email = f"{first_name.lower()}.{last_name.lower()}@temp.com"
            attrs["email"] = email
        if user_type is not None and user_type.role != ROLES_TYPE.SALES:
            raise serializers.ValidationError(
                _(
                    f"Sorry your user role must be of {ROLES_TYPE.SALES} to create a customer"
                )
            )
        if not all([email, phone, pwd1, pwd2]):
            raise serializers.ValidationError(
                _("Email, Phone number and passwords are required.")
            )
        if not pwd1 == pwd2:
            raise serializers.ValidationError(_("The passwords don't match."))
        return attrs


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "sur_name",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "is_superuser",
            "password",
            "full_name",
            "email",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.is_staff = True
        user.save()
        return user


class CreateCustomerSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    sur_name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "sur_name",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password1",
            "password2",
        )

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        phone = validated_data.pop("phone_number", validated_data.get("username", None))
        pwd = validated_data.pop("password1")
        validated_data.pop("password2")
        user = User.objects.create_user(
            email=email, phone_number=phone, password=pwd, **validated_data
        )
        return user

    def validate(self, attrs):
        email = attrs.get("email", None)
        sur_name = attrs.get("sur_name", None)
        first_name = attrs.get("first_name", None)
        last_name = attrs.get("last_name", None)
        phone = attrs.get("phone_number", attrs.get("username", None))
        pwd1 = attrs.get("password1", None)
        pwd2 = attrs.get("password2", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("User with this email already exists."))
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError(
                _("User with this phone number already exists.")
            )
        if email is None:
            email = f"{first_name.lower()}.{last_name.lower()}@temp.com"
            attrs["email"] = email

        if not all([email, phone, pwd1, pwd2]):
            raise serializers.ValidationError(
                _("Email, Phone number and passwords are required.")
            )
        if not pwd1 == pwd2:
            raise serializers.ValidationError(_("The passwords don't match."))
        return attrs
