from rest_framework import serializers
from django.contrib.auth import get_user_model
################################################################
# AUTHENTICATION SERIALIZER
################################################################
#user = UserDetaukSerializer(read_only=True)
User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    def get_avatar(self, user):
        request = self.context.get('request')
        avatar_url = user.avatar.url
        return request.build_absolute_uri(avatar_url)
    class Meta:
        model = User
        fields = ['email', 'firstName', 'lastName','avatar','faceboookAvatar' ,'longitude', 'latitude', 'status']


class UserCreateSerializer(serializers.ModelSerializer):
    email2 = serializers.EmailField(label='Confirm Email')
    class Meta:
        model= User
        fields = ['email','email2', 'buddycode','firstName','lastName', 'password']
        extra_kwargs = {"password": {"write_only":True}}

    def validate(self, data):
        return data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if(email1 != email2):
            raise serializers.ValidationError("Emails are not matched.")

        user_qs = User.objects.filter(email=email2)
        if(user_qs.exists()):
            raise serializers.ValidationError("user with this email address already exists.")
        return value

    def validate_buddycode(self, value):
        buddycode = value
        user_qs = User.objects.filter(buddycode=buddycode)
        if(user_qs.exists()):
            raise serializers.ValidationError("user with this buddycode already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        buddycode = validated_data['buddycode']
        user_obj = User(email = email, buddycode=buddycode, firstName = validated_data['firstName'], lastName = validated_data['lastName'])
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(label = "Email Address")
    class Meta:
        model= User
        fields = ['email','password', 'token']
        extra_kwargs = {"password": {"write_only":True}}

    def validate(self, data):
        user_obj=None
        email = data.get("email", None)
        password = data.get("password")
        if(not email):
            raise serializers.ValidationError("Email is empty")

        user = User.objects.filter(email=email).distinct()
        user = user.exclude(email__iexact='')
        if(user.exists() and user.count()==1):
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email is not valid")

        if (user_obj):
            if(not(user_obj.check_password(password))):
                raise serializers.ValidationError("Incorrect Username or Password")

        return data
