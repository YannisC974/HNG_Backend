from rest_framework import serializers
from .models import Survey, UserSurvey
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"
        extra_kwargs = {
            'status': {'read_only': True},
            'user': {'required': False},
            'user': {'read_only': True},
            'number_of_completed': {'read_only': True},
        }
    def validate(self, attrs):
        is_valid = any(item in attrs.keys() for item in ["physical_done", "mental_done", "social_done"])
        if not is_valid:
            raise serializers.ValidationError("Please fill the required fields")
        return super().validate(attrs)
    def create(self, validated_data):
        user = self.context.get('user')
        validated_data["user"] = user
        count = 0
        for item in ["physical_done", "mental_done", "social_done"]:
            if validated_data[item] == True:
                count+=1
        validated_data["number_of_completed"] = count
        return super().create(validated_data)
    
class UserSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSurvey
        fields = "__all__"
        read_only_fields = ['user', 'number_of_completed', 'is_choosed', 'is_validated'] 
