from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from diet_app.models import User, UserProfile, FoodLog

class UserSerializer(ModelSerializer):

    profile = serializers.SerializerMethodField(read_only = True)

    class Meta:

        model = User

        fields = ['id', 'username', "email", 'phone', 'password', 'profile']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)
    
    def get_profile(self, object):

        try:

            profile_inst = UserProfile.objects.get(owner = object)

            serailizer_inst = UserProfileSerializer(profile_inst)

            return serailizer_inst.data
        
        except:

            return "No Profile"

        # try:

        #     profile = object.profile

        #     return {
        #         "height" : profile.height,
        #         "weight" : profile.weight,
        #         "age" : profile.age,
        #         "gender" : profile.gender,
        #         "activity_level" : profile.activity_level,
        #         "bmr" : profile.bmr,
        #     }
        
        # except:

        #     return None

class UserProfileSerializer(ModelSerializer):

    owner = serializers.StringRelatedField(read_only = True)

    class Meta:

        model = UserProfile

        fields = "__all__"

        read_only_fields = ['id', 'owner', "bmr"]


class FoodLogSerializer(serializers.ModelSerializer):

    class Meta:

        model = FoodLog

        fields = "__all__"

        read_only_fields = ["id", "owner", "created_at"]




        



