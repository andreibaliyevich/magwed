from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from main.models import Country, City, Language
from .choices import UserType
from .models import Customer, OrganizerRole, Organizer
from .utilities import decode_uid, check_token


UserModel = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    """ User Login Serializer """

    class Meta:
        model = UserModel
        fields = [
            'uuid',
            'username',
            'email',
            'user_type',
            'name',
            'avatar',
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    """ Registration Serializer """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password2': _('Password fields did not match.')})
        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            name=validated_data['name'],
        )

        if user.user_type == UserType.CUSTOMER:
            Customer.objects.create(user=user)
        elif user.user_type == UserType.ORGANIZER:
            Organizer.objects.create(user=user, profile_url=user.username)

        return user

    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'user_type',
            'name',
        ]
        extra_kwargs = {
            'user_type': {'choices': UserType.choices[1:]},
        }


class ActivationSerializer(serializers.Serializer):
    """ Activation Serializer """
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            user_uuid = decode_uid(data['uid'])
            self.user = UserModel.objects.get(uuid=user_uuid)
        except (UserModel.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'uid': _('Invalid user uuid or user does not exist.')},
                code='invalid_uid',
            )

        if not check_token(self.user, data['token']):
            raise serializers.ValidationError(
                {'token': _('Invalid token for given user.')},
                code='invalid_token',
            )

        return data


class PasswordChangeSerializer(serializers.Serializer):
    """ Password Change Serializer """
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    new_password2 = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Invalid current password.'))
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                'new_password2': _('Password fields did not match.')})
        return data


class PasswordResetSerializer(serializers.Serializer):
    """ Password Reset Serializer """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = UserModel.objects.get(email=value, is_active=True)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                _('User with given email does not exist.'))
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """ Password Reset Confirm Serializer """
    uid = serializers.CharField()
    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user_uuid = decode_uid(data['uid'])
            self.user = UserModel.objects.get(uuid=user_uuid)
        except (UserModel.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'uid': _('Invalid user uuid or user does not exist.')},
                code='invalid_uid',
            )

        if not check_token(self.user, data['token']):
            raise serializers.ValidationError(
                {'token': _('Invalid token for given user.')},
                code='invalid_token',
            )

        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                'new_password2': _('Password fields did not match.')})

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """ User Profile Serializer """

    class Meta:
        model = UserModel
        fields = [
            'name',
            'country',
            'city',
            'phone',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """ Customer Profile Serializer """
    user = UserProfileSerializer()

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.pop('user')

        user.name = user_data.get('name', user.name)
        user.country = user_data.get('country', user.country)
        user.city = user_data.get('city', user.city)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        instance.date_of_wedding = validated_data.get(
            'date_of_wedding', instance.date_of_wedding)
        instance.save()

        return instance

    class Meta:
        model = Customer
        fields = [
            'user',
            'date_of_wedding',
        ]


class OrganizerProfileSerializer(serializers.ModelSerializer):
    """ Organizer Profile Serializer """
    user = UserProfileSerializer()
    rating = serializers.DecimalField(
        read_only=True,
        max_digits=2,
        decimal_places=1,
    )
    pro_time = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.pop('user')

        user.name = user_data.get('name', user.name)
        user.country = user_data.get('country', user.country)
        user.city = user_data.get('city', user.city)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        instance.roles.set(validated_data.get('roles', instance.roles))
        instance.description = validated_data.get(
            'description', instance.description)
        instance.countries.set(
            validated_data.get('countries', instance.countries))
        instance.cities.set(validated_data.get('cities', instance.cities))
        instance.languages.set(
            validated_data.get('languages', instance.languages))
        instance.cost_work = validated_data.get(
            'cost_work', instance.cost_work)
        instance.number_hours = validated_data.get(
            'number_hours', instance.number_hours)
        instance.website = validated_data.get('website', instance.website)
        instance.profile_url = validated_data.get(
            'profile_url', instance.profile_url)
        instance.save()

        return instance

    class Meta:
        model = Organizer
        fields = [
            'user',
            'roles',
            'description',
            'countries',
            'cities',
            'languages',
            'cost_work',
            'number_hours',
            'website',
            'profile_url',
            'rating',
            'pro_time',
        ]


class ProfileDeleteSerializer(serializers.Serializer):
    """ Profile Delete Serializer """
    current_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Invalid current password.'))
        return value


class ProfileAvatarSerializer(serializers.ModelSerializer):
    """ Profile Avatar Serializer """

    class Meta:
        model = UserModel
        fields = ['avatar']


class OrganizerCoverSerializer(serializers.ModelSerializer):
    """ Organizer Cover Serializer """

    class Meta:
        model = Organizer
        fields = ['cover']


class UserAuthorReadSerializer(serializers.ModelSerializer):
    """ User Author Read Serializer """

    class Meta:
        model = UserModel
        fields = [
            'uuid',
            'name',
        ]


class UserOwnerReadSerializer(serializers.ModelSerializer):
    """ User Owner Read Serializer """
    profile_url = serializers.SerializerMethodField()

    def get_profile_url(self, obj):
        if obj.user_type == UserType.ORGANIZER:
            return obj.organizer.profile_url
        return None

    class Meta:
        model = UserModel
        fields = [
            'name',
            'avatar',
            'profile_url',
        ]


class UserBriefReadSerializer(serializers.ModelSerializer):
    """ User Brief Read Serializer """
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        ch_set = obj.connection_histories.all()
        if ch_set.filter(online=True).count() > 0:
            return 'online'
        ch_obj = ch_set.first()
        if ch_obj is not None:
            return str(ch_obj.last_visit)
        return None

    class Meta:
        model = UserModel
        fields = [
            'uuid',
            'name',
            'avatar',
            'status',
        ]


class UserShortReadSerializer(serializers.ModelSerializer):
    """ User Short Read Serializer """
    status = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()

    def get_status(self, obj):
        ch_set = obj.connection_histories.all()
        if ch_set.filter(online=True).count() > 0:
            return 'online'
        ch_obj = ch_set.first()
        if ch_obj is not None:
            return str(ch_obj.last_visit)
        return None

    def get_profile_url(self, obj):
        if obj.user_type == UserType.ORGANIZER:
            return obj.organizer.profile_url
        return None

    class Meta:
        model = UserModel
        fields = [
            'uuid',
            'name',
            'avatar',
            'status',
            'profile_url',
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):
    """ User Retrieve Serializer """
    status = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def get_status(self, obj):
        ch_set = obj.connection_histories.all()
        if ch_set.filter(online=True).count() > 0:
            return 'online'
        ch_obj = ch_set.first()
        if ch_obj is not None:
            return str(ch_obj.last_visit)
        return None

    def get_following(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.followers.filter(
                follower=self.context['request'].user,
            ).exists()
        return False

    class Meta:
        model = UserModel
        fields = [
            'uuid',
            'email',
            'name',
            'avatar',
            'country',
            'city',
            'phone',
            'date_joined',
            'status',
            'following',
        ]


class OrganizerListSerializer(serializers.ModelSerializer):
    """ Organizer List Serializer """
    user = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Organizer
        fields = [
            'user',
            'cost_work',
            'number_hours',
        ]


class OrganizerRetrieveSerializer(serializers.ModelSerializer):
    """ Organizer Retrieve Serializer """
    user = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = Organizer
        fields = [
            'user',
            'roles',
            'cover',
            'description',
            'countries',
            'cities',
            'languages',
            'cost_work',
            'number_hours',
            'website',
            'rating',
        ]
