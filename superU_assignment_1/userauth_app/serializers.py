from rest_framework import serializers
from .models import User, UserProfiles

class UserSerializser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password' : {'write_only':True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) # set_password is provided by django and the password is hashed

        instance.save()
        return instance

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserProfiles
        # fields = ['id', 'fname', 'lname', 'phone_no', 'address', 'gender', 'email', 'bio', 'profile_picture_url']
        fields = '__all__'   